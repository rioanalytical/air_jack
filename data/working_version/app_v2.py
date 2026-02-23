"""
FastAPI for quantitative finance data and portfolio risk analysis
Designed for quant professionals with meaningful risk metrics
"""

import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

import numpy as np
import pandas as pd
import sqlite3
from scipy import stats

from fastapi import FastAPI, Query, HTTPException, Body, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator, EmailStr

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create logs directory if it doesn't exist
Path('logs').mkdir(exist_ok=True)

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
DB_PATH = Path(__file__).parent.parent / "market_data.db"

class DatabaseManager:
    """SQLite connection manager with error handling"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._validate_database()
    
    def _validate_database(self):
        """Validate database exists and is accessible"""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")
        
        # Test connection
        try:
            conn = self.get_connection()
            conn.close()
            logger.info(f"Database connection verified: {self.db_path}")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def get_connection(self):
        """Get SQLite connection with proper configuration"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent access
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

db_manager = DatabaseManager(DB_PATH)

# ============================================================================
# PYDANTIC MODELS (Request/Response Validation)
# ============================================================================

class PortfolioRequest(BaseModel):
    """Portfolio metrics request model"""
    holdings: Dict[str, float] = Field(
        ..., 
        description="Ticker -> weight mapping (must sum to 1.0)"
    )
    start_date: Optional[str] = Field(
        None, 
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Start date in YYYY-MM-DD format"
    )
    end_date: Optional[str] = Field(
        None, 
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="End date in YYYY-MM-DD format"
    )
    risk_free_rate: float = Field(
        0.02, 
        ge=0, 
        le=0.1,
        description="Annual risk-free rate for Sharpe ratio"
    )
    
    @validator("holdings")
    def validate_weights(cls, v):
        """Validate holdings dictionary"""
        if not v:
            raise ValueError("holdings cannot be empty")
        
        # Validate each ticker
        for ticker, weight in v.items():
            if not isinstance(ticker, str) or not ticker.strip():
                raise ValueError(f"Invalid ticker: {ticker}")
            if not isinstance(weight, (int, float)):
                raise ValueError(f"Weight for {ticker} must be numeric")
            if weight < 0:
                raise ValueError(f"Weight for {ticker} cannot be negative")
        
        # Validate sum
        weight_sum = sum(v.values())
        if not (0.99 <= weight_sum <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {weight_sum:.4f}")
        
        return v

class PriceResponse(BaseModel):
    """Price data response"""
    ticker: str
    data: List[Dict]
    count: int
    date_range: Optional[Dict] = None

class ReturnsResponse(BaseModel):
    """Returns statistics response"""
    ticker: str
    returns: List[float]
    statistics: Dict[str, float]
    count: int

class VolatilityResponse(BaseModel):
    """Volatility response"""
    ticker: str
    volatility: List[float]
    dates: List[str]
    statistics: Dict[str, float]
    window_days: int
    count: int

class CorrelationResponse(BaseModel):
    """Correlation matrix response"""
    correlation: Dict
    covariance: Dict
    tickers: List[str]
    observations: int
    date_range: Dict[str, str]

class DrawdownResponse(BaseModel):
    """Drawdown metrics response"""
    ticker: str
    max_drawdown: float
    max_drawdown_date: str
    recovery_date: Optional[str]
    drawdown_series: List[float]
    dates: List[str]
    observation_count: int

class VaRResponse(BaseModel):
    """Value at Risk response"""
    ticker: str
    method: str
    lookback_days: int
    var: Dict[str, float]
    expected_return: float
    volatility: float

class PortfolioMetricsResponse(BaseModel):
    """Portfolio metrics response"""
    holdings: Dict[str, float]
    performance: Dict[str, float]
    correlation_matrix: Dict
    observations: int
    date_range: Dict[str, str]

class TickerInfoResponse(BaseModel):
    """Ticker metadata response"""
    ticker: str
    record_count: int
    earliest_date: str
    latest_date: str
    avg_volume: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    database: str
    version: str = "1.0.0"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def parse_date(date_str: Optional[str]) -> Optional[str]:
    """
    Parse and validate date string
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Validated date string or None
        
    Raises:
        ValueError: If date format is invalid
    """
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")

def validate_ticker(ticker: str) -> str:
    """
    Validate and normalize ticker symbol
    
    Args:
        ticker: Ticker symbol
        
    Returns:
        Normalized ticker (uppercase)
        
    Raises:
        ValueError: If ticker is invalid
    """
    ticker = ticker.strip().upper()
    
    if not ticker:
        raise ValueError("Ticker cannot be empty")
    
    if not ticker.isalpha():
        raise ValueError(f"Ticker must contain only letters: {ticker}")
    
    if len(ticker) > 5:
        raise ValueError(f"Ticker too long (max 5 chars): {ticker}")
    
    return ticker

def validate_tickers(tickers_str: str, min_count: int = 1) -> List[str]:
    """
    Validate comma-separated tickers
    
    Args:
        tickers_str: Comma-separated ticker symbols
        min_count: Minimum number of tickers required
        
    Returns:
        List of validated tickers
        
    Raises:
        ValueError: If validation fails
    """
    if not tickers_str or not tickers_str.strip():
        raise ValueError("Ticker(s) required")
    
    tickers = [validate_ticker(t) for t in tickers_str.split(",")]
    
    if len(tickers) < min_count:
        raise ValueError(f"Need at least {min_count} ticker(s), got {len(tickers)}")
    
    return tickers

def execute_query(
    query: str,
    params: List = None,
    fetch_one: bool = False
) -> pd.DataFrame or Dict:
    """
    Execute SQL query safely with error handling
    
    Args:
        query: SQL query string
        params: Query parameters
        fetch_one: Return single row as dict
        
    Returns:
        DataFrame or dict depending on fetch_one
        
    Raises:
        Exception: Database errors
    """
    conn = db_manager.get_connection()
    try:
        if fetch_one:
            cursor = conn.execute(query, params or [])
            row = cursor.fetchone()
            return dict(row) if row else None
        else:
            return pd.read_sql(query, conn, params=params or [])
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        raise
    finally:
        conn.close()

# ============================================================================
# APPLICATION LIFESPAN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    logger.info("🚀 Quant Finance API starting up...")
    logger.info(f"Database: {DB_PATH}")
    yield
    logger.info("🛑 Quant Finance API shutting down...")

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Quant Finance API",
    description="Portfolio risk analysis and market data for quantitative professionals",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# HEALTH & METADATA ENDPOINTS
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check"
)
async def health():
    """
    Health check endpoint
    
    Returns:
        Status, timestamp, and database connection status
    """
    try:
        conn = db_manager.get_connection()
        cursor = conn.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check - DB error: {e}")
        db_status = "error"
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        database=db_status
    )

