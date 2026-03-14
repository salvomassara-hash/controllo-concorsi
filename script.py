import requests

# I tuoi dati che abbiamo testato e funzionano!
TOKEN = "8609744766:AAH59P3OQ89WTnvna94zsCHlpzoGjhRMaYM"  # Lascia il tuo token qui dentro
CHAT_ID = "1475832381"

def controlla_concorsi():
    link = "https://www.beniculturali.it/comunicati-ufficiali"
    try:
        risposta = requests.get(link)
        testo = risposta.text.lower()
        
        # Se trova le parole chiave, ti avvisa con urgenza
        if "diario" in testo or "calendario" in testo or "date" in testo or "1800" in testo or "assistenti" in testo:
            messaggio = "🚨 ATTENZIONE SALVATORE: Potrebbero essere uscite le date del concorso MiC! Controlla subito qui: " + link
        else:
            # Messaggio di controllo quotidiano
            messaggio = "✅ Controllo quotidiano MIC: nessuna novità sui diari oggi."
            
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": messaggio}
        requests.post(url, json=payload)
        
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    controlla_concorsi()
