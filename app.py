from flask import Flask, request
import os

app = Flask(__name__)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "alaxendra123")

@app.route("/")
def home():
    return "Music Hub Bot is LIVE!"

@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def incoming():
    print(request.get_json())
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
