import os
import requests

# Recupero sicuro delle credenziali dai Secrets di GitHub
# Il TOKEN non è più scritto in chiaro per evitare revoche automatiche [cite: 46]
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381" # Il tuo ID utente Telegram [cite: 46]

def controlla():
    msg_mic = ""
    msg_roma = ""
    errori_rilevati = []
    
    # 1. CONTROLLO MINISTERO DELLA CULTURA (MIC)
    # Monitoraggio specifico per il concorso 1800 posti [cite: 83, 84]
    try:
        url_mic = "https://www.beniculturali.it/comunicati-ufficiali"
        r_mic = requests.get(url_mic, timeout=20)
        r_mic.raise_for_status()
        testo_mic = r_mic.text.lower()
        
        # Logica di ricerca parole chiave [cite: 84]
        parole_chiave = ["diario", "calendario", "1800", "assistente"]
        if any(p in testo_mic for p in parole_chiave):
            msg_mic = f"🔔 *MIC: NOVITÀ RILEVATE!*\nControlla subito qui: {url_mic}"
        else:
            msg_mic = "✅ *MIC:* Nessuna novità sui diari oggi."
    except Exception as e:
        msg_mic = "⚠️ *MIC:* Errore tecnico nel collegamento al sito."
        errori_rilevati.append(f"Dettaglio MIC: {type(e).__name__}")

    # 2. CONTROLLO CONCORSI ROMA PA
    # Monitoraggio concorsi regione Lazio e provincia di Roma [cite: 88]
    try:
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r_roma = requests.get(url_roma, headers=headers, timeout=20)
        
        if r_roma.status_code == 200:
            msg_roma = f"📍 *ROMA:* Link aggiornato ai concorsi PA: {url_roma}"
        else:
            msg_roma = f"⚠️ *ROMA:* Sito momentaneamente non raggiungibile (Status {r_roma.status_code})."
            errori_rilevati.append(f"Dettaglio ROMA: Status Code {r_roma.status_code}")
    except Exception as e:
        msg_roma = "⚠️ *ROMA:* Errore tecnico nel controllo."
        errori_rilevati.append(f"Dettaglio ROMA: {type(e).__name__}")

    # 3. COMPOSIZIONE E INVIO MESSAGGIO [cite: 107, 108, 109]
    testo_finale = f"{msg_mic}\n\n{msg_roma}"
    
    # Se ci sono stati errori tecnici, aggiungiamo la diagnostica in coda
    if errori_rilevati:
        testo_finale += "\n\n---\n🛠 *REPORT DIAGNOSTICO:*\n" + "\n".join(errori_rilevati)
        testo_finale += "\n\n_Controlla i log su GitHub Actions per maggiori dettagli._"

    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    try:
        payload = {
            "chat_id": CHAT_ID,
            "text": testo_finale,
            "parse_mode": "Markdown", # Permette il grassetto e i link puliti
            "disable_web_page_preview": False
        }
        res = requests.post(url_tg, json=payload, timeout=15)
        res.raise_for_status()
        print("Messaggio inviato correttamente a Telegram.")
    except Exception as e:
        print(f"Errore critico durante l'invio del messaggio: {e}")

if __name__ == "__main__":
    controlla()
