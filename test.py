from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAgI4mZBPdbUBPiT2UPzN9Ea5n2oY3LjP6W08TvMCBxulZC56Qzoo2eHgt33GdvyxiiFAdXk4gLzD1CdEoNPd0toRHArcAaPYZAfvGxJozVy0AaB7I1gxKi5t6Wdf6HBBGjBQ6CnrhsJwRUVgzM9OHrl5WVZAIVC1NstfzJHrQGvHJMhfU3MSZCjcfyrjQkNjA6mDS81AdQ3GlyCbvmtwc16TplcQmhAzkxWZAziOa0gZDZD"
PHONE_ID = "01557902213"

def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    requests.post(url, json=payload, headers=headers)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        sender = message['from']
        text = message['text']['body']
        
        # Detect if this is the user's first message
        if text:
            welcome_msg = (
                "👋 Hello! Welcome to my WhatsApp chatbot.\n"
                "I'm here to help you. How can I assist you today?"
            )
            send_message(sender, welcome_msg)
    except Exception as e:
        print("Error:", e)
        
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(port=5000)
