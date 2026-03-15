import os
import requests
import time
import random

# Configurazione sicura
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381" 

def controlla():
    msg_mic = ""
    msg_roma = ""
    errori_rilevati = []
    
    # Sessione con parametri avanzati
    session = requests.Session()
    
    # Lista di User-Agent per ruotare in caso di blocco
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]

    def get_with_retry(url, label):
        for i in range(3): # Prova fino a 3 volte
            try:
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Referer': 'https://www.google.it/',
                    'DNT': '1',
                    'Upgrade-Insecure-Requests': '1'
                }
                # Aspetta un tempo casuale tra i tentativi per non sembrare un bot
                if i > 0: time.sleep(random.uniform(2, 5))
                
                response = session.get(url, headers=headers, timeout=30)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print(f"Tentativo {i+1} per {label} fallito: {e}")
        return None

    # 1. CONTROLLO MIC (Ministero della Cultura)
    # Proviamo a passare dalla home prima
    session.get("https://www.beniculturali.it/", timeout=15)
    r_mic = get_with_retry("https://www.beniculturali.it/comunicati-ufficiali", "MIC")
    
    if r_mic:
        testo_mic = r_mic.text.lower()
        if any(p in testo_mic for p in ["diario", "calendario", "1800", "assistente"]):
            msg_mic = "🔔 *MIC: NOVITÀ RILEVATE!*\nhttps://www.beniculturali.it/comunicati-ufficiali"
        else:
            msg_mic = "✅ *MIC:* Nessuna novità sui diari oggi."
    else:
        msg_mic = "⚠️ *MIC:* Il sito continua a bloccare l'accesso automatico."
        errori_rilevati.append("MIC: Persistente Errore 403 o Timeout")

    # 2. CONTROLLO ROMA (Concorsi Pubblici) - Già funzionante
    r_roma = get_with_retry("https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm", "ROMA")
    if r_roma:
        msg_roma = f"📍 *ROMA:* Link aggiornato ai concorsi PA: https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
    else:
        msg_roma = "⚠️ *ROMA:* Accesso negato (Status 403)."
        errori_rilevati.append("ROMA: Errore 403")

    # 3. INVIO
    testo_finale = f"{msg_mic}\n\n{msg_roma}"
    if errori_rilevati:
        testo_finale += "\n\n---\n🛠 *DIAGNOSTICA:* Rilevati blocchi IP."

    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_tg, json={"chat_id": CHAT_ID, "text": testo_finale, "parse_mode": "Markdown"})

if __name__ == "__main__":
    controlla()
