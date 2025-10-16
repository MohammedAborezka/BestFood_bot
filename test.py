from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load .env file (for local testing)
load_dotenv()

app = Flask(__name__)

# Load environment variables
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_ID = os.getenv("PHONE_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "my_verify_token")

def send_message(to, text):
    """Send a WhatsApp message using the Meta Graph API"""
    url = f"https://graph.facebook.com/v19.0/{PHONE_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.post(url, json=payload, headers=headers)
    print("📤 Message send response:", response.text)
    
@app.route("/cert.txt")
def serve_cert():
    return send_file("cert.txt")

@app.route("/", methods=["GET"])
def home():
    """Simple route to check if the bot is live"""
    return "✅ WhatsApp Bot is running!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """
    Handles both:
    - GET: Webhook verification (for Meta setup)
    - POST: Incoming WhatsApp messages
    """
    if request.method == "GET":
        # Verification request from Meta
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("✅ Webhook verified successfully!")
            return challenge, 200
        else:
            print("❌ Verification failed. Invalid token or mode.")
            return "Verification failed", 403

    if request.method == "POST":
        # Incoming message from WhatsApp
        data = request.get_json()
        print("📩 Incoming message:", data)

        try:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            sender = message['from']
            text = message['text']['body']

            if text:
                welcome_msg = (
                    "👋 Hello! Welcome to my WhatsApp chatbot.\n"
                    "I'm here to help you. How can I assist you today?"
                )
                send_message(sender, welcome_msg)
        except Exception as e:
            print("⚠️ Error processing message:", e)

        return jsonify(status="ok"), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
