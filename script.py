import requests

# INSERIAMO I DATI DIRETTAMENTE PER IL TEST
TOKEN = "8609744766:AAH59P3OQ89WTnvna94zsCHlpzoGjhRMaYM"  # Incolla qui il tuo token tra le virgolette
CHAT_ID = "1475832381"

def controlla():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "✅ SALVATORE, CE L'ABBIAMO FATTA! GitHub ti sta scrivendo!"}
    r = requests.post(url, json=payload)
    print(f"Risultato: {r.status_code} - {r.text}")

if __name__ == "__main__":
    controlla()