@app.get(
    "/available-tickers",
    tags=["Metadata"],
    summary="Get all available tickers"
)
async def available_tickers():
    """
    Get list of all tickers in database
    
    Returns:
        List of tickers and count
    """
    try:
        query = "SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker"
        df = execute_query(query)
        
        return {
            "tickers": df["ticker"].tolist() if not df.empty else [],
            "count": len(df)
        }
    except Exception as e:
        logger.error(f"Error getting tickers: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tickers"
        )

@app.get(
    "/ticker-info/{ticker}",
    response_model=TickerInfoResponse,
    tags=["Metadata"],
    summary="Get ticker metadata"
)
async def ticker_info(ticker: str ):
    """
    Get metadata about a specific ticker
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Record count, date range, and average volume
    """
    try:
        tk = validate_ticker(ticker)
        
        query = """
        SELECT 
            COUNT(*) as record_count,
            MIN(date) as earliest_date,
            MAX(date) as latest_date,
            AVG(volume) as avg_volume
        FROM stock_prices 
        WHERE ticker = ?
        """
        
        result = execute_query(query, [tk], fetch_one=True)
        
        if not result or result["record_count"] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for ticker {tk}"
            )
        
        return TickerInfoResponse(
            ticker=tk,
            record_count=int(result["record_count"]),
            earliest_date=result["earliest_date"],
            latest_date=result["latest_date"],
            avg_volume=float(result["avg_volume"] or 0)
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting ticker info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve ticker information"
        )

# ============================================================================
# BASIC DATA ENDPOINTS
# ============================================================================

