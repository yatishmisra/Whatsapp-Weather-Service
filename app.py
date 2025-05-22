from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "news" in incoming_msg:
        # Example: scraping example.com/news
        r = requests.get("https://example.com/news")  # replace with real site
        soup = BeautifulSoup(r.text, "html.parser")
        headline = soup.find("h1").text
        msg.body(f"Top headline: {headline}")
    elif "hello" in incoming_msg:
        msg.body("Welcome! Send 'news' to get the latest update.")
    else:
        msg.body("Sorry, I didn't understand that. Try 'news' or 'hello'.")

    return str(resp)
