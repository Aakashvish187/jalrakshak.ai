from flask import Flask, request, jsonify
import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class TelegramWebhookHandler:
    def __init__(self, bot_token, backend_url="http://localhost:5000"):
        self.bot_token = bot_token
        self.backend_url = backend_url
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, chat_id, text, reply_markup=None):
        """Send message to Telegram user"""
        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            
            response = requests.post(url, json=data)
            return response.json()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def get_backend_data(self, endpoint):
        """Get data from Flask backend"""
        try:
            response = requests.get(f"{self.backend_url}{endpoint}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error getting backend data: {e}")
            return None
    
    def post_backend_data(self, endpoint, data):
        """Post data to Flask backend"""
        try:
            response = requests.post(f"{self.backend_url}{endpoint}", json=data)
            if response.status_code in [200, 201]:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error posting backend data: {e}")
            return None
    
    def handle_start_command(self, chat_id, user_name):
        """Handle /start command"""
        welcome_text = f"""
🌊 <b>Welcome to JalRakshā AI, {user_name}!</b>

I'm your personal flood monitoring assistant. Here's what I can do:

🚨 <b>Emergency Commands:</b>
/sos - Send emergency SOS request
/status - Check current flood risk status
/report - Report flood conditions

📊 <b>Information Commands:</b>
/live - Get live sensor data
/routes - Find safe routes
/teams - Check rescue team status

💡 <b>Quick Actions:</b>
Type any location to get flood risk assessment
Type "help" for more information

Stay safe! 🛡️
        """
        
        keyboard = {
            'keyboard': [
                [{'text': '🚨 SOS Emergency'}, {'text': '📊 Live Status'}],
                [{'text': '🗺️ Safe Routes'}, {'text': '🚑 Rescue Teams'}],
                [{'text': '📝 Report Issue'}, {'text': 'ℹ️ Help'}]
            ],
            'resize_keyboard': True,
            'one_time_keyboard': False
        }
        
        self.send_message(chat_id, welcome_text, keyboard)
    
    def handle_sos_command(self, chat_id, user_name):
        """Handle /sos command"""
        sos_text = f"""
🚨 <b>EMERGENCY SOS REQUEST</b>

{user_name}, I'm processing your emergency request...

Please provide your location:
1. Share your current location (GPS)
2. Or type your address/landmark

I'll immediately dispatch the nearest rescue team!
        """
        
        keyboard = {
            'keyboard': [
                [{'text': '📍 Share Location', 'request_location': True}],
                [{'text': '🏠 Enter Address'}, {'text': '❌ Cancel'}]
            ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        }
        
        self.send_message(chat_id, sos_text, keyboard)
    
    def handle_location(self, chat_id, latitude, longitude):
        """Handle location sharing"""
        try:
            # Call backend to assign rescue team
            data = {
                'lat': latitude,
                'lng': longitude
            }
            
            result = self.post_backend_data('/assign_rescue', data)
            
            if result:
                response_text = f"""
🚑 <b>RESCUE TEAM DISPATCHED!</b>

Team: {result['team']}
ETA: {result['eta']}
Status: {result['status']}
Distance: {result['distance']}

Your location has been logged and rescue team is on the way!
Stay safe and follow emergency protocols.
                """
            else:
                response_text = """
❌ <b>Error dispatching rescue team</b>

Please try again or contact emergency services directly.
                """
            
            self.send_message(chat_id, response_text)
            
        except Exception as e:
            logger.error(f"Error handling location: {e}")
            self.send_message(chat_id, "❌ Error processing location. Please try again.")
    
    def handle_live_status(self, chat_id):
        """Handle live status request"""
        try:
            data = self.get_backend_data('/get_live_data')
            
            if data:
                risk_emoji = "🟢" if data['risk'] == "Low" else "🟡" if data['risk'] == "Medium" else "🔴"
                
                status_text = f"""
📊 <b>LIVE FLOOD MONITORING STATUS</b>

{risk_emoji} <b>Risk Level:</b> {data['risk']}
💧 <b>Water Level:</b> {data['water_level']} cm
🌧️ <b>Rainfall:</b> {data['rainfall']} mm
🌊 <b>River Flow:</b> {data['river_flow']} m³/s

⏰ <b>Last Updated:</b> {data['timestamp']}

{'🚨 HIGH RISK ALERT! Take immediate precautions!' if data['risk'] == 'High' else '✅ Conditions are stable' if data['risk'] == 'Low' else '⚠️ Monitor conditions closely'}
                """
            else:
                status_text = "❌ Unable to fetch live data. Please try again later."
            
            self.send_message(chat_id, status_text)
            
        except Exception as e:
            logger.error(f"Error getting live status: {e}")
            self.send_message(chat_id, "❌ Error fetching status. Please try again.")
    
    def handle_report_command(self, chat_id, user_name):
        """Handle /report command"""
        report_text = f"""
📝 <b>FLOOD CONDITION REPORT</b>

{user_name}, please provide details about the flood situation:

1. <b>Location:</b> Where is the flooding?
2. <b>Severity:</b> How severe is it?
3. <b>Description:</b> What's happening?

Type your report in this format:
Location: [Your location]
Severity: [Low/Medium/High/Critical]
Description: [What you're seeing]

Example:
Location: Riverside District
Severity: High
Description: Water level rising rapidly, roads blocked
        """
        
        self.send_message(chat_id, report_text)
    
    def handle_report_submission(self, chat_id, message_text):
        """Handle report submission"""
        try:
            # Parse the report
            lines = message_text.split('\n')
            location = ""
            severity = "medium"
            description = ""
            
            for line in lines:
                if line.startswith('Location:'):
                    location = line.replace('Location:', '').strip()
                elif line.startswith('Severity:'):
                    severity = line.replace('Severity:', '').strip().lower()
                elif line.startswith('Description:'):
                    description = line.replace('Description:', '').strip()
            
            if location and description:
                # Submit to backend
                data = {
                    'location': location,
                    'description': description,
                    'severity': severity,
                    'contact': f"Telegram: {chat_id}"
                }
                
                result = self.post_backend_data('/report_issue', data)
                
                if result:
                    response_text = f"""
✅ <b>REPORT SUBMITTED SUCCESSFULLY!</b>

Report ID: {result['report_id']}
Location: {location}
Severity: {severity.title()}
Time: {result['timestamp']}

Your report has been logged and will be reviewed by authorities.
Thank you for helping keep the community safe!
                    """
                else:
                    response_text = "❌ Error submitting report. Please try again."
            else:
                response_text = "❌ Please provide both location and description."
            
            self.send_message(chat_id, response_text)
            
        except Exception as e:
            logger.error(f"Error handling report: {e}")
            self.send_message(chat_id, "❌ Error processing report. Please try again.")
    
    def handle_help_command(self, chat_id):
        """Handle /help command"""
        help_text = """
ℹ️ <b>JalRakshā AI Bot Help</b>

🚨 <b>Emergency Commands:</b>
/sos - Send emergency SOS request
/status - Check current flood risk status
/report - Report flood conditions

📊 <b>Information Commands:</b>
/live - Get live sensor data
/routes - Find safe routes
/teams - Check rescue team status

💡 <b>Quick Actions:</b>
• Type any location to get flood risk assessment
• Share your location for emergency response
• Use the keyboard buttons for quick access

🔧 <b>How to Use:</b>
1. Use /start to begin
2. Use /sos for emergencies
3. Use /report to submit flood reports
4. Use /live to check current conditions

Stay safe! 🛡️
        """
        
        self.send_message(chat_id, help_text)
    
    def process_message(self, message):
        """Process incoming message"""
        try:
            chat_id = message['chat']['id']
            user_name = message['from'].get('first_name', 'User')
            text = message.get('text', '')
            
            # Handle commands
            if text.startswith('/'):
                command = text.split()[0].lower()
                
                if command == '/start':
                    self.handle_start_command(chat_id, user_name)
                elif command == '/sos':
                    self.handle_sos_command(chat_id, user_name)
                elif command == '/status' or command == '/live':
                    self.handle_live_status(chat_id)
                elif command == '/report':
                    self.handle_report_command(chat_id, user_name)
                elif command == '/help':
                    self.handle_help_command(chat_id)
                else:
                    self.send_message(chat_id, "❓ Unknown command. Use /help for available commands.")
            
            # Handle location sharing
            elif 'location' in message:
                location = message['location']
                self.handle_location(chat_id, location['latitude'], location['longitude'])
            
            # Handle report submission
            elif 'Location:' in text and 'Description:' in text:
                self.handle_report_submission(chat_id, text)
            
            # Handle other messages
            else:
                # Check if it's a location query
                if any(word in text.lower() for word in ['flood', 'water', 'rain', 'risk', 'status']):
                    self.handle_live_status(chat_id)
                else:
                    self.send_message(chat_id, "❓ I didn't understand that. Use /help for available commands.")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")

# Initialize the webhook handler
BOT_TOKEN = "8211632151:AAEGorB-qqxUHeA3JgsDaoau2FwER-PS4XQ"
webhook_handler = TelegramWebhookHandler(BOT_TOKEN)

@app.route('/telegram-webhook', methods=['POST'])
def telegram_webhook():
    """Handle Telegram webhook"""
    try:
        data = request.get_json()
        
        if 'message' in data:
            webhook_handler.process_message(data['message'])
        
        return jsonify({'status': 'ok'})
    
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/telegram-status', methods=['GET'])
def telegram_status():
    """Check Telegram bot status"""
    return jsonify({
        'status': 'active',
        'bot_token': BOT_TOKEN[:10] + '...',
        'backend_url': webhook_handler.backend_url,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
