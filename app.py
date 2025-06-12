import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def get_weather_message():
    url = "https://prodgojweatherstorage.blob.core.windows.net/data/jerseyForecast.json"
    try:
        data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
        today = data.get("forecastDay", [{}])[0]
        return f"""🌤️ *Jersey Weather Update*

📍 Location: {data.get("Location", "Jersey")}
🕒 Issued: {data.get("forecastTime", "N/A")} on {data.get("forecastDate", "N/A")}
🌡️ Current: {data.get("currentTemprature", "N/A")}

📋 *Summary:* {today.get("summary", "N/A")}
🌅 Sunrise: {today.get("sunRise", "N/A")}, 🌇 Sunset: {today.get("sunSet", "N/A")}
💨 Wind: {today.get("windToolTipMPH", "N/A")}
🔆 UV Index: {today.get("uvIndex", "N/A")}
"""
    except Exception as e:
        return "❌ Unable to fetch weather right now."

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    msg_body = request.form.get("Body", "").strip().lower()
    resp = MessagingResponse()

    if "weather" in msg_body:
        reply = get_weather_message()
    else:
        reply = "👋 Hi! Reply with *weather* to get the latest forecast for Jersey."

    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)