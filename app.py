from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    reply = resp.message()

    if msg == "hello":
        reply.body("Hi! I'm your test bot.")
    elif msg == "news":
        reply.body("Top headline: AI takes over the world!")
    else:
        reply.body("Send 'hello' or 'news'.")

    return str(resp)
