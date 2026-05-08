#!/usr/bin/env python3
"""Generate realistic demo data for the dashboard."""
import json
from pathlib import Path

data = {
  "last_updated": "2026-05-08 01:02 UTC",
  "benchmarks": {
    "S&P 500":      {"ytd": 3.24,  "ret_1y": 14.82, "price": 5312.41},
    "NASDAQ":       {"ytd": 4.87,  "ret_1y": 19.63, "price": 16723.05},
    "Dow Jones":    {"ytd": 1.93,  "ret_1y": 11.24, "price": 39247.33},
    "Russell 2000": {"ytd": -1.42, "ret_1y": 6.73,  "price": 2014.55}
  },
  "institutions": [
    {
      "rank": 1,
      "name": "Renaissance Technologies",
      "type": "Quant Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 32.14, "ret_1m": 5.82, "ret_6m": 19.43, "ret_1y": 47.61, "coverage": 91.0},
      "top_holdings": [
        {"ticker": "IWM",  "ytd": 8.3,   "ret_1y": 12.4, "price": 198.45, "weight_pct": 10.0},
        {"ticker": "SPY",  "ytd": 3.2,   "ret_1y": 14.8, "price": 529.41, "weight_pct": 10.0},
        {"ticker": "QQQ",  "ytd": 4.9,   "ret_1y": 19.6, "price": 447.23, "weight_pct": 10.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 10.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 10.0},
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 10.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 10.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 10.0},
        {"ticker": "GLD",  "ytd": 14.2,  "ret_1y": 21.8, "price": 224.56, "weight_pct": 10.0},
        {"ticker": "EEM",  "ytd": 6.4,   "ret_1y": 9.2,  "price": 42.18,  "weight_pct": 10.0}
      ]
    },
    {
      "rank": 2,
      "name": "Citadel Advisors",
      "type": "Multi-Strategy",
      "holding_count": 10,
      "portfolio_return": {"ytd": 28.93, "ret_1m": 4.71, "ret_6m": 16.82, "ret_1y": 41.24, "coverage": 88.0},
      "top_holdings": [
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 15.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 12.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 11.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 10.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 10.0},
        {"ticker": "TSLA", "ytd": -18.4, "ret_1y": -12.3,"price": 162.48, "weight_pct": 9.0},
        {"ticker": "AMD",  "ytd": 22.1,  "ret_1y": 38.7, "price": 172.34, "weight_pct": 9.0},
        {"ticker": "AVGO", "ytd": 31.2,  "ret_1y": 52.4, "price": 1423.56,"weight_pct": 8.0},
        {"ticker": "ORCL", "ytd": 24.7,  "ret_1y": 42.3, "price": 127.89, "weight_pct": 8.0},
        {"ticker": "CRM",  "ytd": 16.3,  "ret_1y": 28.9, "price": 298.45, "weight_pct": 8.0}
      ]
    },
    {
      "rank": 3,
      "name": "Coatue Management",
      "type": "Tech Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 24.17, "ret_1m": 3.94, "ret_6m": 14.21, "ret_1y": 38.56, "coverage": 85.0},
      "top_holdings": [
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 18.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 14.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 12.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 11.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 10.0},
        {"ticker": "TSLA", "ytd": -18.4, "ret_1y": -12.3,"price": 162.48, "weight_pct": 8.0},
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 8.0},
        {"ticker": "AMD",  "ytd": 22.1,  "ret_1y": 38.7, "price": 172.34, "weight_pct": 7.0},
        {"ticker": "SNOW", "ytd": -8.3,  "ret_1y": -14.2,"price": 139.45, "weight_pct": 6.0},
        {"ticker": "UBER", "ytd": 18.6,  "ret_1y": 34.1, "price": 74.23,  "weight_pct": 6.0}
      ]
    },
    {
      "rank": 4,
      "name": "Tiger Global Management",
      "type": "Tech Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 21.84, "ret_1m": 3.21, "ret_6m": 12.44, "ret_1y": 34.71, "coverage": 83.0},
      "top_holdings": [
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 16.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 14.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 13.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 12.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 11.0},
        {"ticker": "UBER", "ytd": 18.6,  "ret_1y": 34.1, "price": 74.23,  "weight_pct": 9.0},
        {"ticker": "SNOW", "ytd": -8.3,  "ret_1y": -14.2,"price": 139.45, "weight_pct": 8.0},
        {"ticker": "SHOP", "ytd": 12.9,  "ret_1y": 22.4, "price": 74.56,  "weight_pct": 7.0},
        {"ticker": "SQ",   "ytd": -4.2,  "ret_1y": -8.1, "price": 62.34,  "weight_pct": 6.0},
        {"ticker": "COIN", "ytd": 31.4,  "ret_1y": 58.2, "price": 214.78, "weight_pct": 4.0}
      ]
    },
    {
      "rank": 5,
      "name": "Two Sigma Investments",
      "type": "Quant Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 18.52, "ret_1m": 2.84, "ret_6m": 10.93, "ret_1y": 29.84, "coverage": 79.0},
      "top_holdings": [
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 13.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 12.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 11.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 10.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 10.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 9.0},
        {"ticker": "BRK-B","ytd": 11.4,  "ret_1y": 19.8, "price": 401.23, "weight_pct": 9.0},
        {"ticker": "LLY",  "ytd": 28.3,  "ret_1y": 47.6, "price": 832.45, "weight_pct": 8.0},
        {"ticker": "UNH",  "ytd": 4.2,   "ret_1y": 8.1,  "price": 512.34, "weight_pct": 9.0},
        {"ticker": "JPM",  "ytd": 14.8,  "ret_1y": 26.3, "price": 198.74, "weight_pct": 9.0}
      ]
    },
    {
      "rank": 6,
      "name": "D.E. Shaw & Co",
      "type": "Quant Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 16.74, "ret_1m": 2.41, "ret_6m": 9.82, "ret_1y": 27.43, "coverage": 81.0},
      "top_holdings": [
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 12.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 11.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 10.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 10.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 9.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 9.0},
        {"ticker": "TSLA", "ytd": -18.4, "ret_1y": -12.3,"price": 162.48, "weight_pct": 8.0},
        {"ticker": "BRK-B","ytd": 11.4,  "ret_1y": 19.8, "price": 401.23, "weight_pct": 8.0},
        {"ticker": "JPM",  "ytd": 14.8,  "ret_1y": 26.3, "price": 198.74, "weight_pct": 8.0},
        {"ticker": "V",    "ytd": 7.3,   "ret_1y": 14.2, "price": 274.56, "weight_pct": 8.0}
      ]
    },
    {
      "rank": 7,
      "name": "Appaloosa Management",
      "type": "Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 14.32, "ret_1m": 1.98, "ret_6m": 8.41, "ret_1y": 23.87, "coverage": 76.0},
      "top_holdings": [
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 14.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 13.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 12.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 11.0},
        {"ticker": "TSLA", "ytd": -18.4, "ret_1y": -12.3,"price": 162.48, "weight_pct": 10.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 9.0},
        {"ticker": "ORCL", "ytd": 24.7,  "ret_1y": 42.3, "price": 127.89, "weight_pct": 9.0},
        {"ticker": "UBER", "ytd": 18.6,  "ret_1y": 34.1, "price": 74.23,  "weight_pct": 8.0},
        {"ticker": "BIDU", "ytd": 7.4,   "ret_1y": 12.3, "price": 108.45, "weight_pct": 7.0},
        {"ticker": "JD",   "ytd": 14.2,  "ret_1y": 22.1, "price": 31.23,  "weight_pct": 7.0}
      ]
    },
    {
      "rank": 8,
      "name": "Viking Global Investors",
      "type": "Long/Short Equity",
      "holding_count": 10,
      "portfolio_return": {"ytd": 13.18, "ret_1m": 1.74, "ret_6m": 7.82, "ret_1y": 21.43, "coverage": 74.0},
      "top_holdings": [
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 14.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 13.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 12.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 11.0},
        {"ticker": "UNH",  "ytd": 4.2,   "ret_1y": 8.1,  "price": 512.34, "weight_pct": 10.0},
        {"ticker": "V",    "ytd": 7.3,   "ret_1y": 14.2, "price": 274.56, "weight_pct": 9.0},
        {"ticker": "MA",   "ytd": 8.1,   "ret_1y": 16.4, "price": 472.34, "weight_pct": 9.0},
        {"ticker": "JPM",  "ytd": 14.8,  "ret_1y": 26.3, "price": 198.74, "weight_pct": 8.0},
        {"ticker": "HD",   "ytd": 3.4,   "ret_1y": 7.8,  "price": 336.78, "weight_pct": 8.0},
        {"ticker": "CRM",  "ytd": 16.3,  "ret_1y": 28.9, "price": 298.45, "weight_pct": 6.0}
      ]
    },
    {
      "rank": 9,
      "name": "Berkshire Hathaway",
      "type": "Conglomerate",
      "holding_count": 10,
      "portfolio_return": {"ytd": 11.42, "ret_1m": 1.32, "ret_6m": 6.84, "ret_1y": 18.74, "coverage": 95.0},
      "top_holdings": [
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 43.0},
        {"ticker": "BAC",  "ytd": 11.2,  "ret_1y": 19.4, "price": 37.45,  "weight_pct": 9.0},
        {"ticker": "AXP",  "ytd": 18.4,  "ret_1y": 31.2, "price": 228.34, "weight_pct": 8.0},
        {"ticker": "KO",   "ytd": 4.1,   "ret_1y": 7.3,  "price": 62.18,  "weight_pct": 6.0},
        {"ticker": "CVX",  "ytd": 8.3,   "ret_1y": 13.4, "price": 158.45, "weight_pct": 5.0},
        {"ticker": "OXY",  "ytd": 6.4,   "ret_1y": 11.2, "price": 56.78,  "weight_pct": 4.0},
        {"ticker": "MCO",  "ytd": 14.2,  "ret_1y": 24.8, "price": 412.34, "weight_pct": 4.0},
        {"ticker": "KHC",  "ytd": -3.2,  "ret_1y": -6.4, "price": 33.45,  "weight_pct": 3.0},
        {"ticker": "CB",   "ytd": 9.8,   "ret_1y": 17.3, "price": 248.56, "weight_pct": 3.0},
        {"ticker": "DVA",  "ytd": 12.4,  "ret_1y": 21.7, "price": 134.23, "weight_pct": 2.0}
      ]
    },
    {
      "rank": 10,
      "name": "Lone Pine Capital",
      "type": "Long/Short Equity",
      "holding_count": 10,
      "portfolio_return": {"ytd": 10.83, "ret_1m": 1.21, "ret_6m": 6.32, "ret_1y": 17.94, "coverage": 72.0},
      "top_holdings": [
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 16.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 14.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 13.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 12.0},
        {"ticker": "NVDA", "ytd": 78.4,  "ret_1y": 132.1,"price": 891.03, "weight_pct": 11.0},
        {"ticker": "UBER", "ytd": 18.6,  "ret_1y": 34.1, "price": 74.23,  "weight_pct": 9.0},
        {"ticker": "BKNG", "ytd": 9.4,   "ret_1y": 17.2, "price": 3842.34,"weight_pct": 8.0},
        {"ticker": "WDAY", "ytd": -2.4,  "ret_1y": -5.1, "price": 224.56, "weight_pct": 7.0},
        {"ticker": "ZM",   "ytd": -14.3, "ret_1y": -23.4,"price": 58.45,  "weight_pct": 5.0},
        {"ticker": "DDOG", "ytd": 8.2,   "ret_1y": 14.7, "price": 128.34, "weight_pct": 5.0}
      ]
    },
    {
      "rank": 11,
      "name": "Pershing Square Capital",
      "type": "Activist",
      "holding_count": 10,
      "portfolio_return": {"ytd": 9.14, "ret_1m": 0.94, "ret_6m": 5.41, "ret_1y": 15.82, "coverage": 88.0},
      "top_holdings": [
        {"ticker": "HLT",  "ytd": 12.3,  "ret_1y": 21.4, "price": 194.23, "weight_pct": 18.0},
        {"ticker": "QSR",  "ytd": 6.8,   "ret_1y": 12.3, "price": 72.34,  "weight_pct": 15.0},
        {"ticker": "CMG",  "ytd": 8.4,   "ret_1y": 15.2, "price": 3124.56,"weight_pct": 14.0},
        {"ticker": "CP",   "ytd": 4.2,   "ret_1y": 8.7,  "price": 78.45,  "weight_pct": 13.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 12.0},
        {"ticker": "MKL",  "ytd": 7.1,   "ret_1y": 13.4, "price": 1623.45,"weight_pct": 10.0},
        {"ticker": "LOW",  "ytd": 5.4,   "ret_1y": 9.8,  "price": 234.56, "weight_pct": 8.0},
        {"ticker": "NFLX", "ytd": 24.3,  "ret_1y": 42.1, "price": 674.23, "weight_pct": 5.0},
        {"ticker": "NKE",  "ytd": -8.4,  "ret_1y": -14.2,"price": 73.45,  "weight_pct": 3.0},
        {"ticker": "UNH",  "ytd": 4.2,   "ret_1y": 8.1,  "price": 512.34, "weight_pct": 2.0}
      ]
    },
    {
      "rank": 12,
      "name": "Third Point LLC",
      "type": "Activist",
      "holding_count": 10,
      "portfolio_return": {"ytd": 7.82, "ret_1m": 0.71, "ret_6m": 4.32, "ret_1y": 13.41, "coverage": 70.0},
      "top_holdings": [
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 14.0},
        {"ticker": "GOOGL","ytd": 14.3,  "ret_1y": 24.8, "price": 163.21, "weight_pct": 12.0},
        {"ticker": "META", "ytd": 41.2,  "ret_1y": 68.3, "price": 512.89, "weight_pct": 11.0},
        {"ticker": "AMZN", "ytd": 19.8,  "ret_1y": 31.4, "price": 186.42, "weight_pct": 10.0},
        {"ticker": "PG",   "ytd": 5.3,   "ret_1y": 9.8,  "price": 162.34, "weight_pct": 10.0},
        {"ticker": "BABA", "ytd": 22.4,  "ret_1y": 38.7, "price": 78.56,  "weight_pct": 9.0},
        {"ticker": "PYPL", "ytd": -12.4, "ret_1y": -21.3,"price": 58.34,  "weight_pct": 8.0},
        {"ticker": "SLB",  "ytd": 4.2,   "ret_1y": 8.1,  "price": 42.56,  "weight_pct": 8.0},
        {"ticker": "RH",   "ytd": -4.8,  "ret_1y": -9.2, "price": 298.45, "weight_pct": 9.0},
        {"ticker": "TGT",  "ytd": -8.3,  "ret_1y": -14.7,"price": 148.34, "weight_pct": 9.0}
      ]
    },
    {
      "rank": 13,
      "name": "Baupost Group",
      "type": "Value Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 5.43, "ret_1m": 0.42, "ret_6m": 3.14, "ret_1y": 9.82, "coverage": 65.0},
      "top_holdings": [
        {"ticker": "VRTX", "ytd": 18.4,  "ret_1y": 31.2, "price": 432.56, "weight_pct": 14.0},
        {"ticker": "OVV",  "ytd": 6.4,   "ret_1y": 11.2, "price": 42.34,  "weight_pct": 12.0},
        {"ticker": "PBF",  "ytd": -4.2,  "ret_1y": -8.4, "price": 28.45,  "weight_pct": 11.0},
        {"ticker": "EBAY", "ytd": -2.4,  "ret_1y": -4.8, "price": 44.56,  "weight_pct": 11.0},
        {"ticker": "LGND", "ytd": 12.3,  "ret_1y": 21.4, "price": 78.34,  "weight_pct": 10.0},
        {"ticker": "NWSA", "ytd": 4.8,   "ret_1y": 8.7,  "price": 23.45,  "weight_pct": 9.0},
        {"ticker": "QRTE", "ytd": 2.1,   "ret_1y": 4.3,  "price": 14.56,  "weight_pct": 9.0},
        {"ticker": "BKD",  "ytd": -8.4,  "ret_1y": -14.2,"price": 3.45,   "weight_pct": 8.0},
        {"ticker": "NCR",  "ytd": 6.4,   "ret_1y": 11.2, "price": 12.34,  "weight_pct": 8.0},
        {"ticker": "HCA",  "ytd": 9.2,   "ret_1y": 16.4, "price": 312.45, "weight_pct": 8.0}
      ]
    },
    {
      "rank": 14,
      "name": "Bridgewater Associates",
      "type": "Macro Hedge Fund",
      "holding_count": 10,
      "portfolio_return": {"ytd": 4.82, "ret_1m": 0.34, "ret_6m": 2.91, "ret_1y": 8.43, "coverage": 92.0},
      "top_holdings": [
        {"ticker": "SPY",  "ytd": 3.2,   "ret_1y": 14.8, "price": 529.41, "weight_pct": 18.0},
        {"ticker": "VWO",  "ytd": 7.4,   "ret_1y": 13.2, "price": 42.34,  "weight_pct": 14.0},
        {"ticker": "EEM",  "ytd": 6.4,   "ret_1y": 9.2,  "price": 42.18,  "weight_pct": 12.0},
        {"ticker": "GLD",  "ytd": 14.2,  "ret_1y": 21.8, "price": 224.56, "weight_pct": 11.0},
        {"ticker": "TLT",  "ytd": -4.8,  "ret_1y": -8.4, "price": 91.23,  "weight_pct": 10.0},
        {"ticker": "IEF",  "ytd": -2.4,  "ret_1y": -4.2, "price": 94.56,  "weight_pct": 9.0},
        {"ticker": "LQD",  "ytd": -1.8,  "ret_1y": -3.4, "price": 108.34, "weight_pct": 8.0},
        {"ticker": "EFA",  "ytd": 8.4,   "ret_1y": 14.2, "price": 78.45,  "weight_pct": 8.0},
        {"ticker": "IEMG", "ytd": 5.8,   "ret_1y": 9.4,  "price": 52.34,  "weight_pct": 6.0},
        {"ticker": "IAU",  "ytd": 13.8,  "ret_1y": 21.2, "price": 42.12,  "weight_pct": 4.0}
      ]
    },
    {
      "rank": 15,
      "name": "Greenlight Capital",
      "type": "Long/Short Equity",
      "holding_count": 10,
      "portfolio_return": {"ytd": 2.14, "ret_1m": -0.24, "ret_6m": 1.32, "ret_1y": 4.82, "coverage": 68.0},
      "top_holdings": [
        {"ticker": "AAPL", "ytd": 9.1,   "ret_1y": 18.7, "price": 189.30, "weight_pct": 14.0},
        {"ticker": "MSFT", "ytd": 12.4,  "ret_1y": 22.1, "price": 418.74, "weight_pct": 12.0},
        {"ticker": "GM",   "ytd": -2.4,  "ret_1y": -4.8, "price": 43.45,  "weight_pct": 12.0},
        {"ticker": "GOLD", "ytd": 24.3,  "ret_1y": 41.2, "price": 18.45,  "weight_pct": 11.0},
        {"ticker": "CCJ",  "ytd": 12.4,  "ret_1y": 21.8, "price": 48.34,  "weight_pct": 10.0},
        {"ticker": "GOOG", "ytd": 14.3,  "ret_1y": 24.8, "price": 164.34, "weight_pct": 10.0},
        {"ticker": "HCA",  "ytd": 9.2,   "ret_1y": 16.4, "price": 312.45, "weight_pct": 9.0},
        {"ticker": "SWKS", "ytd": -8.4,  "ret_1y": -14.2,"price": 78.34,  "weight_pct": 8.0},
        {"ticker": "STX",  "ytd": 14.2,  "ret_1y": 24.8, "price": 82.34,  "weight_pct": 7.0},
        {"ticker": "NCR",  "ytd": 6.4,   "ret_1y": 11.2, "price": 12.34,  "weight_pct": 7.0}
      ]
    }
  ]
}

out = Path(__file__).parent.parent / "data" / "institutions.json"
out.parent.mkdir(exist_ok=True)
with open(out, "w") as f:
    json.dump(data, f, indent=2)
print(f"✅ Mock data written to {out}")
