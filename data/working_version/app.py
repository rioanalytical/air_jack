"""
Flask API for quantitative finance data and portfolio risk analysis
Designed for quant professionals with meaningful risk metrics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from functools import wraps
import json

app = Flask(__name__)
CORS(app)

DB_PATH = "../market_data.db"


def get_db_connection():
    """Get SQLite connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def handle_errors(f):
    """Decorator for consistent error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({"error": f"Invalid input: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"error": f"Server error: {str(e)}"}), 500
    return decorated_function


def parse_date_param(date_str):
    """Parse date parameter, return None if invalid"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD")


# ============================================================================
# BASIC DATA ENDPOINTS
# ============================================================================

@app.route("/prices", methods=["GET"])
@handle_errors
def get_prices():
    """
    Get OHLCV data for ticker(s) and date range
    
    Query params:
    - ticker: comma-separated list (required)
    - start_date: YYYY-MM-DD (optional)
    - end_date: YYYY-MM-DD (optional)
    - limit: max rows per ticker (optional, default 1000)
    """
    tickers = request.args.get("ticker", "").strip().upper()
    if not tickers:
        return jsonify({"error": "ticker parameter required"}), 400
    
    tickers = [t.strip() for t in tickers.split(",")]
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    limit = request.args.get("limit", 1000, type=int)
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    results = {}
    
    for ticker in tickers:
        query = "SELECT * FROM stock_prices WHERE ticker = ?"
        params = [ticker]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)
        
        df = pd.read_sql(query, conn, params=params)
        if df.empty:
            results[ticker] = {"data": [], "count": 0}
        else:
            df = df.sort_values("date").reset_index(drop=True)
            results[ticker] = {
                "data": df.to_dict(orient="records"),
                "count": len(df),
                "date_range": {
                    "start": df["date"].min(),
                    "end": df["date"].max()
                }
            }
    
    conn.close()
    return jsonify(results), 200


# ============================================================================
# RETURNS & VOLATILITY ENDPOINTS
# ============================================================================

@app.route("/returns", methods=["GET"])
@handle_errors
def get_returns():
    """
    Calculate returns for ticker(s)
    
    Query params:
    - ticker: comma-separated list (required)
    - start_date: YYYY-MM-DD (optional)
    - end_date: YYYY-MM-DD (optional)
    - return_type: 'simple' or 'log' (default 'log')
    """
    tickers = request.args.get("ticker", "").strip().upper()
    if not tickers:
        return jsonify({"error": "ticker parameter required"}), 400
    
    tickers = [t.strip() for t in tickers.split(",")]
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    return_type = request.args.get("return_type", "log").lower()
    
    if return_type not in ["simple", "log"]:
        return jsonify({"error": "return_type must be 'simple' or 'log'"}), 400
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    results = {}
    
    for ticker in tickers:
        query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
        params = [ticker]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = pd.read_sql(query, conn, params=params)
        
        if len(df) < 2:
            results[ticker] = {"error": "Insufficient data", "count": len(df)}
            continue
        
        if return_type == "log":
            returns = np.log(df["close"] / df["close"].shift(1)).dropna()
        else:
            returns = (df["close"].pct_change()).dropna()
        
        results[ticker] = {
            "returns": returns.tolist(),
            "statistics": {
                "mean": float(returns.mean()),
                "std": float(returns.std()),
                "min": float(returns.min()),
                "max": float(returns.max()),
                "skewness": float(returns.skew()),
                "kurtosis": float(returns.kurtosis())
            },
            "count": len(returns)
        }
    
    conn.close()
    return jsonify(results), 200


