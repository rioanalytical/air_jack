# Quantitative Finance Flask API

A production-ready Flask API designed for quantitative professionals to access market data and compute meaningful risk metrics for portfolio analysis.

## Features

✓ **OHLCV Data Access** - Raw price data with flexible querying  
✓ **Returns Analysis** - Simple and log returns with statistical summaries  
✓ **Volatility Metrics** - Rolling volatility windows  
✓ **Correlation Analysis** - Multi-ticker correlation & covariance matrices  
✓ **Drawdown Analysis** - Maximum drawdown and drawdown series  
✓ **Value at Risk** - Historical and Gaussian VaR at multiple confidence levels  
✓ **Portfolio Metrics** - Expected return, volatility, Sharpe ratio for weighted portfolios  
✓ **CORS Enabled** - Ready for web-based consumption  

---

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Server runs on `http://localhost:5000`

---

## API Endpoints

### Health & Metadata

#### `GET /health`
System health check.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-21T10:30:00"
}
```

#### `GET /available-tickers`
Get all tickers in the database.

**Response:**
```json
{
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "count": 3
}
```

#### `GET /ticker-info/<ticker>`
Get metadata for a specific ticker.

**Example:** `/ticker-info/AAPL`

**Response:**
```json
{
  "ticker": "AAPL",
  "record_count": 250,
  "earliest_date": "2023-01-01",
  "latest_date": "2024-02-21",
  "avg_volume": 52000000.5
}
```

---

### Basic Data Access

#### `GET /prices`

Get OHLCV data for one or more tickers.

**Query Parameters:**
- `ticker` (required): Comma-separated list (e.g., `AAPL,GOOGL,MSFT`)
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `limit` (optional): Max rows per ticker, default 1000

**Examples:**

```bash
# Last 5 days for single ticker
curl "http://localhost:5000/prices?ticker=AAPL&limit=5"

# Date range for multiple tickers
curl "http://localhost:5000/prices?ticker=AAPL,GOOGL&start_date=2024-01-01&end_date=2024-02-21"
```

**Response:**
```json
{
  "AAPL": {
    "data": [
      {
        "date": "2024-02-20",
        "ticker": "AAPL",
        "open": 182.5,
        "high": 183.2,
        "low": 181.8,
        "close": 182.95,
        "volume": 48500000
      }
    ],
    "count": 20,
    "date_range": {
      "start": "2024-02-01",
      "end": "2024-02-21"
    }
  }
}
```

---

### Returns Analysis

#### `GET /returns`

Calculate simple or log returns with statistical summaries.

**Query Parameters:**
- `ticker` (required): Comma-separated list
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `return_type` (optional): `'simple'` or `'log'`, default `'log'`

**Examples:**

```bash
# Log returns for single ticker
curl "http://localhost:5000/returns?ticker=AAPL"

# Simple returns for multiple tickers
curl "http://localhost:5000/returns?ticker=AAPL,GOOGL&return_type=simple"

# Date range with statistics
curl "http://localhost:5000/returns?ticker=MSFT&start_date=2024-01-01&end_date=2024-02-21"
```

**Response:**
```json
{
  "AAPL": {
    "returns": [0.0045, -0.0032, 0.0089, ...],
    "statistics": {
      "mean": 0.00127,
      "std": 0.0142,
      "min": -0.0485,
      "max": 0.0512,
      "skewness": -0.234,
      "kurtosis": 2.156
    },
    "count": 250
  }
}
```

**Key Metrics:**
- **mean**: Expected daily return
- **std**: Volatility (annualize by √252 for annual)
- **skewness**: Distribution asymmetry (negative = left tail)
- **kurtosis**: Tail risk (>3 = fatter tails than normal)

---

### Volatility Analysis

#### `GET /volatility`

Calculate rolling volatility windows.

**Query Parameters:**
- `ticker` (required): Comma-separated list
- `window` (optional): Rolling window in days, default 20
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD

**Examples:**

```bash
# 20-day rolling volatility
curl "http://localhost:5000/volatility?ticker=AAPL"

# 60-day rolling volatility for multiple tickers
curl "http://localhost:5000/volatility?ticker=AAPL,GOOGL&window=60"

