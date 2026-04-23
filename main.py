import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import yfinance as yf

app = FastAPI()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>나이스정보통신 실시간 주가</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script>
            async function updatePrice() {
                try {
                    const response = await fetch('/api/price');
                    const data = await response.json();
                    document.getElementById('price').innerText = data.price.toLocaleString() + ' 원';
                    document.getElementById('change').innerText = data.change_percent.toFixed(2) + '%';
                    
                    const changeElem = document.getElementById('change');
                    if (data.change_percent > 0) {
                        changeElem.style.color = '#ff4d4d';
                    } else if (data.change_percent < 0) {
                        changeElem.style.color = '#4d79ff';
                    } else {
                        changeElem.style.color = '#333';
                    }
                    
                    document.getElementById('time').innerText = "최근 업데이트: " + new Date().toLocaleTimeString();
                } catch (error) {
                    console.error("데이터를 가져오는 중 오류 발생:", error);
                }
            }
            setInterval(updatePrice, 10000);
            window.onload = updatePrice;
        </script>
        <style>
            body { font-family: 'Apple SD Gothic Neo', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f5f7fa; }
            .card { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; width: 300px; }
            h1 { font-size: 1.2rem; color: #666; margin-bottom: 0.5rem; }
            .price { font-size: 2.5rem; font-weight: bold; margin: 10px 0; color: #222; }
            .change { font-size: 1.1rem; font-weight: 600; }
            .time { font-size: 0.8rem; color: #999; margin-top: 1.5rem; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>나이스정보통신 (036800)</h1>
            <div id="price" class="price">불러오는 중...</div>
            <div id="change" class="change">0.00%</div>
            <div id="time" class="time"></div>
        </div>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE

@app.get("/api/price")
async def get_price():
    stock = yf.Ticker("036800.KQ")
    data = stock.history(period="1d")
    
    if not data.empty:
        current_price = data['Close'].iloc[-1]
        prev_close = stock.info.get('previousClose', current_price)
        change_percent = ((current_price - prev_close) / prev_close) * 100
        
        return {
            "price": int(current_price),
            "change_percent": change_percent
        }
    return {"error": "데이터를 불러올 수 없습니다."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)