
import os
import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_ID = os.environ.get("GROUPME_BOT_ID", "")

JOKES = [
    "Why did the pizza maker get promoted? He really brought a lot to the table.",
    "I tried to tell a pizza joke, but it was too cheesy.",
    "My work ethic is like delivery pizza: always on the way.",
]

CHALLENGES = [
    "Challenge: Give a teammate genuine recognition today.",
    "Challenge: Find one thing you can improve before your next shift.",
    "Challenge: Do one task today that makes tomorrow easier.",
    "Challenge: Make someone's day better with excellent service.",
]


def send_message(text):
    if not BOT_ID:
        print("Missing GROUPME_BOT_ID configuration.")
        return

    response = requests.post(
        "https://api.groupme.com/v3/bots/post",
        json={"bot_id": BOT_ID, "text": text},
        timeout=10,
    )
    response.raise_for_status()


@app.route("/", methods=["GET"])
def home():
    return "GroupMe bot is running!"


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


@app.route("/callback", methods=["POST"])
def callback():
    message = request.get_json(silent=True) or {}

    # Ignore messages that weren't sent by a regular group member.
    if message.get("sender_type") != "user":
        return jsonify(status="ignored")

    # Ignore empty messages.
    text = (message.get("text") or "").strip()
    if not text:
        return jsonify(status="ignored")

    # Respond only to commands, not every conversation.
    command = text.lower().split()[0]

    if command == "!help":
        send_message(
            "Bot commands:\n"
            "!help - Show commands\n"
            "!ping - Check if I'm online\n"
            "!joke - Get a joke\n"
            "!challenge - Get a daily challenge"
        )
    elif command == "!ping":
        send_message("Pong! 🤖 I'm online.")
    elif command == "!joke":
        send_message(random.choice(JOKES))
    elif command == "!challenge":
        send_message(random.choice(CHALLENGES))

    return jsonify(status="ok")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
