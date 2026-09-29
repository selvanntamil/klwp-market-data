import json
import urllib.request
import math

def fetch_yahoo_chart(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=5d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())['chart']['result'][0]

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(change if change > 0 else 0)
        losses.append(abs(change) if change < 0 else 0)
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 2)

def calculate_vwap(indicators):
    try:
        closes = indicators['quote'][0]['close']
        volumes = indicators['quote'][0]['volume']
        highs = indicators['quote'][0]['high']
        lows = indicators['quote'][0]['low']
        
        cum_pv, cum_vol = 0, 0
        for i in range(len(closes)):
            if closes[i] is not None and volumes[i] is not None and volumes[i] > 0:
                typical_price = (highs[i] + lows[i] + closes[i]) / 3
                cum_pv += typical_price * volumes[i]
                cum_vol += volumes[i]
        return round(cum_pv / cum_vol, 2) if cum_vol > 0 else 0.0
    except:
        return 0.0

def get_market_data():
    # Default values
    nifty_spot, banknifty_spot, vix_price = 0.0, 0.0, 0.0
    nifty_rsi, banknifty_rsi = 50.0, 50.0
    nifty_vwap, banknifty_vwap = 0.0, 0.0

    # 1. NIFTY 50 Data
    try:
        res = fetch_yahoo_chart("^NSEI")
        closes = [c for c in res['indicators']['quote'][0]['close'] if c is not None]
        nifty_spot = round(res['meta']['regularMarketPrice'], 2)
        nifty_rsi = calculate_rsi(closes)
        nifty_vwap = calculate_vwap(res['indicators'])
    except Exception as e:
        print(f"Nifty Error: {e}")

    # 2. BANKNIFTY Data
    try:
        res = fetch_yahoo_chart("^NSEBANK")
        closes = [c for c in res['indicators']['quote'][0]['close'] if c is not None]
        banknifty_spot = round(res['meta']['regularMarketPrice'], 2)
        banknifty_rsi = calculate_rsi(closes)
        banknifty_vwap = calculate_vwap(res['indicators'])
    except Exception as e:
        print(f"BankNifty Error: {e}")

    # 3. INDIA VIX
    try:
        res = fetch_yahoo_chart("^INDIAVIX")
        vix_price = round(res['meta']['regularMarketPrice'], 2)
    except Exception as e:
        print(f"VIX Error: {e}")

    # Market Structure & Signal Logic
    nifty_signal = "BULLISH" if nifty_spot > nifty_vwap and nifty_rsi > 50 else "BEARISH" if nifty_spot < nifty_vwap and nifty_rsi < 50 else "SIDEWAYS"

    data = {
        "nifty_spot": f"{nifty_spot:,.2f}",
        "nifty_rsi": str(nifty_rsi),
        "nifty_vwap": f"{nifty_vwap:,.2f}",
        "nifty_signal": nifty_signal,
        
        "banknifty_spot": f"{banknifty_spot:,.2f}",
        "banknifty_rsi": str(banknifty_rsi),
        "banknifty_vwap": f"{banknifty_vwap:,.2f}",
        
        "india_vix": str(vix_price),
        "pcr_ratio": "1.08",
        "max_pain": "24,500"
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    get_market_data()
