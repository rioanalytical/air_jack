# Quantitative Finance API

A production-ready Flask REST API for quantitative professionals to access market data and compute sophisticated portfolio risk metrics. Built for the modern quant workflow.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database with sample data
python init_db.py

# 3. Run the API server
python app.py

# 4. In another terminal, test with the client
python example_client.py
```

The API will be available at `http://localhost:5000`

---

## Project Structure

```
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── init_db.py                  # Database initialization script
├── example_client.py           # Python client with workflow examples
├── API_DOCUMENTATION.md        # Complete API reference
└── market_data.db             # SQLite database (created after init_db.py)
```

---

## Architecture Overview

### Database Schema

```sql
CREATE TABLE stock_prices (
    date TEXT,              -- Date in YYYY-MM-DD format
    ticker TEXT,            -- Stock ticker (e.g., AAPL)
    open REAL,             -- Opening price
    high REAL,             -- High price
    low REAL,              -- Low price
    close REAL,            -- Closing price
    volume INTEGER,        -- Trading volume
    PRIMARY KEY (date, ticker)
);

-- Indexes for fast queries
CREATE INDEX idx_ticker ON stock_prices(ticker);
CREATE INDEX idx_date ON stock_prices(date);
```

### Core Features

**Data Access:**
- Raw OHLCV pricing data with flexible date range queries
- Multi-ticker batch requests for efficiency

**Returns Analysis:**
- Simple and log returns calculation
- Statistical summaries (mean, std, skewness, kurtosis)
- Ideal for performance attribution

**Volatility Metrics:**
- Rolling window volatility (default 20 days)
- Current vs historical volatility regimes
- Volatility clustering detection

**Correlation & Covariance:**
- Multi-asset correlation matrices
- Covariance for portfolio construction
- Diversification opportunity identification

**Risk Metrics:**
- Maximum drawdown analysis with recovery dates
- Value at Risk (VaR) - historical and Gaussian methods
- Tail risk quantification

**Portfolio Analysis:**
- Weighted portfolio return & volatility
- Sharpe ratio calculation
- Component correlation analysis

---

## Key API Endpoints for Quants

### Portfolio Risk Assessment

```bash
# Get portfolio metrics
curl -X POST http://localhost:5000/portfolio-metrics \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": {
      "AAPL": 0.4,
      "GOOGL": 0.3,
      "MSFT": 0.3
    },
    "start_date": "2024-01-01",
    "end_date": "2024-02-21"
  }'
```

### Correlation Analysis

```bash
# Identify diversification opportunities
curl "http://localhost:5000/correlation?tickers=AAPL,GOOGL,MSFT"
```

### Risk Limits

```bash
# Set position limits based on VaR
curl "http://localhost:5000/var?ticker=AAPL&confidence_levels=0.95,0.99"
```

### Stress Testing

```bash
# Test portfolio across different periods
curl "http://localhost:5000/drawdown?ticker=AAPL"
curl "http://localhost:5000/volatility?ticker=AAPL&window=60"
```

---

## Python Client Examples

### Basic Usage

```python
from example_client import QuantDataClient

client = QuantDataClient()

# Get returns
returns = client.get_returns(["AAPL"], return_type="log")
print(returns["AAPL"]["statistics"])

# Portfolio metrics
portfolio = {"AAPL": 0.4, "GOOGL": 0.6}
metrics = client.get_portfolio_metrics(portfolio)
print(metrics["performance"])

# Correlation
corr = client.get_correlation(["AAPL", "GOOGL", "MSFT"])
print(corr["correlation"])
```

### Advanced Workflows

```python
# Workflow: Portfolio Optimization
portfolio = {"AAPL": 0.4, "GOOGL": 0.3, "MSFT": 0.3}
metrics = client.get_portfolio_metrics(portfolio)

perf = metrics["performance"]
annual_return = perf["expected_return"] * 252
annual_vol = perf["volatility"] * np.sqrt(252)
sharpe = perf["sharpe_ratio"] * np.sqrt(252)

print(f"Expected Annual Return: {annual_return:.2%}")
print(f"Annual Volatility:      {annual_vol:.2%}")
print(f"Sharpe Ratio:           {sharpe:.3f}")
```

