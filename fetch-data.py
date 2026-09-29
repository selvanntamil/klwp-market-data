import json
import yfinance as yf

def get_market_data():
    try:
        nifty = yf.Ticker("^NSEI").history(period="1d")
        vix = yf.Ticker("^INDIAVIX").history(period="1d")
        
        nifty_price = round(nifty['Close'].iloc[-1], 2) if not nifty.empty else 0.0
        vix_price = round(vix['Close'].iloc[-1], 2) if not vix.empty else 0.0

        pcr = 1.12
        trend_status = "BULLISH" if nifty_price > 24000 else "BEARISH"
        
        data = {
            "nifty_spot": f"{nifty_price:,.2f}",
            "india_vix": str(vix_price),
            "pcr_ratio": str(pcr),
            "max_pain": "24,500",
            "trend": trend_status,
            "status_text": f"NIFTY: {nifty_price:,.2f} | VIX: {vix_price} | Trend: {trend_status}"
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print("data.json updated successfully!")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    get_market_data()
