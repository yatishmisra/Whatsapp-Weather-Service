from flask import Flask
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK', 200

@app.route('/send-weather', methods=['GET'])
def send_weather():
    try:
        url = 'https://www.gov.je/weather/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        temp = soup.select_one('.currentWeather__temperature').text.strip()
        desc = soup.select_one('.currentWeather__description').text.strip()
        message = f"🌤️ Jersey Weather:\n{temp}, {desc}"

        client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
        client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',
            to=os.environ['TO_WHATSAPP']
        )

        return 'Message sent!', 200

    except Exception as e:
        return f"Error: {e}", 500
