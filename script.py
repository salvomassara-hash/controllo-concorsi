import os
import requests

# Recupero sicuro dei segreti
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381" 

def controlla():
    msg_mic = ""
    msg_roma = ""
    errori_rilevati = []
    
    # Simuliamo un browser reale (Chrome su Windows) per evitare il blocco 403
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # 1. CONTROLLO MIC (Ministero della Cultura)
    try:
        url_mic = "https://www.beniculturali.it/comunicati-ufficiali"
        r_mic = requests.get(url_mic, headers=headers, timeout=25)
        r_mic.raise_for_status() 
        testo_mic = r_mic.text.lower()
        
        if any(p in testo_mic for p in ["diario", "calendario", "1800", "assistente"]):
            msg_mic = f"🔔 *MIC: NOVITÀ RILEVATE!*\nControlla qui: {url_mic}"
        else:
            msg_mic = "✅ *MIC:* Nessuna novità sui diari oggi."
    except Exception as e:
        msg_mic = "⚠️ *MIC:* Errore tecnico nel collegamento."
        errori_rilevati.append(f"Dettaglio MIC: {type(e).__name__}")

    # 2. CONTROLLO ROMA (Concorsi Pubblici)
    try:
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        r_roma = requests.get(url_roma, headers=headers, timeout=25)
        
        if r_roma.status_code == 200:
            msg_roma = f"📍 *ROMA:* Link aggiornato ai concorsi PA: {url_roma}"
        else:
            msg_roma = f"⚠️ *ROMA:* Sito momentaneamente bloccato (Status {r_roma.status_code})."
            errori_rilevati.append(f"Dettaglio ROMA: Status Code {r_roma.status_code}")
    except Exception as e:
        msg_roma = "⚠️ *ROMA:* Errore tecnico nel controllo."
        errori_rilevati.append(f"Dettaglio ROMA: {type(e).__name__}")

    # 3. INVIO MESSAGGIO CON FORMATTAZIONE
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