@app.get(
    "/prices",
    tags=["Market Data"],
    summary="Get OHLCV price data"
)
async def get_prices(
    ticker: str = Query(..., description="Comma-separated ticker symbols"),
    start_date: Optional[str] = Query(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Start date (YYYY-MM-DD)"
    ),
    end_date: Optional[str] = Query(
        None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="End date (YYYY-MM-DD)"
    ),
    limit: int = Query(1000, ge=1, le=100000, description="Max rows per ticker")
):
    """
    Get OHLCV data for ticker(s) and date range
    
    Args:
        ticker: Comma-separated list of tickers
        start_date: Optional start date
        end_date: Optional end date
        limit: Maximum rows per ticker
        
    Returns:
        Dictionary with ticker data and statistics
    """
    try:
        tickers = validate_tickers(ticker)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        results = {}
        
        for tk in tickers:
            query = "SELECT * FROM stock_prices WHERE ticker = ?"
            params = [tk]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date DESC LIMIT ?"
            params.append(limit)
            
            df = execute_query(query, params)
            
            if df.empty:
                results[tk] = {"data": [], "count": 0}
            else:
                df = df.sort_values("date").reset_index(drop=True)
                results[tk] = {
                    "data": df.to_dict(orient="records"),
                    "count": len(df),
                    "date_range": {
                        "start": df["date"].min(),
                        "end": df["date"].max()
                    }
                }
        
        return results
    
    except Exception as e:
        logger.error(f"Error in get_prices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve price data"
        )

# ============================================================================
# RETURNS & VOLATILITY ENDPOINTS
# ============================================================================

@app.get(
    "/returns",
    tags=["Analytics"],
    summary="Calculate returns statistics"
)
async def get_returns(
    ticker: str = Query(..., description="Comma-separated ticker symbols"),
    start_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    return_type: str = Query("log", enum=["simple", "log"], description="Return calculation method")
):
    """
    Calculate returns and return statistics for ticker(s)
    
    Args:
        ticker: Comma-separated ticker symbols
        start_date: Optional start date
        end_date: Optional end date
        return_type: 'simple' or 'log' returns
        
    Returns:
        Returns series and statistics (mean, std, skewness, kurtosis, etc.)
    """
    try:
        tickers = validate_tickers(ticker)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        results = {}
        
        for tk in tickers:
            query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
            params = [tk]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date"
            
            df = execute_query(query, params)
            
            if len(df) < 2:
                results[tk] = {
                    "error": "Insufficient data",
                    "count": len(df)
                }
                continue
            
            # Calculate returns
            if return_type == "log":
                returns = np.log(df["close"] / df["close"].shift(1)).dropna()
            else:
                returns = df["close"].pct_change().dropna()
            
            results[tk] = {
                "returns": returns.tolist(),
                "statistics": {
                    "mean": float(returns.mean()),
                    "std": float(returns.std()),
                    "min": float(returns.min()),
                    "max": float(returns.max()),
                    "median": float(returns.median()),
                    "skewness": float(returns.skew()),
                    "kurtosis": float(returns.kurtosis()),
                    "var_95": float(np.percentile(returns, 5))  # Value at Risk
                },
                "count": len(returns),
                "type": return_type
            }
        
        return results
    
    except Exception as e:
        logger.error(f"Error in get_returns: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate returns"
        )

@app.get(
    "/volatility",
    tags=["Analytics"],
    summary="Calculate rolling volatility"
)
async def get_volatility(
    ticker: str = Query(..., description="Comma-separated ticker symbols"),
    window: int = Query(20, ge=2, le=500, description="Rolling window in days"),
    start_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
):
    """
    Calculate rolling volatility for ticker(s)
    
    Args:
        ticker: Comma-separated ticker symbols
        window: Rolling window size in days
        start_date: Optional start date
        end_date: Optional end date
        
    Returns:
        Rolling volatility series and statistics
    """
    try:
        tickers = validate_tickers(ticker)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        results = {}
        
        for tk in tickers:
            query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
            params = [tk]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date"
            
            df = execute_query(query, params)
            
            if len(df) < window + 1:
                results[tk] = {
                    "error": f"Insufficient data (need {window + 1} days, got {len(df)})"
                }
                continue
            
            returns = np.log(df["close"] / df["close"].shift(1)).dropna()
            rolling_vol = returns.rolling(window=window).std()
            
            results[tk] = {
                "volatility": rolling_vol.tolist(),
                "dates": df["date"].iloc[window:].tolist(),
                "statistics": {
                    "mean_volatility": float(rolling_vol.mean()),
                    "current_volatility": float(rolling_vol.iloc[-1]),
                    "min_volatility": float(rolling_vol.min()),
                    "max_volatility": float(rolling_vol.max()),
                    "median_volatility": float(rolling_vol.median())
                },
                "window_days": window,
                "count": len(rolling_vol)
            }
        
        return results
    
    except Exception as e:
        logger.error(f"Error in get_volatility: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate volatility"
        )

# ============================================================================
# CORRELATION & COVARIANCE ENDPOINTS
# ============================================================================

