import requests

# DATI DIRETTI (Senza passare dai Secrets di GitHub)
TOKEN = "8609744766:AAH59P3OQ89WTnvna94zsCHlpzoGjhRMaYM" 
CHAT_ID = "1475832381"

def controlla():
    link = "https://www.beniculturali.it/comunicati-ufficiali"
    try:
        r = requests.get(link, timeout=15)
        testo = r.text.lower()
        
        # Parole chiave che hai scelto tu
        if any(p in testo for p in ["diario", "calendario", "date", "1800", "assistenti"]):
            msg = f"🚨 NOVITÀ CONCORSO! Controlla qui: {link}"
        else:
            msg = "✅ Controllo MIC: Nessuna novità sui diari oggi."
            
        # Invio a Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})
        print("Messaggio inviato con successo!")
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    controlla()