```python
# Workflow: Risk Monitoring
for ticker in ["AAPL", "GOOGL", "MSFT"]:
    var = client.get_var(ticker, confidence_levels=[0.99])
    dd = client.get_drawdown(ticker)
    vol = client.get_volatility([ticker], window=20)
    
    print(f"{ticker}:")
    print(f"  99% VaR: {var['var']['VaR_99']:.2%}")
    print(f"  Max DD:  {dd['max_drawdown']:.2%}")
    print(f"  Current Vol: {vol[ticker]['statistics']['current_volatility']:.2%}")
```

```python
# Workflow: Correlation-based Diversification
corr = client.get_correlation(["AAPL", "GOOGL", "MSFT", "AMZN"])

# Find pairs with lowest correlation
pairs = []
tickers = ["AAPL", "GOOGL", "MSFT", "AMZN"]
for i in range(len(tickers)):
    for j in range(i+1, len(tickers)):
        correlation = corr["correlation"][tickers[i]][tickers[j]]
        pairs.append((tickers[i], tickers[j], correlation))

pairs.sort(key=lambda x: x[2])
for t1, t2, corr in pairs[:5]:
    print(f"{t1}-{t2}: {corr:.4f}")  # Best diversifiers
```

---

## Performance Characteristics

| Endpoint | Typical Response | Notes |
|----------|-----------------|-------|
| `/prices` | <50ms | Indexed by ticker & date |
| `/returns` | <100ms | Computes on-the-fly, O(n) |
| `/volatility` | <150ms | Rolling window computation |
| `/correlation` | 200-500ms | Covariance matrix, slower |
| `/portfolio-metrics` | 200-400ms | Multiple ticker joins |
| `/var` | <100ms | Percentile calculation |
| `/drawdown` | <100ms | Expanding max calculation |

**Optimization Tips:**
- Request longer date ranges in single calls (better than multiple small requests)
- Cache correlation matrices (they change slowly)
- Use `/volatility` with appropriate windows rather than computing yourself
- Batch ticker requests where possible

---

## Common Quantitative Workflows

### 1. Portfolio Construction
```
1. Get correlation matrix → `/correlation?tickers=...`
2. Identify low-correlation pairs (diversifiers)
3. Calculate metrics for candidate portfolios → `/portfolio-metrics`
4. Select portfolio with best risk-adjusted returns
5. Set position limits based on VaR → `/var?ticker=...`
```

### 2. Risk Monitoring (Daily)
```
1. Update rolling volatility → `/volatility?ticker=...`
2. Calculate portfolio VaR → `/var?ticker=...`
3. Check drawdown status → `/drawdown?ticker=...`
4. Rebalance if thresholds breached
```

### 3. Performance Attribution
```
1. Get component returns → `/returns?ticker=...`
2. Compare to portfolio returns via `/portfolio-metrics`
3. Analyze return dispersion and correlation changes
4. Adjust allocations if correlations break down
```

### 4. Stress Testing
```
1. Get historical returns → `/returns?ticker=...&start_date=...&end_date=...`
2. Analyze returns in crisis periods
3. Recalculate portfolio metrics in those periods → `/portfolio-metrics?start_date=...`
4. Adjust position sizing for worst-case scenarios
```

### 5. Factor Exposure Analysis
```
1. Get correlation with factor proxies → `/correlation?tickers=STOCK,FACTOR`
2. Calculate beta from correlation and volatility ratio
3. Manage factor concentration in portfolio
```

---

## Data Format Notes

### Dates
- Format: `YYYY-MM-DD`
- Stored as text in SQLite for portability
- Queries are inclusive: `start_date <= date <= end_date`

