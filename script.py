import requests

# L'indirizzo della pagina specifica del concorso 1800 assistenti MiC
URL_CONCORSO = "https://www.inpa.gov.it/bandi-e-avvisi/dettaglio-bando-avviso/?concorso_id=072b25757b444256877907572d4265f0"

def controlla():
    headers = {'User-Agent': 'Mozilla/5.0'}
    risposta = requests.get(URL_CONCORSO, headers=headers)
    
    testo_pagina = risposta.text.lower()
    
    # Parole chiave che indicano che sono uscite le date
    parole_chiave = ["diario", "date d'esame", "prova scritta", "calendario"]
    
    trovato = any(parola in testo_pagina for parola in parole_chiave)
    
    if trovato:
        print("🚨 ATTENZIONE: Potrebbero essere uscite le date del concorso MiC!")
    else:
        print("✅ Tutto tranquillo: Nessun diario d'esame trovato oggi.")

if __name__ == "__main__":
    controlla()
