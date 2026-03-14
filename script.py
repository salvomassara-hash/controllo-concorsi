import requests

TOKEN = "IL_TUO_TOKEN_QUI" # Assicurati che ci sia il tuo token
CHAT_ID = "1475832381"

def controlla():
    messaggi = []
    
    # 1. CONTROLLO MINISTERO (Date Diario)
    try:
        r_mic = requests.get("https://www.beniculturali.it/comunicati-ufficiali")
        testo_mic = r_mic.text.lower()
        if any(parola in testo_mic for parola in ["diario", "1800", "assistenti", "calendario"]):
            messaggi.append("🚨 MIC: Possibili novità sui diari! Controlla: https://www.beniculturali.it/comunicati-ufficiali")
    except:
        pass

    # 2. CONTROLLO CONCORSANDO (Nuovi concorsi Roma)
    try:
        # Puntiamo alla pagina specifica dei concorsi nel Lazio/Roma
        link_concorsando = "https://www.concorsando.it/blog/concorsi-lazio/"
        r_cond = requests.get(link_concorsando)
        testo_cond = r_cond.text.lower()
        
        # Cerchiamo bandi specifici per Roma usciti di recente
        if "roma" in testo_cond:
            messaggi.append("📍 CONCORSANDO: Trovati nuovi riferimenti a ROMA! Guarda qui: " + link_concorsando)
    except:
        pass

    # INVIO RISULTATI
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    if messaggi:
        testo_finale = "\n\n".join(messaggi)
    else:
        testo_finale = "✅ Controllo quotidiano completato: nessuna novità rilevante per il MIC o per Roma."
    
    requests.post(url, json={"chat_id": CHAT_ID, "text": testo_finale})

if __name__ == "__main__":
    controlla()