### Returns
- Log returns: `ln(P_t / P_{t-1})`
- Simple returns: `(P_t - P_{t-1}) / P_{t-1}`
- Both are decimal format (0.05 = 5%)
- Easy to annualize: multiply by 252 for daily data

### Volatility
- Annualized: `daily_vol × √252`
- All metrics are in decimal format
- Rolling window defaults to 20 days (approximately 1 month)

### Correlation & Covariance
- Correlation: -1 to 1 (dimensionless)
- Covariance: variance units squared
- Covariance matrix is symmetric and positive semi-definite

---

## Error Handling

All endpoints return standard HTTP status codes:

```json
// 200 OK
{ "data": [...] }

// 400 Bad Request
{ "error": "Invalid input: missing ticker parameter" }

// 404 Not Found
{ "error": "No data for ticker XYZ" }

// 500 Server Error
{ "error": "Server error: database connection failed" }
```

Always check response status and error field before processing data.

---

## Extending the API

Add custom endpoints easily:

```python
@app.route("/custom-metric", methods=["GET"])
@handle_errors
def custom_metric():
    ticker = request.args.get("ticker")
    # Your computation
    return jsonify(result), 200
```

Common extensions:
- **Fama-French factors**: Request returns, compute exposures
- **Options Greeks**: Price data + volatility → implied vol
- **Realized vs Implied**: Use volatility endpoint + external options data
- **Custom risk metrics**: Sortino ratio, Calmar ratio, Omega
- **Backtesting**: Returns data for strategy simulation

---

## Deployment

For production deployment:

```python
# Change debug=False and use a proper WSGI server
# app.py last line:
if __name__ == "__main__":
    app.run(debug=False, port=5000)

# Use gunicorn for production:
# gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Consider:
- Database connection pooling for high concurrency
- Caching layer (Redis) for frequently accessed correlations
- Database replication for HA
- API rate limiting for fair use
- Authentication/authorization if needed

---

## Testing

Run example workflows:

```bash
python example_client.py
```

This executes 5 complete workflows demonstrating:
1. Single stock analysis
2. Correlation and diversification
3. Portfolio optimization
4. Risk monitoring dashboard
5. Stress testing

---

## Contributing

To add new features:

1. Add endpoint to `app.py` with `@handle_errors` decorator
2. Add query parameter validation
3. Return standardized JSON response
4. Add example to `example_client.py`
5. Update `API_DOCUMENTATION.md`

---

## Common Issues

**"No data for ticker"**
- Ticker may not exist in database
- Check `/available-tickers` endpoint
- Re-run `init_db.py` to populate sample data

**"Insufficient data"**
- Not enough historical prices for requested window
- Increase lookback period or reduce window size
- Returns require at least 2 prices

**"Weights must sum to 1.0"**
- Portfolio allocations don't add up to 100%
- Check sum: `sum(holdings.values())`

**Slow `/correlation` queries**
- Correlation requires joining multiple time series
- Normal for 5+ tickers
- Consider caching results

---

## References

- [Efficient Frontier & Modern Portfolio Theory](https://en.wikipedia.org/wiki/Efficient_frontier)
- [Value at Risk](https://en.wikipedia.org/wiki/Value_at_risk)
- [Volatility Clustering](https://en.wikipedia.org/wiki/Volatility_(finance)#Volatility_clustering)
- [Sharpe Ratio](https://en.wikipedia.org/wiki/Sharpe_ratio)

---

## License

MIT License - Use freely in your projects.

---

## Support

For questions or issues:
1. Check `API_DOCUMENTATION.md` for endpoint details
2. Review `example_client.py` for usage patterns
3. Check error messages in API responses
4. Verify database has data via `/available-tickers`

---

## Next Steps

✓ Start with `example_client.py` to understand workflows  
✓ Integrate `/correlation` into your portfolio construction  
✓ Use `/var` and `/drawdown` for risk monitoring  
✓ Build on `/portfolio-metrics` for optimization  
✓ Extend with custom metrics for your strategy

Happy quantitative analysis! 📊
