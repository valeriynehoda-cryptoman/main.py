import ccxt
import requests
import os

# Секреты подтягиваются из настроек GitHub
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

exchange = ccxt.binance({'options': {'defaultType': 'future'}})

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=payload)

def scan_market():
    try:
        tickers = exchange.fetch_tickers()
        candidates = []
        
        for symbol, data in tickers.items():
            if ':USDT' in symbol and data['quoteVolume'] > 10_000_000:
                change = data['percentage']
                if -10 <= change <= -2:
                    candidates.append(f"{symbol} ({change}%)")
        
        top_4 = candidates[:4]
        
        if top_4:
            msg = "📊 *УТРЕННИЙ СКАН (08:00 UTC):*\n\n" + "\n".join(top_4)
            send_to_telegram(msg)
        else:
            send_to_telegram("🔍 Сканер прошел: интересных проливов сегодня нет.")
            
    except Exception as e:
        send_to_telegram(f"⚠️ Ошибка бота: {str(e)}")

if name == "main":
    scan_market()
