"""
Python client demonstrating portfolio risk analysis using the Flask API
Shows typical workflows for quantitative professionals
"""

import requests
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

class QuantDataClient:
    """Client for consuming quantitative finance API"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def get_prices(self, tickers: List[str], start_date: str = None, 
                   end_date: str = None, limit: int = 1000) -> Dict:
        """Fetch OHLCV data"""
        params = {
            "ticker": ",".join(tickers),
            "limit": limit
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        resp = self.session.get(f"{self.base_url}/prices", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_returns(self, tickers: List[str], return_type: str = "log",
                   start_date: str = None, end_date: str = None) -> Dict:
        """Fetch returns and statistics"""
        params = {
            "ticker": ",".join(tickers),
            "return_type": return_type
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        resp = self.session.get(f"{self.base_url}/returns", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_volatility(self, tickers: List[str], window: int = 20,
                      start_date: str = None, end_date: str = None) -> Dict:
        """Fetch rolling volatility"""
        params = {
            "ticker": ",".join(tickers),
            "window": window
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        resp = self.session.get(f"{self.base_url}/volatility", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_correlation(self, tickers: List[str], return_type: str = "log",
                       start_date: str = None, end_date: str = None) -> Dict:
        """Fetch correlation and covariance"""
        params = {
            "tickers": ",".join(tickers),
            "return_type": return_type
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        resp = self.session.get(f"{self.base_url}/correlation", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_drawdown(self, ticker: str, start_date: str = None, 
                    end_date: str = None) -> Dict:
        """Fetch maximum drawdown"""
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        resp = self.session.get(f"{self.base_url}/drawdown", params={"ticker": ticker, **params})
        resp.raise_for_status()
        return resp.json()
    
    def get_var(self, ticker: str, confidence_levels: List[float] = None,
               method: str = "historical", lookback_days: int = None) -> Dict:
        """Fetch Value at Risk"""
        params = {"ticker": ticker, "method": method}
        if confidence_levels:
            params["confidence_levels"] = ",".join(str(c) for c in confidence_levels)
        if lookback_days:
            params["lookback_days"] = lookback_days
        
        resp = self.session.get(f"{self.base_url}/var", params=params)
        resp.raise_for_status()
        return resp.json()
    
    def get_portfolio_metrics(self, holdings: Dict[str, float],
                             start_date: str = None, end_date: str = None) -> Dict:
        """Calculate portfolio metrics"""
        # Validate weights sum to 1.0
        weight_sum = sum(holdings.values())
        if not (0.99 <= weight_sum <= 1.01):
            raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")
        
        payload = {"holdings": holdings}
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        
        resp = self.session.post(f"{self.base_url}/portfolio-metrics", json=payload)
        resp.raise_for_status()
        return resp.json()
    
    def get_available_tickers(self) -> List[str]:
        """Get all available tickers"""
        resp = self.session.get(f"{self.base_url}/available-tickers")
        resp.raise_for_status()
        return resp.json()["tickers"]


# ============================================================================
# EXAMPLE WORKFLOWS
# ============================================================================

def workflow_1_basic_analysis():
    """Workflow 1: Basic returns and volatility analysis"""
    print("\n" + "="*70)
    print("WORKFLOW 1: Single Stock Analysis")
    print("="*70)
    
    client = QuantDataClient()
    
    # Get returns statistics
    returns_data = client.get_returns(["AAPL"], return_type="log")
    stats = returns_data["AAPL"]["statistics"]
    
    # Annualize metrics
    annual_return = stats["mean"] * 252
    annual_vol = stats["std"] * np.sqrt(252)
    
    print(f"\nAAPL Returns Analysis:")
    print(f"  Daily Return:    {stats['mean']:>8.4%}")
    print(f"  Annual Return:   {annual_return:>8.4%}")
    print(f"  Daily Volatility:{stats['std']:>8.4%}")
    print(f"  Annual Volatility: {annual_vol:>7.4%}")
    print(f"  Skewness:        {stats['skewness']:>8.4f}")
    print(f"  Kurtosis:        {stats['kurtosis']:>8.4f}")
    
    # Get current volatility regime
    vol_data = client.get_volatility(["AAPL"], window=20)
    vol_stats = vol_data["AAPL"]["statistics"]
    
    print(f"\n20-Day Rolling Volatility:")
    print(f"  Current:         {vol_stats['current_volatility']:>8.4%}")
    print(f"  Average:         {vol_stats['mean_volatility']:>8.4%}")
    print(f"  Range:           [{vol_stats['min_volatility']:.4%}, {vol_stats['max_volatility']:.4%}]")
    
    # Get drawdown
    dd_data = client.get_drawdown("AAPL")
    print(f"\nDrawdown Analysis:")
    print(f"  Max Drawdown:    {dd_data['max_drawdown']:>8.2%}")
    print(f"  Date:            {dd_data['max_drawdown_date']}")
    print(f"  Recovery:        {dd_data['recovery_date']}")
    
    # Get Value at Risk
    var_data = client.get_var("AAPL", confidence_levels=[0.95, 0.99])
    print(f"\nValue at Risk:")
    print(f"  95% VaR (daily): {var_data['var']['VaR_95']:>8.2%}")
    print(f"  99% VaR (daily): {var_data['var']['VaR_99']:>8.2%}")


def workflow_2_correlation_analysis():
    """Workflow 2: Multi-asset correlation for portfolio construction"""
    print("\n" + "="*70)
    print("WORKFLOW 2: Correlation & Diversification Analysis")
    print("="*70)
    
    client = QuantDataClient()
    tickers = ["AAPL", "GOOGL", "MSFT"]
    
    # Get correlation matrix
    corr_data = client.get_correlation(tickers)
    
    print(f"\nCorrelation Matrix ({', '.join(tickers)}):")
    corr_df = pd.DataFrame(corr_data["correlation"])
    print(corr_df.to_string())
    
    # Identify best diversification opportunity (lowest correlation)
    print(f"\nDiversification Opportunities:")
    correlations = []
    for i, t1 in enumerate(tickers):
        for t2 in tickers[i+1:]:
            corr = corr_data["correlation"][t1][t2]
            correlations.append((t1, t2, corr))
    
    correlations.sort(key=lambda x: x[2])
    for t1, t2, corr in correlations:
        print(f"  {t1}-{t2}: {corr:.4f}")
    
    # Individual volatilities
    returns_data = client.get_returns(tickers, return_type="log")
    print(f"\nIndividual Volatilities:")
    for ticker in tickers:
        vol = returns_data[ticker]["statistics"]["std"] * np.sqrt(252)
        print(f"  {ticker}: {vol:.4%}")


def workflow_3_portfolio_optimization():
    """Workflow 3: Portfolio risk metrics and optimization"""
    print("\n" + "="*70)
    print("WORKFLOW 3: Portfolio Optimization")
    print("="*70)
    
    client = QuantDataClient()
    
    # Test different portfolio allocations
    portfolios = [
        ("Equal Weight", {"AAPL": 0.33, "GOOGL": 0.33, "MSFT": 0.34}),
        ("Tech Heavy", {"AAPL": 0.5, "GOOGL": 0.3, "MSFT": 0.2}),
        ("Balanced", {"AAPL": 0.4, "GOOGL": 0.35, "MSFT": 0.25}),
    ]
    
    print("\nPortfolio Comparison:")
    print(f"{'Portfolio':<15} {'Return':<10} {'Volatility':<12} {'Sharpe':<8}")
    print("-" * 45)
    
    for name, holdings in portfolios:
        metrics = client.get_portfolio_metrics(holdings)
        perf = metrics["performance"]
        
        annual_ret = perf["expected_return"] * 252
        annual_vol = perf["volatility"] * np.sqrt(252)
        sharpe = perf["sharpe_ratio"] * np.sqrt(252)
        
        print(f"{name:<15} {annual_ret:>7.2%}    {annual_vol:>9.2%}    {sharpe:>6.3f}")
    
    # Detailed analysis of best portfolio
    print(f"\nDetailed Analysis: Equal Weight Portfolio")
    metrics = client.get_portfolio_metrics(portfolios[0][1])
    
    print(f"  Expected Daily Return: {metrics['performance']['expected_return']:.4%}")
    print(f"  Daily Volatility:      {metrics['performance']['volatility']:.4%}")
    print(f"  Sharpe Ratio:          {metrics['performance']['sharpe_ratio']:.4f}")
    
    print(f"\n  Correlation Matrix:")
    corr_df = pd.DataFrame(metrics["correlation_matrix"])
    print(corr_df.to_string())


def workflow_4_risk_monitoring():
    """Workflow 4: Real-time risk monitoring"""
    print("\n" + "="*70)
    print("WORKFLOW 4: Risk Monitoring Dashboard")
    print("="*70)
    
    client = QuantDataClient()
    portfolio = {"AAPL": 0.4, "GOOGL": 0.3, "MSFT": 0.3}
    
    print(f"\nPortfolio: {portfolio}")
    print("\n" + "-"*70)
    
    # Individual risk metrics
    tickers = list(portfolio.keys())
    print("\nComponent Risk Metrics:")
    print(f"{'Ticker':<8} {'Annual Vol':<12} {'Max DD':<10} {'99% VaR':<10}")
    print("-" * 40)
    
    for ticker in tickers:
        vol_data = client.get_volatility([ticker], window=20)
        vol = vol_data[ticker]["statistics"]["current_volatility"] * np.sqrt(252)
        
        dd_data = client.get_drawdown(ticker)
        max_dd = dd_data["max_drawdown"]
        
        var_data = client.get_var(ticker, confidence_levels=[0.99])
        var_99 = var_data["var"]["VaR_99"]
        
        print(f"{ticker:<8} {vol:>10.2%}  {max_dd:>8.2%}  {var_99:>8.2%}")
    
    # Portfolio metrics
    portfolio_metrics = client.get_portfolio_metrics(portfolio)
    perf = portfolio_metrics["performance"]
    
    print(f"\nPortfolio Metrics:")
    print(f"  Annual Return:   {perf['expected_return'] * 252:>8.2%}")
    print(f"  Annual Volatility: {perf['volatility'] * np.sqrt(252):>7.2%}")
    print(f"  Sharpe Ratio:    {perf['sharpe_ratio'] * np.sqrt(252):>8.4f}")


def workflow_5_stress_testing():
    """Workflow 5: Stress testing different market conditions"""
    print("\n" + "="*70)
    print("WORKFLOW 5: Stress Testing")
    print("="*70)
    
    client = QuantDataClient()
    portfolio = {"AAPL": 0.5, "GOOGL": 0.5}
    
    # Test portfolio in different volatility regimes
    print(f"\nPortfolio: {portfolio}")
    print("\nPerformance Under Different Volatility Regimes:")
    print(f"{'Regime':<15} {'Daily Vol':<12} {'Annual Vol':<12} {'Sharpe':<8}")
    print("-" * 47)
    
    vol_periods = [
        ("Low Vol Period", "2024-01-01", "2024-01-31"),
        ("High Vol Period", "2024-02-01", "2024-02-21"),
    ]
    
    for regime_name, start, end in vol_periods:
        try:
            metrics = client.get_portfolio_metrics(portfolio, start_date=start, end_date=end)
            perf = metrics["performance"]
            
            daily_vol = perf["volatility"]
            annual_vol = daily_vol * np.sqrt(252)
            sharpe = perf["sharpe_ratio"] * np.sqrt(252)
            
            print(f"{regime_name:<15} {daily_vol:>10.2%}  {annual_vol:>10.2%}  {sharpe:>6.3f}")
        except Exception as e:
            print(f"{regime_name:<15} Data not available: {str(e)}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("QUANTITATIVE PORTFOLIO ANALYSIS - API CLIENT EXAMPLES")
    print("="*70)
    
    try:
        # Run workflows
        workflow_1_basic_analysis()
        workflow_2_correlation_analysis()
        workflow_3_portfolio_optimization()
        workflow_4_risk_monitoring()
        workflow_5_stress_testing()
        
        print("\n" + "="*70)
        print("✓ All workflows completed successfully!")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("   Make sure the Flask app is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