# Date-filtered with custom window
curl "http://localhost:5000/volatility?ticker=MSFT&window=30&start_date=2024-01-01"
```

**Response:**
```json
{
  "AAPL": {
    "volatility": [0.0142, 0.0145, 0.0138, ...],
    "dates": ["2023-02-15", "2023-02-16", ...],
    "statistics": {
      "mean_volatility": 0.0145,
      "current_volatility": 0.0142,
      "min_volatility": 0.0098,
      "max_volatility": 0.0287
    },
    "window_days": 20,
    "count": 230
  }
}
```

**Use Cases:**
- Track volatility regime changes
- Set dynamic position sizing
- Model option pricing

---

### Correlation & Covariance

#### `GET /correlation`

Calculate correlation and covariance between multiple tickers.

**Query Parameters:**
- `tickers` (required): Comma-separated list (minimum 2)
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `return_type` (optional): `'simple'` or `'log'`, default `'log'`

**Examples:**

```bash
# Correlations between 3 stocks
curl "http://localhost:5000/correlation?tickers=AAPL,GOOGL,MSFT"

# Date range correlation
curl "http://localhost:5000/correlation?tickers=AAPL,GOOGL&start_date=2024-01-01&end_date=2024-02-21"

# Using simple returns
curl "http://localhost:5000/correlation?tickers=SPY,TLT,GLD&return_type=simple"
```

**Response:**
```json
{
  "correlation": {
    "AAPL": {"AAPL": 1.0, "GOOGL": 0.62, "MSFT": 0.71},
    "GOOGL": {"AAPL": 0.62, "GOOGL": 1.0, "MSFT": 0.58},
    "MSFT": {"AAPL": 0.71, "GOOGL": 0.58, "MSFT": 1.0}
  },
  "covariance": {
    "AAPL": {"AAPL": 0.000156, "GOOGL": 0.0000892, ...},
    ...
  },
  "tickers": ["AAPL", "GOOGL", "MSFT"],
  "observations": 250,
  "date_range": {
    "start": "2023-02-21",
    "end": "2024-02-21"
  }
}
```

**Use Cases:**
- Portfolio diversification analysis
- Risk decomposition
- Hedging strategy identification
- Factor exposure measurement

---

### Drawdown Analysis

#### `GET /drawdown`

Calculate maximum drawdown and drawdown series.

**Query Parameters:**
- `ticker` (required): Single ticker
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD

**Examples:**

```bash
# Maximum drawdown for stock
curl "http://localhost:5000/drawdown?ticker=AAPL"

# Drawdown over specific period
curl "http://localhost:5000/drawdown?ticker=MSFT&start_date=2023-01-01&end_date=2024-02-21"
```

**Response:**
```json
{
  "ticker": "AAPL",
  "max_drawdown": -0.287,
  "max_drawdown_date": "2022-10-03",
  "recovery_date": "2023-01-09",
  "drawdown_series": [-0.0, -0.015, -0.042, ..., -0.287, ...],
  "dates": ["2023-01-01", "2023-01-02", ...],
  "observation_count": 250
}
```

**Key Metrics:**
- **max_drawdown**: -28.7% = From peak, stock fell 28.7%
- **max_drawdown_date**: When peak-to-trough occurred
- **recovery_date**: When price exceeded previous peak again

**Use Cases:**
- Stress testing
- Risk-adjusted return calculation
- Portfolio resilience analysis

---

### Value at Risk

#### `GET /var`

Calculate Value at Risk at multiple confidence levels.

**Query Parameters:**
- `ticker` (required): Single ticker
- `confidence_levels` (optional): Comma-separated, default `'0.95,0.99'`
- `method` (optional): `'historical'` or `'gaussian'`, default `'historical'`
- `lookback_days` (optional): Historical period to use

**Examples:**

```bash
# Default: 95% and 99% VaR using historical method
curl "http://localhost:5000/var?ticker=AAPL"

# Custom confidence levels
curl "http://localhost:5000/var?ticker=MSFT&confidence_levels=0.90,0.95,0.99"

# Gaussian VaR with 60-day lookback
curl "http://localhost:5000/var?ticker=GOOGL&method=gaussian&lookback_days=60"
```

**Response:**
```json
{
  "ticker": "AAPL",
  "method": "historical",
  "lookback_days": 250,
  "var": {
    "VaR_95": -0.0245,
    "VaR_99": -0.0412
  },
  "expected_return": 0.00127,
  "volatility": 0.0142
}
```

**Interpretation:**
- **VaR_95**: -2.45% = "95% confidence, daily loss won't exceed 2.45%"
- **VaR_99**: -4.12% = "99% confidence, daily loss won't exceed 4.12%"

**Use Cases:**
- Risk limit setting
- Capital adequacy calculation
- Regulatory reporting

---

### Portfolio Metrics

#### `POST /portfolio-metrics`

Calculate comprehensive metrics for a weighted portfolio.

**Request Body:**
```json
{
  "holdings": {
    "AAPL": 0.4,
    "GOOGL": 0.3,
    "MSFT": 0.3
  },
  "start_date": "2024-01-01",
  "end_date": "2024-02-21"
}
```

**Examples:**

```bash
curl -X POST http://localhost:5000/portfolio-metrics \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": {
      "AAPL": 0.4,
      "GOOGL": 0.3,
      "MSFT": 0.3
    }
  }'