@app.route("/volatility", methods=["GET"])
@handle_errors
def get_volatility():
    """
    Calculate rolling volatility for ticker(s)
    
    Query params:
    - ticker: comma-separated list (required)
    - window: rolling window in days (default 20)
    - start_date: YYYY-MM-DD (optional)
    - end_date: YYYY-MM-DD (optional)
    """
    tickers = request.args.get("ticker", "").strip().upper()
    if not tickers:
        return jsonify({"error": "ticker parameter required"}), 400
    
    tickers = [t.strip() for t in tickers.split(",")]
    window = request.args.get("window", 20, type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    if window < 2:
        return jsonify({"error": "window must be >= 2"}), 400
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    results = {}
    
    for ticker in tickers:
        query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
        params = [ticker]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = pd.read_sql(query, conn, params=params)
        
        if len(df) < window + 1:
            results[ticker] = {"error": f"Insufficient data (need {window + 1} days)"}
            continue
        
        returns = np.log(df["close"] / df["close"].shift(1)).dropna()
        rolling_vol = returns.rolling(window=window).std()
        
        results[ticker] = {
            "volatility": rolling_vol.tolist(),
            "dates": df["date"].iloc[window:].tolist(),
            "statistics": {
                "mean_volatility": float(rolling_vol.mean()),
                "current_volatility": float(rolling_vol.iloc[-1]),
                "min_volatility": float(rolling_vol.min()),
                "max_volatility": float(rolling_vol.max())
            },
            "window_days": window,
            "count": len(rolling_vol)
        }
    
    conn.close()
    return jsonify(results), 200


# ============================================================================
# CORRELATION & COVARIANCE ENDPOINTS
# ============================================================================

@app.route("/correlation", methods=["GET"])
@handle_errors
def get_correlation():
    """
    Calculate correlation matrix between multiple tickers
    
    Query params:
    - tickers: comma-separated list (required, minimum 2)
    - start_date: YYYY-MM-DD (optional)
    - end_date: YYYY-MM-DD (optional)
    - return_type: 'simple' or 'log' (default 'log')
    """
    tickers_param = request.args.get("tickers", "").strip().upper()
    if not tickers_param:
        return jsonify({"error": "tickers parameter required (comma-separated)"}), 400
    
    tickers = [t.strip() for t in tickers_param.split(",")]
    
    if len(tickers) < 2:
        return jsonify({"error": "At least 2 tickers required for correlation"}), 400
    
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    return_type = request.args.get("return_type", "log").lower()
    
    if return_type not in ["simple", "log"]:
        return jsonify({"error": "return_type must be 'simple' or 'log'"}), 400
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    price_data = {}
    
    for ticker in tickers:
        query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
        params = [ticker]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = pd.read_sql(query, conn, params=params)
        price_data[ticker] = df.set_index("date")["close"]
    
    conn.close()
    
    # Align all series to common dates
    prices_df = pd.DataFrame(price_data)
    prices_df = prices_df.dropna()
    
    if len(prices_df) < 2:
        return jsonify({"error": "Insufficient overlapping data"}), 400
    
    if return_type == "log":
        returns_df = np.log(prices_df / prices_df.shift(1)).dropna()
    else:
        returns_df = prices_df.pct_change().dropna()
    
    corr_matrix = returns_df.corr()
    cov_matrix = returns_df.cov()
    
    return jsonify({
        "correlation": corr_matrix.to_dict(),
        "covariance": cov_matrix.to_dict(),
        "tickers": tickers,
        "observations": len(returns_df),
        "date_range": {
            "start": prices_df.index.min(),
            "end": prices_df.index.max()
        }
    }), 200


# ============================================================================
# DRAWDOWN & RISK ENDPOINTS
# ============================================================================

@app.route("/drawdown", methods=["GET"])
@handle_errors
def get_drawdown():
    """
    Calculate maximum drawdown and drawdown series
    
    Query params:
    - ticker: single ticker (required)
    - start_date: YYYY-MM-DD (optional)
    - end_date: YYYY-MM-DD (optional)
    """
    ticker = request.args.get("ticker", "").strip().upper()
    if not ticker:
        return jsonify({"error": "ticker parameter required"}), 400
    
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
    params = [ticker]
    
    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    
    query += " ORDER BY date"
    
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    
    if df.empty:
        return jsonify({"error": f"No data for ticker {ticker}"}), 404
    
    # Calculate running maximum and drawdown
    running_max = df["close"].expanding().max()
    drawdown = (df["close"] - running_max) / running_max
    
    max_drawdown = drawdown.min()
    max_dd_idx = drawdown.idxmin()
    recovery_idx = df[df.index > max_dd_idx]["close"][df["close"] > running_max[max_dd_idx]]
    
    recovery_date = None
    if not recovery_idx.empty:
        recovery_date = df.loc[recovery_idx.index[0], "date"]
    
    return jsonify({
        "ticker": ticker,
        "max_drawdown": float(max_drawdown),
        "max_drawdown_date": df.loc[max_dd_idx, "date"],
        "recovery_date": recovery_date,
        "drawdown_series": drawdown.tolist(),
        "dates": df["date"].tolist(),
        "observation_count": len(df)
    }), 200


@app.route("/var", methods=["GET"])
@handle_errors
def get_value_at_risk():
    """
    Calculate Value at Risk (VaR) at different confidence levels
    
    Query params:
    - ticker: single ticker (required)
    - confidence_levels: comma-separated (default '0.95,0.99')
    - method: 'historical' or 'gaussian' (default 'historical')
    - lookback_days: days of history to use (optional)
    """
    ticker = request.args.get("ticker", "").strip().upper()
    if not ticker:
        return jsonify({"error": "ticker parameter required"}), 400
    
    confidence_str = request.args.get("confidence_levels", "0.95,0.99")
    confidence_levels = [float(x.strip()) for x in confidence_str.split(",")]
    method = request.args.get("method", "historical").lower()
    lookback_days = request.args.get("lookback_days", type=int)
    
    if method not in ["historical", "gaussian"]:
        return jsonify({"error": "method must be 'historical' or 'gaussian'"}), 400
    
    conn = get_db_connection()
    query = "SELECT date, close FROM stock_prices WHERE ticker = ? ORDER BY date"
    
    df = pd.read_sql(query, conn, params=[ticker])
    conn.close()
    
    if df.empty:
        return jsonify({"error": f"No data for ticker {ticker}"}), 404
    
    if lookback_days:
        df = df.tail(lookback_days)
    
    returns = np.log(df["close"] / df["close"].shift(1)).dropna()
    
    var_results = {}
    
    for conf in confidence_levels:
        if conf <= 0 or conf >= 1:
            continue
        
        if method == "historical":
            var = np.percentile(returns, (1 - conf) * 100)
        else:  # gaussian
            mean = returns.mean()
            std = returns.std()
            from scipy import stats
            var = stats.norm.ppf(1 - conf) * std + mean
        
        var_results[f"VaR_{int(conf*100)}"] = float(var)
    
    return jsonify({
        "ticker": ticker,
        "method": method,
        "lookback_days": len(returns),
        "var": var_results,
        "expected_return": float(returns.mean()),
        "volatility": float(returns.std())
    }), 200


# ============================================================================
# PORTFOLIO ENDPOINTS
# ============================================================================

@app.route("/portfolio-metrics", methods=["POST"])
@handle_errors
def get_portfolio_metrics():
    """
    Calculate comprehensive portfolio metrics
    
    JSON body:
    {
        "holdings": {
            "TICKER1": 0.4,
            "TICKER2": 0.6
        },
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD"
    }
    """
    data = request.get_json()
    if not data or "holdings" not in data:
        return jsonify({"error": "holdings required in request body"}), 400
    
    holdings = data.get("holdings")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    
    if not isinstance(holdings, dict) or not holdings:
        return jsonify({"error": "holdings must be non-empty dict"}), 400
    
    # Validate weights sum to ~1.0
    weight_sum = sum(holdings.values())
    if not (0.99 <= weight_sum <= 1.01):
        return jsonify({"error": f"Weights must sum to 1.0, got {weight_sum}"}), 400
    
    if start_date:
        start_date = parse_date_param(start_date).strftime("%Y-%m-%d")
    if end_date:
        end_date = parse_date_param(end_date).strftime("%Y-%m-%d")
    
    conn = get_db_connection()
    price_data = {}
    
    for ticker in holdings.keys():
        query = "SELECT date, close FROM stock_prices WHERE ticker = ?"
        params = [ticker.upper()]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = pd.read_sql(query, conn, params=params)
        if df.empty:
            conn.close()
            return jsonify({"error": f"No data for ticker {ticker}"}), 404
        
        price_data[ticker.upper()] = df.set_index("date")["close"]
    
    conn.close()
    
    # Align all series
    prices_df = pd.DataFrame(price_data)
    prices_df = prices_df.dropna()
    
    if len(prices_df) < 2:
        return jsonify({"error": "Insufficient overlapping data"}), 400
    
    # Calculate returns
    returns_df = np.log(prices_df / prices_df.shift(1)).dropna()
    
    # Portfolio weights
    weights = np.array([holdings[ticker.upper()] for ticker in holdings.keys()])
    
    # Portfolio return and volatility
    portfolio_return = float((returns_df.mean() * weights).sum())
    cov_matrix = returns_df.cov()
    portfolio_variance = float(weights @ cov_matrix @ weights)
    portfolio_volatility = float(np.sqrt(portfolio_variance))
    
    # Sharpe ratio (assuming 0% risk-free rate)
    sharpe_ratio = float(portfolio_return / portfolio_volatility) if portfolio_volatility > 0 else 0
    
    return jsonify({
        "holdings": holdings,
        "performance": {
            "expected_return": portfolio_return,
            "volatility": portfolio_volatility,
            "sharpe_ratio": sharpe_ratio
        },
        "correlation_matrix": returns_df.corr().to_dict(),
        "observations": len(returns_df),
        "date_range": {
            "start": prices_df.index.min(),
            "end": prices_df.index.max()
        }
    }), 200


# ============================================================================
# HEALTH & METADATA
# ============================================================================

@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200


@app.route("/available-tickers", methods=["GET"])
@handle_errors
def available_tickers():
    """Get all tickers in database"""
    conn = get_db_connection()
    query = "SELECT DISTINCT ticker FROM stock_prices ORDER BY ticker"
    df = pd.read_sql(query, conn)
    conn.close()
    
    return jsonify({
        "tickers": df["ticker"].tolist(),
        "count": len(df)
    }), 200


@app.route("/ticker-info/<ticker>", methods=["GET"])
@handle_errors
def ticker_info(ticker):
    """Get metadata about a ticker"""
    ticker = ticker.upper()
    conn = get_db_connection()
    
    query = """
    SELECT 
        COUNT(*) as record_count,
        MIN(date) as earliest_date,
        MAX(date) as latest_date,
        AVG(volume) as avg_volume
    FROM stock_prices WHERE ticker = ?
    """
    
    df = pd.read_sql(query, conn, params=[ticker])
    conn.close()
    
    if df.empty or df["record_count"].iloc[0] == 0:
        return jsonify({"error": f"No data for ticker {ticker}"}), 404
    
    return jsonify({
        "ticker": ticker,
        "record_count": int(df["record_count"].iloc[0]),
        "earliest_date": df["earliest_date"].iloc[0],
        "latest_date": df["latest_date"].iloc[0],
        "avg_volume": float(df["avg_volume"].iloc[0])
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
