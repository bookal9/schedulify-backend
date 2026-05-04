import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://bookal9.github.io"])

@app.route('/')
def health_check():
    return {"status": "ok"}

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['name', 'email', 'tiktok', 'plan']):
            return jsonify({"error": "Missing required fields"}), 400
        
        name = data['name']
        email = data['email']
        tiktok = data['tiktok']
        plan = data['plan']
        
        # Send email notification
        send_notification_email(name, email, tiktok, plan)
        
        return jsonify({"message": "Subscription successful"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_notification_email(name, email, tiktok, plan):
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not gmail_address or not gmail_app_password:
        raise Exception("Gmail credentials not configured")
    
    # Create email message
    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = 'developerinfoapplication@gmail.com'
    msg['Subject'] = 'New Schedulify Signup'
    
    # Email body
    body = f"""Name: {name}
Email: {email}
TikTok: {tiktok}
Plan: {plan}"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email using Gmail SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(gmail_address, gmail_app_password)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
