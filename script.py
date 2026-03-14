import requests

# I tuoi dati sicuri
TOKEN = "8609744766:AAH59P3OQ89WTnvna94zsCHlpzoGjhRMaYM" 
CHAT_ID = "1475832381"

def controlla():
    risultati = []
    
    # --- CONTROLLO 1: MINISTERO DELLA CULTURA ---
    try:
        r_mic = requests.get("https://www.beniculturali.it/comunicati-ufficiali", timeout=15)
        testo_mic = r_mic.text.lower()
        if any(p in testo_mic for p in ["diario", "calendario", "1800", "prove", "scritte", "assistenti"]):
            risultati.append("🚨 MIC: Novità sui diari! https://www.beniculturali.it/comunicati-ufficiali")
    except:
        risultati.append("⚠️ Errore nel controllare il sito del Ministero.")

    # --- CONTROLLO 2: CONCORSIPUBBLICI.COM (ROMA) ---
    try:
        # Link filtrato per la provincia di Roma
        url_roma = "https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
        headers = {'User-Agent': 'Mozilla/5.0'} # Facciamo finta di essere un browser
        r_roma = requests.get(url_roma, headers=headers, timeout=15)
        
        # Cerchiamo se ci sono bandi molto recenti (es. pubblicati "oggi" o "ieri")
        # Per ora facciamo un controllo semplice: se il sito risponde, ti diamo il link
        if r_roma.status_code == 200:
            risultati.append("📍 ROMA PA: Controlla nuovi bandi qui: " + url_roma)
    except:
        risultati.append("⚠️ Errore nel controllare ConcorsiPubblici.com")

    # --- INVIO MESSAGGIO UNICO ---
    testo_finale = "\n\n".join(risultati) if risultati else "✅ Nessun aggiornamento oggi."
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url_tg, json={"chat_id": CHAT_ID, "text": testo_finale})

if __name__ == "__main__":
    controlla()
