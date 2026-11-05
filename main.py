import os
import time
import urllib.request
import urllib.parse
import json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SEEN = set()

def get_data(url):
    req = urllib.request.Request(url, headers={"User-Agent": "SolanaScanner/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode())

def send_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(message)
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }).encode()
    req = urllib.request.Request(url, data=data)
    urllib.request.urlopen(req, timeout=20)

def scan():
    tokens = get_data("https://api.dexscreener.com/token-profiles/latest/v1")
    for token in tokens:
        if token.get("chainId") != "solana":
            continue
        address = token.get("tokenAddress")
        if not address or address in SEEN:
            continue
        SEEN.add(address)
        try:
            pairs = get_data(
                f"https://api.dexscreener.com/token-pairs/v1/solana/{address}"
            )
            if not pairs:
                continue
            pair = max(
                pairs,
                key=lambda p: (p.get("liquidity") or {}).get("usd") or 0
            )
            name = pair.get("baseToken", {}).get("name", "Unbekannt")
            symbol = pair.get("baseToken", {}).get("symbol", "?")
            price = pair.get("priceUsd", "unbekannt")
            liquidity = (pair.get("liquidity") or {}).get("usd") or 0
            volume = (pair.get("volume") or {}).get("h24") or 0
            link = pair.get("url", "")
            risk = "RISIKO HOCH" if liquidity < 10000 else "WEITER PRÜFEN"
            message = (
                f"NEUER SOLANA-COIN\n\n"
                f"Name: {name} ({symbol})\n"
                f"Preis: ${price}\n"
                f"Liquidität: ${liquidity:,.0f}\n"
                f"24h Volumen: ${volume:,.0f}\n"
                f"Status: {risk}\n{link}\n\n"
                f"Nur Beobachtung – kein echter Kauf!"
            )
            send_message(message)
        except Exception as error:
            print("Prüfung fehlgeschlagen:", error)

while True:
    try:
        scan()
    except Exception as error:
        print("Scanner-Fehler:", error)
    time.sleep(60)