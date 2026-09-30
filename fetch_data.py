import json
import urllib.request

def get_symbol_data(symbol):
    price = 0.0
    change_str = "+0.00"
    rsi = 50.0
    vwap = 0.0
    
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode())['chart']['result'][0]
            
            if 'regularMarketPrice' in res['meta']:
                price = round(res['meta']['regularMarketPrice'], 2)
            
            prev_close = res['meta'].get('chartPreviousClose', price)
            if prev_close and price > 0:
                chg = round(price - prev_close, 2)
                change_str = f"+{chg}" if chg >= 0 else str(chg)
                
            quote = res['indicators']['quote'][0]
            closes = [c for c in quote.get('close', []) if c is not None]
            highs = [h for h in quote.get('high', []) if h is not None]
            lows = [l for l in quote.get('low', []) if l is not None]
            volumes = [v for v in quote.get('volume', []) if v is not None]

            if len(closes) > 0:
                if price == 0.0:
                    price = round(closes[-1], 2)
                    
                if len(closes) >= 14:
                    gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
                    losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
                    avg_gain = sum(gains[-14:]) / 14
                    avg_loss = sum(losses[-14:]) / 14
                    if avg_loss > 0:
                        rs = avg_gain / avg_loss
                        rsi = round(100 - (100 / (1 + rs)), 2)
                    elif avg_gain > 0:
                        rsi = 100.0

                cum_pv, cum_vol = 0, 0
                min_len = min(len(closes), len(highs), len(lows), len(volumes))
                for i in range(min_len):
                    tp = (highs[i] + lows[i] + closes[i]) / 3
                    cum_pv += tp * volumes[i]
                    cum_vol += volumes[i]
                if cum_vol > 0:
                    vwap = round(cum_pv / cum_vol, 2)
                    
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

    return price, change_str, rsi, vwap

def get_market_data():
    nifty_price, nifty_change, nifty_rsi, nifty_vwap = get_symbol_data("^NSEI")
    bank_price, bank_change, bank_rsi, bank_vwap = get_symbol_data("^NSEBANK")
    sensex_price, sensex_change, sensex_rsi, sensex_vwap = get_symbol_data("^BSESN")
    vix_price, _, _, _ = get_symbol_data("^INDIAVIX")
    
    # GIFT NIFTY Data (NSE International Exchange)
    gift_price, gift_change, _, _ = get_symbol_data("NIFTY_FIN.NS")

    nifty_sig = "BULLISH" if nifty_price > nifty_vwap and nifty_rsi > 50 else "BEARISH" if nifty_price < nifty_vwap and nifty_rsi < 50 else "SIDEWAYS"
    sensex_sig = "BULLISH" if sensex_price > sensex_vwap and sensex_rsi > 50 else "BEARISH" if sensex_price < sensex_vwap and sensex_rsi < 50 else "SIDEWAYS"

    data = {
        "nifty_spot": f"{nifty_price:,.2f}" if nifty_price > 0 else "N/A",
        "nifty_change": nifty_change,
        "nifty_rsi": str(nifty_rsi),
        "nifty_vwap": f"{nifty_vwap:,.2f}" if nifty_vwap > 0 else "N/A",
        "nifty_signal": nifty_sig,
        
        "gift_nifty": f"{gift_price:,.2f}" if gift_price > 0 else "N/A",
        "gift_change": gift_change,
        
        "banknifty_spot": f"{bank_price:,.2f}" if bank_price > 0 else "N/A",
        "banknifty_change": bank_change,
        "banknifty_rsi": str(bank_rsi),
        "banknifty_vwap": f"{bank_vwap:,.2f}" if bank_vwap > 0 else "N/A",

        "sensex_spot": f"{sensex_price:,.2f}" if sensex_price > 0 else "N/A",
        "sensex_change": sensex_change,
        "sensex_rsi": str(sensex_rsi),
        "sensex_vwap": f"{sensex_vwap:,.2f}" if sensex_vwap > 0 else "N/A",
        "sensex_signal": sensex_sig,
        
        "india_vix": str(vix_price) if vix_price > 0 else "N/A"
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("data.json updated successfully!")

if __name__ == "__main__":
    get_market_data()
