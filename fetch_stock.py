import requests, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # .env에서 API_KEY 불러오기

API_KEY = os.getenv("API_KEY")
SYMBOL = "AAPL"  # 원하는 종목
README_PATH = "README.md"

URL = (
    f"https://www.alphavantage.co/query?"
    f"function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=1min&apikey={API_KEY}"
)

def fetch_latest_stock():
    """Alpha Vantage에서 최신 1분 시세 가져오기"""
    data = requests.get(URL).json()
    time_series = data.get("Time Series (1min)", {})

    if not time_series:
        return None, "⚠️ 데이터 없음(API 제한 또는 오류)"

    # 가장 최근 시각/가격 추출
    latest_time = sorted(time_series.keys())[-1]
    latest_close = time_series[latest_time]["4. close"]
    return latest_time, latest_close

def update_readme():
    """README.md 파일에 최신 주식 시세 업데이트"""
    latest_time, latest_close = fetch_latest_stock()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if latest_time is None:
        stock_info = "데이터를 가져오지 못했습니다."
    else:
        stock_info = f"{SYMBOL} 최신 시세({latest_time}): ${latest_close}"

    readme_content = f"""
# Stock Price Tracker

이 리포지토리는 Alpha Vantage API를 사용하여 주식 정보를 자동으로 업데이트합니다.

## 최신 주식 시세
> {stock_info}

⏳ 업데이트 시간: {now} (KST)

---
자동 업데이트 봇에 의해 관리됩니다.
"""

    with open(README_PATH, "w", encoding="utf-8") as file:
        file.write(readme_content)
    print("✅ README.md 업데이트 완료!")

if __name__ == "__main__":
    update_readme()
