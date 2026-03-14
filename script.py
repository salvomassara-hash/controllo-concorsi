import requests

# I tuoi dati sicuri
TOKEN = "8609744766:AAH59P3OQ89WTnvna94zsCHlpzoGjhRMaYM" 
CHAT_ID = "1475832381"

def controlla():
    msg_mic = ""
    msg_roma = ""
    
    # --- 1. CONTROLLO MINISTERO (MIC) ---
    try:
        r_mic = requests.get("https://www.beniculturali.it/comunicati-ufficiali", timeout=15)
        testo_mic = r_mic.text.lower()
        if any(p in testo_mic for p in ["diario", "calendario", "1800", "assistenti"]):
            msg_mic = "🚨 MIC: NOVITÀ RILEVATE! Controlla qui: https://www.beniculturali.it/comunicati-ufficiali"
        else:
            msg_mic = "✅ MIC: Nessuna novità sui diari oggi."
    except:
        msg_mic = "⚠️ MIC: Errore di collegamento al sito del Ministero."

    # --- 2. CONTROLLO ROMA (ConcorsiPubblici) ---
    try:
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r_roma = requests.get(url_roma, headers=headers, timeout=15)
        if r_roma.status_code == 200:
            msg_roma = "📍 ROMA: Link aggiornato ai concorsi PA: " + url_roma
        else:
            msg_roma = "⚠️ ROMA: Sito momentaneamente non raggiungibile."
    except:
        msg_roma = "⚠️ ROMA: Errore tecnico nel controllo."

    # --- INVIO MESSAGGIO UNICO ---
    testo_finale = f"{msg_mic}\n\n{msg_roma}"
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_tg, json={"chat_id": CHAT_ID, "text": testo_finale})

if __name__ == "__main__":
    controlla()
