import os
import requests

# Dati di configurazione [cite: 46, 107-109]
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381" 

def controlla():
    msg_mic = ""
    msg_roma = ""
    errori_rilevati = []
    
    # Creiamo una sessione per gestire i cookie come un vero browser
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/{q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
    })

    # 1. CONTROLLO MIC (Ministero della Cultura) [cite: 57, 83-85]
    try:
        url_mic = "https://www.beniculturali.it/comunicati-ufficiali"
        # Facciamo una prima richiesta alla home per "prendere i cookie"
        session.get("https://www.beniculturali.it/", timeout=15)
        r_mic = session.get(url_mic, timeout=25)
        r_mic.raise_for_status() 
        testo_mic = r_mic.text.lower()
        
        parole_chiave = ["diario", "calendario", "1800", "assistente"]
        if any(p in testo_mic for p in parole_chiave):
            msg_mic = f"🔔 *MIC: NOVITÀ RILEVATE!*\nControlla qui: {url_mic}"
        else:
            msg_mic = "✅ *MIC:* Nessuna novità sui diari oggi."
    except Exception as e:
        msg_mic = "⚠️ *MIC:* Collegamento ancora bloccato dal server."
        errori_rilevati.append(f"Dettaglio MIC: {type(e).__name__}")

    # 2. CONTROLLO ROMA (Concorsi Pubblici) [cite: 87-93]
    try:
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        r_roma = session.get(url_roma, timeout=25)
        
        if r_roma.status_code == 200:
            msg_roma = f"📍 *ROMA:* Link aggiornato ai concorsi PA: {url_roma}"
        else:
            msg_roma = f"⚠️ *ROMA:* Accesso negato dal sito (Status {r_roma.status_code})."
            errori_rilevati.append(f"Dettaglio ROMA: Status Code {r_roma.status_code}")
    except Exception as e:
        msg_roma = "⚠️ *ROMA:* Errore tecnico nel controllo."
        errori_rilevati.append(f"Dettaglio ROMA: {type(e).__name__}")

    # 3. COMPOSIZIONE E INVIO [cite: 107-109]
    testo_finale = f"{msg_mic}\n\n{msg_roma}"
    if errori_rilevati:
        testo_finale += "\n\n---\n🛠 *REPORT DIAGNOSTICO:*\n" + "\n".join(errori_rilevati)

    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url_tg, json={
            "chat_id": CHAT_ID,
            "text": testo_finale,
            "parse_mode": "Markdown"
        }, timeout=15)
    except:
        print("Errore invio Telegram")

if __name__ == "__main__":
    controlla()
