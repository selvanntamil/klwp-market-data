import json
import yfinance as yf

def get_market_data():
    nifty_price = 0.0
    vix_price = 0.0
    
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        if not nifty.empty:
            nifty_price = round(nifty['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching Nifty: {e}")

    try:
        vix = yf.Ticker("^INDIAVIX").history(period="1d")
        if not vix.empty:
            vix_price = round(vix['Close'].iloc[-1], 2)
    except Exception as e:
        print(f"Error fetching VIX: {e}")

    pcr = 1.12
    trend_status = "BULLISH" if nifty_price > 20000 else "NEUTRAL"
    
    data = {
        "nifty_spot": f"{nifty_price:,.2f}" if nifty_price > 0 else "N/A",
        "india_vix": str(vix_price) if vix_price > 0 else "N/A",
        "pcr_ratio": str(pcr),
        "max_pain": "24,500",
        "trend": trend_status,
        "status_text": f"NIFTY: {nifty_price:,.2f} | VIX: {vix_price} | Trend: {trend_status}"
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("data.json updated successfully!")

if __name__ == "__main__":
    get_market_data()
