import os
import smtplib
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return {"status": "ok"}

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'email', 'plan']):
            return jsonify({"error": "Missing required fields"}), 400

        name = data['name']
        email = data['email']
        tiktok = data.get('tiktok', '')
        plan = data['plan']

        # Send email in background so it doesn't timeout
        thread = threading.Thread(target=send_notification_email, args=(name, email, tiktok, plan))
        thread.daemon = True
        thread.start()

        return jsonify({"message": "Subscription successful"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_notification_email(name, email, tiktok, plan):
    try:
        gmail_address = os.getenv('GMAIL_ADDRESS')
        gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')

        if not gmail_address or not gmail_app_password:
            return

        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = 'developerinfoapplication@gmail.com'
        msg['Subject'] = 'New Schedulify Signup'

        body = f"Name: {name}\nEmail: {email}\nTikTok: {tiktok}\nPlan: {plan}"
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(gmail_address, gmail_app_password)
            server.send_message(msg)
    except Exception:
        pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))