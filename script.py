import os
import requests

# Legge il token dai Secrets di GitHub che hai appena impostato
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381"

def controlla():
    msg_mic = ""
    msg_roma = ""
    
    # 1. CONTROLLO MINISTERO (MIC)
    try:
        url_mic = "https://www.beniculturali.it/comunicati-ufficiali"
        r_mic = requests.get(url_mic, timeout=15)
        testo_mic = r_mic.text.lower()
        # Cerca le parole chiave per il concorso 1800 posti
        if any(p in testo_mic for p in ["diario", "calendario", "1800", "assistente"]):
            msg_mic = f"🔔 MIC: NOVITÀ RILEVATE! Controlla qui: {url_mic}"
        else:
            msg_mic = "✅ MIC: Nessuna novità sui diari oggi."
    except:
        msg_mic = "⚠️ MIC: Errore di collegamento al sito del Ministero."

    # 2. CONTROLLO ROMA
    try:
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r_roma = requests.get(url_roma, headers=headers, timeout=15)
        if r_roma.status_code == 200:
            msg_roma = f"📍 ROMA: Link aggiornato ai concorsi PA: {url_roma}"
        else:
            msg_roma = "⚠️ ROMA: Sito momentaneamente non raggiungibile."
    except:
        msg_roma = "⚠️ ROMA: Errore tecnico nel controllo Roma."

    # 3. INVIO MESSAGGIO UNICO
    testo_finale = f"{msg_mic}\n\n{msg_roma}"
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url_tg, json={"chat_id": CHAT_ID, "text": testo_finale}, timeout=10)
    except:
        print("Errore nell'invio a Telegram")

if __name__ == "__main__":
    controlla()