@app.get(
    "/correlation",
    tags=["Analytics"],
    summary="Calculate correlation matrix"
)
async def get_correlation(
    tickers: str = Query(..., description="Comma-separated tickers (min 2)"),
    start_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    return_type: str = Query("log", enum=["simple", "log"])
):
    """
    Calculate correlation matrix between tickers
    
    Args:
        tickers: Comma-separated tickers (minimum 2)
        start_date: Optional start date
        end_date: Optional end date
        return_type: 'simple' or 'log' returns
        
    Returns:
        Correlation and covariance matrices
    """
    try:
        ticker_list = validate_tickers(tickers, min_count=2)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        price_data = {}
        
        for tk in ticker_list:
            query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
            params = [tk]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date"
            
            df = execute_query(query, params)
            price_data[tk] = df.set_index("date")["close"]
        
        prices_df = pd.DataFrame(price_data).dropna()
        
        if len(prices_df) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient overlapping data for correlation"
            )
        
        if return_type == "log":
            returns_df = np.log(prices_df / prices_df.shift(1)).dropna()
        else:
            returns_df = prices_df.pct_change().dropna()
        
        corr_matrix = returns_df.corr()
        cov_matrix = returns_df.cov()
        
        return {
            "correlation": corr_matrix.to_dict(),
            "covariance": cov_matrix.to_dict(),
            "tickers": ticker_list,
            "observations": len(returns_df),
            "date_range": {
                "start": prices_df.index.min(),
                "end": prices_df.index.max()
            },
            "return_type": return_type
        }
    
    except Exception as e:
        logger.error(f"Error in get_correlation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate correlation"
        )

# ============================================================================
# DRAWDOWN & RISK ENDPOINTS
# ============================================================================

@app.get(
    "/drawdown",
    tags=["Risk Analytics"],
    summary="Calculate maximum drawdown"
)
async def get_drawdown(
    ticker: str = Query(..., description="Single ticker symbol"),
    start_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end_date: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$")
):
    """
    Calculate maximum drawdown and drawdown series
    
    Args:
        ticker: Single ticker symbol
        start_date: Optional start date
        end_date: Optional end date
        
    Returns:
        Maximum drawdown, recovery date, and drawdown series
    """
    try:
        tk = validate_ticker(ticker)
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
        params = [tk]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = execute_query(query, params)
        
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for ticker {tk}"
            )
        
        # Calculate drawdown
        running_max = df["close"].expanding().max()
        drawdown = (df["close"] - running_max) / running_max
        
        max_drawdown = float(drawdown.min())
        max_dd_idx = drawdown.idxmin()
        max_dd_date = df.loc[max_dd_idx, "date"]
        
        # Find recovery date
        recovery_date = None
        recovery_idx = df[df.index > max_dd_idx]["close"][
            df["close"] > running_max[max_dd_idx]
        ]
        
        if not recovery_idx.empty:
            recovery_date = df.loc[recovery_idx.index[0], "date"]
        
        return {
            "ticker": tk,
            "max_drawdown": max_drawdown,
            "max_drawdown_percent": max_drawdown * 100,
            "max_drawdown_date": max_dd_date,
            "recovery_date": recovery_date,
            "drawdown_series": drawdown.tolist(),
            "dates": df["date"].tolist(),
            "observation_count": len(df)
        }
    
    except Exception as e:
        logger.error(f"Error in get_drawdown: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate drawdown"
        )

@app.get(
    "/var",
    tags=["Risk Analytics"],
    summary="Calculate Value at Risk"
)
async def get_value_at_risk(
    ticker: str = Query(..., description="Single ticker symbol"),
    confidence_levels: str = Query(
        "0.95,0.99",
        description="Comma-separated confidence levels (e.g., 0.95,0.99)"
    ),
    method: str = Query("historical", enum=["historical", "gaussian"]),
    lookback_days: Optional[int] = Query(None, ge=2, le=10000)
):
    """
    Calculate Value at Risk (VaR) at different confidence levels
    
    Args:
        ticker: Single ticker symbol
        confidence_levels: Comma-separated confidence levels (0-1)
        method: 'historical' or 'gaussian' estimation method
        lookback_days: Optional number of days to look back
        
    Returns:
        VaR at specified confidence levels with expected return and volatility
    """
    try:
        tk = validate_ticker(ticker)
        conf_levels = [float(x.strip()) for x in confidence_levels.split(",")]
        
        # Validate confidence levels
        if not conf_levels:
            raise ValueError("At least one confidence level required")
        
        for conf in conf_levels:
            if not (0 < conf < 1):
                raise ValueError(f"Confidence level must be between 0 and 1, got {conf}")
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        query = "SELECT date, close FROM stock_prices WHERE ticker = ? ORDER BY date"
        
        df = execute_query(query, [tk])
        
        if df.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No data found for ticker {tk}"
            )
        
        if lookback_days:
            df = df.tail(lookback_days)
        
        returns = np.log(df["close"] / df["close"].shift(1)).dropna()
        
        var_results = {}
        
        for conf in conf_levels:
            if method == "historical":
                var = np.percentile(returns, (1 - conf) * 100)
            else:  # gaussian
                mean = returns.mean()
                std = returns.std()
                var = stats.norm.ppf(1 - conf) * std + mean
            
            var_results[f"VaR_{int(conf*100)}"] = float(var)
        
        return {
            "ticker": tk,
            "method": method,
            "lookback_days": len(returns),
            "var": var_results,
            "expected_return": float(returns.mean()),
            "volatility": float(returns.std()),
            "confidence_levels": conf_levels
        }
    
    except Exception as e:
        logger.error(f"Error in get_value_at_risk: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate Value at Risk"
        )

