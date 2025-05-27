from flask import Flask, request
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route('/')
def health_check():
    return 'OK', 200

@app.route('/send-weather', methods=['GET'])
def send_weather():
    return send_weather_message(os.environ['TO_WHATSAPP'])

def send_weather_message(to_whatsapp):
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
            to=to_whatsapp
        )

        return 'Message sent!', 200
    except Exception as e:
        print(f"Error in scheduled send: {e}")
        return f"Error: {e}", 500

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'weather' in incoming_msg:
        try:
            url = 'https://www.gov.je/weather/'
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers)

            # Debug logs
            print("Status Code:", r.status_code)
            print("First 500 chars of HTML:\n", r.text[:500])

            soup = BeautifulSoup(r.text, 'html.parser')
            temp = soup.select_one('.currentWeather__temperature').text.strip()
            desc = soup.select_one('.currentWeather__description').text.strip()

            msg.body(f"🌤️ Jersey Weather:\n{temp}, {desc}")
        except Exception as e:
            print(f"Error scraping: {e}")
            msg.body("⚠️ Sorry, couldn't fetch the weather right now.")
    else:
        msg.body("❓ Type 'weather' to get the current Jersey weather update.")

    return str(resp)
