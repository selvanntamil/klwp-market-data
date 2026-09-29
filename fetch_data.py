import json
import urllib.request

def get_market_data():
    nifty_price = "24,500.00"
    vix_price = "13.50"
    
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/^NSEI?interval=1m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            price = res['chart']['result'][0]['meta']['regularMarketPrice']
            nifty_price = f"{price:,.2f}"
    except Exception as e:
        print(f"Nifty fetch error: {e}")

    try:
        url_vix = "https://query1.finance.yahoo.com/v8/finance/chart/^INDIAVIX?interval=1m&range=1d"
        req_vix = urllib.request.Request(url_vix, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_vix) as response:
            res_vix = json.loads(response.read().decode())
            price_vix = res_vix['chart']['result'][0]['meta']['regularMarketPrice']
            vix_price = f"{price_vix:.2f}"
    except Exception as e:
        print(f"VIX fetch error: {e}")

    pcr = 1.12
    trend_status = "BULLISH"
    
    data = {
        "nifty_spot": nifty_price,
        "india_vix": vix_price,
        "pcr_ratio": str(pcr),
        "max_pain": "24,500",
        "trend": trend_status,
        "status_text": f"NIFTY: {nifty_price} | VIX: {vix_price} | Trend: {trend_status}"
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("data.json updated successfully!")

if __name__ == "__main__":
    get_market_data()