# With date range
curl -X POST http://localhost:5000/portfolio-metrics \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": {
      "SPY": 0.6,
      "TLT": 0.3,
      "GLD": 0.1
    },
    "start_date": "2024-01-01",
    "end_date": "2024-02-21"
  }'
```

**Response:**
```json
{
  "holdings": {
    "AAPL": 0.4,
    "GOOGL": 0.3,
    "MSFT": 0.3
  },
  "performance": {
    "expected_return": 0.00156,
    "volatility": 0.01285,
    "sharpe_ratio": 0.1214
  },
  "correlation_matrix": {
    "AAPL": {"AAPL": 1.0, "GOOGL": 0.62, "MSFT": 0.71},
    ...
  },
  "observations": 250,
  "date_range": {
    "start": "2023-02-21",
    "end": "2024-02-21"
  }
}
```

**Key Metrics:**
- **expected_return**: Portfolio's average daily return
- **volatility**: Portfolio's daily volatility (annualize for annual)
- **sharpe_ratio**: Risk-adjusted return (higher is better)
- **correlation_matrix**: Component correlations

**Annualization:**
- Annual return = daily_return × 252
- Annual volatility = daily_volatility × √252
- Annualized Sharpe = daily_sharpe × √252

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Get prices for multiple stocks
response = requests.get(f"{BASE_URL}/prices", params={
    "ticker": "AAPL,GOOGL,MSFT",
    "start_date": "2024-01-01",
    "limit": 20
})
prices = response.json()

# Calculate returns
response = requests.get(f"{BASE_URL}/returns", params={
    "ticker": "AAPL",
    "return_type": "log"
})
returns_data = response.json()
print(f"AAPL annual volatility: {returns_data['AAPL']['statistics']['std'] * (252 ** 0.5):.2%}")

# Correlation analysis
response = requests.get(f"{BASE_URL}/correlation", params={
    "tickers": "AAPL,GOOGL,MSFT"
})
corr_matrix = response.json()

# Portfolio optimization workflow
portfolio = {
    "holdings": {
        "AAPL": 0.4,
        "GOOGL": 0.3,
        "MSFT": 0.3
    }
}

response = requests.post(f"{BASE_URL}/portfolio-metrics", json=portfolio)
portfolio_metrics = response.json()
print(f"Portfolio Sharpe Ratio: {portfolio_metrics['performance']['sharpe_ratio']:.4f}")

# Risk assessment
response = requests.get(f"{BASE_URL}/drawdown", params={"ticker": "AAPL"})
drawdown = response.json()
print(f"Maximum Drawdown: {drawdown['max_drawdown']:.2%}")

response = requests.get(f"{BASE_URL}/var", params={
    "ticker": "AAPL",
    "confidence_levels": "0.95,0.99"
})
var_data = response.json()
print(f"99% VaR: {var_data['var']['VaR_99']:.2%}")
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Invalid parameters
- `404`: Data not found
- `500`: Server error

Error responses:
```json
{
  "error": "Description of what went wrong"
}
```

---

## Best Practices for Quants

1. **Correlation Analysis First**: Use `/correlation` to identify diversification opportunities
2. **Rolling Metrics**: Use `/volatility` with different windows (20, 60, 252) to track regime changes
3. **Drawdown Tracking**: Monitor `/drawdown` in real-time for portfolio stress
4. **VaR for Limits**: Use `/var` to set position sizing limits
5. **Portfolio Optimization**: Iterate with `/portfolio-metrics` to test different weights
6. **Factor Exposure**: Request returns data and perform custom analysis on JSON responses

---

## Performance Notes

- All queries use indexed lookups by ticker and date
- Efficient pandas operations for numerical computations
- Consider caching frequently-accessed correlations (they're slower)
- For large backtests, request longer date ranges in single calls rather than multiple small calls

---

## Extending the API

Add custom endpoints for:
- Fama-French factor exposures
- Options implied volatility
- Realized vs implied volatility comparison
- Custom risk metrics (Sortino, Calmar, Omega)
- Backtesting engine integration
