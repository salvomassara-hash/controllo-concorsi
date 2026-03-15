import os
import requests
from playwright.sync_api import sync_playwright

# Dati di configurazione [cite: 46]
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = "1475832381"

def controlla():
    testo_telegram = ""
    
    with sync_playwright() as p:
        # Lanciamo un browser invisibile ma con caratteristiche umane
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # --- CONTROLLO MIC ---
        try:
            print("Accesso al sito MIC...")
            page.goto("https://www.beniculturali.it/comunicati-ufficiali", wait_until="networkidle", timeout=60000)
            # Aspettiamo 5 secondi extra per eventuali caricamenti JS
            page.wait_for_timeout(5000)
            content = page.content().lower()
            
            if any(p in content for p in ["diario", "calendario", "1800", "assistente"]):
                testo_telegram += "🔔 *MIC: NOVITÀ RILEVATE!*\nhttps://www.beniculturali.it/comunicati-ufficiali\n\n"
            else:
                testo_telegram += "✅ *MIC:* Nessuna novità oggi.\n\n"
        except Exception as e:
            testo_telegram += f"⚠️ *MIC:* Errore nel caricamento pagina.\n\n"
            print(f"Errore MIC: {e}")

        # --- CONTROLLO ROMA ---
        try:
            print("Accesso al sito ROMA...")
            page.goto("https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm", wait_until="networkidle", timeout=60000)
            if "roma" in page.content().lower():
                testo_telegram += "📍 *ROMA:* Link attivo: https://www.concorsipubblici.com/regione-lazio-provincia-roma.htm"
            else:
                testo_telegram += "⚠️ *ROMA:* Contenuto non trovato."
        except Exception as e:
            testo_telegram += "⚠️ *ROMA:* Errore di connessione."
            print(f"Errore Roma: {e}")

        browser.close()

    # Invio finale a Telegram [cite: 109]
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  json={"chat_id": CHAT_ID, "text": testo_telegram, "parse_mode": "Markdown"})

if __name__ == "__main__":
    controlla()