# ============================================================================
# PORTFOLIO ENDPOINTS
# ============================================================================

@app.post(
    "/portfolio-metrics",
    tags=["Portfolio Analysis"],
    summary="Calculate portfolio metrics"
)
async def get_portfolio_metrics(
    portfolio: PortfolioRequest
):
    """
    Calculate comprehensive portfolio metrics
    
    Args:
        portfolio: Portfolio configuration with holdings and dates
        
    Returns:
        Portfolio performance metrics, correlation matrix, and date range
    """
    try:
        start_date = parse_date(portfolio.start_date)
        end_date = parse_date(portfolio.end_date)
        
        # Validate and normalize holdings
        holdings = {
            validate_ticker(t): w 
            for t, w in portfolio.holdings.items()
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    try:
        price_data = {}
        
        # Fetch price data for all tickers
        for ticker in holdings.keys():
            query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
            params = [ticker]
            
            if start_date:
                query += " AND date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND date <= ?"
                params.append(end_date)
            
            query += " ORDER BY date"
            
            df = execute_query(query, params)
            if df.empty:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No data found for ticker {ticker}"
                )
            
            price_data[ticker] = df.set_index("date")["close"]
        
        # Align all series to common dates
        prices_df = pd.DataFrame(price_data).dropna()
        
        if len(prices_df) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient overlapping data for portfolio analysis"
            )
        
        # Calculate returns
        returns_df = np.log(prices_df / prices_df.shift(1)).dropna()
        
        # Portfolio weights
        weights = np.array([holdings[ticker] for ticker in holdings.keys()])
        
        # Portfolio metrics
        portfolio_return = float((returns_df.mean() * weights).sum())
        cov_matrix = returns_df.cov()
        portfolio_variance = float(weights @ cov_matrix @ weights)
        portfolio_volatility = float(np.sqrt(portfolio_variance))
        
        # Sharpe ratio
        annual_return = portfolio_return * 252  # Annualize
        annual_volatility = portfolio_volatility * np.sqrt(252)
        annual_risk_free = portfolio.risk_free_rate
        
        sharpe_ratio = (
            (annual_return - annual_risk_free) / annual_volatility
            if annual_volatility > 0 else 0
        )
        
        return {
            "holdings": holdings,
            "performance": {
                "daily_return": portfolio_return,
                "annualized_return": annual_return,
                "daily_volatility": portfolio_volatility,
                "annualized_volatility": annual_volatility,
                "sharpe_ratio": float(sharpe_ratio),
                "risk_free_rate": portfolio.risk_free_rate
            },
            "correlation_matrix": returns_df.corr().to_dict(),
            "covariance_matrix": cov_matrix.to_dict(),
            "observations": len(returns_df),
            "date_range": {
                "start": str(prices_df.index.min()),
                "end": str(prices_df.index.max())
            }
        }
    
    except Exception as e:
        logger.error(f"Error in get_portfolio_metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate portfolio metrics"
        )

# ============================================================================
# APPLICATION ROOT
# ============================================================================

@app.get("/", tags=["Root"], summary="API information")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Quant Finance API",
        "version": "1.0.0",
        "description": "Portfolio risk analysis and market data",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "market_data": "/prices",
            "analytics": ["/returns", "/volatility", "/correlation"],
            "risk": ["/drawdown", "/var"],
            "portfolio": "/portfolio-metrics",
            "metadata": ["/available-tickers", "/ticker-info/{ticker}"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Run with: uvicorn app:app --host 0.0.0.0 --port 5000 --reload
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5001,
        log_level="info"
    )