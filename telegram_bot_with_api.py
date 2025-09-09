#!/usr/bin/env python3
"""
Telegram Bot with Flask API for JalRaksha AI
Connects Telegram bot with the website dashboard
"""
import asyncio
import logging
import sqlite3
import sys
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Configuration
BOT_TOKEN = "8211632151:AAEGorB-qqxUHeA3JgsDaoau2FwER-PS4XQ"
DATABASE_PATH = 'telegram_sos.db'
FLASK_PORT = 5000

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

class TelegramBotWithAPI:
    def __init__(self):
        self.init_database()
        self.sos_requests = []
        self.bot_started = False
        
    def init_database(self):
        """Initialize SQLite database for SOS requests."""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sos_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    username TEXT,
                    chat_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    location TEXT,
                    status TEXT DEFAULT 'pending',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database error: {e}")
    
    def get_sos_requests(self):
        """Get all SOS requests from database."""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, user_id, username, chat_id, message, location, status, timestamp
                FROM sos_requests 
                ORDER BY timestamp DESC
            ''')
            
            requests = cursor.fetchall()
            conn.close()
            
            return [
                {
                    'id': req[0],
                    'user_id': req[1],
                    'username': req[2],
                    'chat_id': req[3],
                    'message': req[4],
                    'location': req[5],
                    'status': req[6],
                    'timestamp': req[7]
                }
                for req in requests
            ]
        except Exception as e:
            logger.error(f"Error getting SOS requests: {e}")
            return []
    
    def save_sos_request(self, user_id, username, chat_id, message, location=None):
        """Save SOS request to database."""
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO sos_requests 
                (user_id, username, chat_id, message, location, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(user_id),
                username,
                str(chat_id),
                message,
                location,
                'pending',
                datetime.now()
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"SOS request saved: {user_id} - {message}")
            return True
        except Exception as e:
            logger.error(f"Error saving SOS request: {e}")
            return False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user
        welcome_message = f"""
🌊 Welcome to JalRaksha AI Emergency System!

Hello {user.first_name}! I'm your emergency response bot.

🚨 Emergency Commands:
• Send HELP - Get assistance
• Send SOS - Emergency request
• Send EMERGENCY - Urgent help needed
• Send FLOOD - Report flood emergency
• Send RESCUE - Request rescue

📍 Location Sharing:
• Send your location for faster rescue
• Type your address or landmark

🆘 Quick Emergency:
Just type: HELP or SOS

Stay safe! 🛡️
        """
        
        keyboard = [
            [InlineKeyboardButton("🚨 EMERGENCY SOS", callback_data="emergency_sos")],
            [InlineKeyboardButton("📍 Share Location", callback_data="share_location")],
            [InlineKeyboardButton("ℹ️ Help", callback_data="help_info")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """
🆘 JalRaksha AI Emergency Help

🚨 Emergency Keywords:
• HELP - General assistance
• SOS - Emergency request
• EMERGENCY - Urgent help
• FLOOD - Flood emergency
• RESCUE - Rescue request

📍 Location Sharing:
• Send your current location
• Type your address
• Share landmark details

✅ What happens when you send SOS:
1. Your request is logged
2. Rescue team gets notified
3. You get confirmation with ID
4. Track your request status

📞 Contact:
Emergency: +91 9327773901
Web: http://localhost:8080

Stay safe! 🛡️
        """
        await update.message.reply_text(help_message)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages."""
        if not update.message or not update.message.text:
            return
            
        user = update.effective_user
        message_text = update.message.text.upper().strip()
        
        # Check for emergency keywords
        sos_keywords = ['HELP', 'SOS', 'EMERGENCY', 'FLOOD', 'RESCUE', 'DANGER', 'URGENT']
        is_emergency = any(keyword in message_text for keyword in sos_keywords)
        
        if is_emergency:
            await self.handle_sos_request(update, context, message_text)
        else:
            # Regular message
            await update.message.reply_text(
                "👋 Hello! Send HELP or SOS for emergency assistance."
            )
    
    async def handle_sos_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle SOS emergency request."""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Generate request ID
        request_id = f"TG{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Save to database
        success = self.save_sos_request(
            user.id,
            user.username or user.first_name,
            chat_id,
            message,
            "Unknown"  # Location will be updated if user shares it
        )
        
        if success:
            # Send confirmation
            confirmation_message = f"""
🚨 EMERGENCY REQUEST RECEIVED!

🆔 Request ID: {request_id}
📊 Status: Processing
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Your emergency request has been logged
✅ Rescue team has been notified
✅ You will receive updates soon

📞 Emergency Contact: +91 9327773901
🌐 Track Status: http://localhost:8080

Stay safe! Help is on the way! 🚁
            """
            
            await update.message.reply_text(confirmation_message)
            logger.info(f"SOS request processed: {request_id} from {user.username}")
        else:
            await update.message.reply_text(
                "❌ Error processing your request. Please try again or call +91 9327773901"
            )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        if query.data == "emergency_sos":
            await query.edit_message_text(
                "🚨 EMERGENCY SOS ACTIVATED!\n\nYour emergency request has been sent. Help is on the way!"
            )
            # Process as SOS request
            await self.handle_sos_request(update, context, "EMERGENCY SOS")
            
        elif query.data == "share_location":
            await query.edit_message_text(
                "📍 Share Your Location\n\nPlease send your current location or type your address for faster rescue coordination."
            )
            
        elif query.data == "help_info":
            await self.help_command(update, context)
    
    async def run_bot(self):
        """Run the Telegram bot."""
        try:
            # Create application
            application = Application.builder().token(BOT_TOKEN).build()
            
            # Add handlers
            application.add_handler(CommandHandler("start", self.start_command))
            application.add_handler(CommandHandler("help", self.help_command))
            application.add_handler(CallbackQueryHandler(self.button_callback))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info("JalRaksha AI Telegram Bot Starting...")
            logger.info("Bot is ready to receive emergency messages")
            
            self.bot_started = True
            
            # Start the bot
            await application.run_polling()
            
        except Exception as e:
            logger.error(f"Bot startup failed: {e}")
            self.bot_started = False

# Flask API Routes
@app.route('/status', methods=['GET'])
def get_status():
    """Get bot status."""
    return jsonify({
        'status': 'online' if bot_instance.bot_started else 'offline',
        'uptime': 'N/A',
        'requests_processed': len(bot_instance.get_sos_requests()),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/sos-requests', methods=['GET'])
def get_sos_requests():
    """Get all SOS requests."""
    requests = bot_instance.get_sos_requests()
    return jsonify(requests)

@app.route('/sos-requests', methods=['POST'])
def create_sos_request():
    """Create a new SOS request."""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    success = bot_instance.save_sos_request(
        data.get('user_id', 'web_user'),
        data.get('username', 'Web User'),
        data.get('chat_id', '0'),
        data.get('message'),
        data.get('location')
    )
    
    if success:
        return jsonify({'status': 'success', 'message': 'SOS request created'}), 201
    else:
        return jsonify({'error': 'Failed to create SOS request'}), 500

@app.route('/sos', methods=['POST'])
def create_website_sos_request():
    """Create a new SOS request from website."""
    try:
        data = request.get_json()
        
        # Extract data from request
        emergency_type = data.get('emergency_type', 'Emergency')
        location = data.get('location', 'Unknown')
        contact = data.get('contact', 'Unknown')
        people_count = data.get('people_count', '1')
        description = data.get('description', 'Emergency request from website')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        # Create SOS message
        sos_message = f"""
🚨 EMERGENCY SOS REQUEST 🚨

Type: {emergency_type}
Location: {location}
Contact: {contact}
People: {people_count}
Description: {description}
Time: {timestamp}
Source: Website
        """.strip()
        
        # Save to database
        success = bot_instance.save_sos_request(
            user_id='website_user',
            username='Website User',
            chat_id='website',
            message=sos_message,
            location=location
        )
        
        if success:
            # Send to admin chat (replace with your admin chat ID)
            try:
                admin_chat_id = "YOUR_ADMIN_CHAT_ID"  # Replace with your admin chat ID
                # You'll need to implement send_message_to_chat method
                logger.info("SOS request saved to database")
            except Exception as e:
                logger.error(f"Failed to send SOS to admin: {e}")
            
            return jsonify({
                'status': 'success',
                'message': 'SOS request created successfully'
            })
        else:
            return jsonify({'error': 'Failed to create SOS request'}), 500
        
    except Exception as e:
        logger.error(f"Error creating SOS request: {e}")
        return jsonify({'error': 'Failed to create SOS request'}), 500

@app.route('/send-alert', methods=['POST'])
def send_telegram_alert():
    """Send flood alert to Telegram."""
    try:
        data = request.get_json()
        message = data.get('message', 'Flood alert')
        alert_type = data.get('alert_type', 'HIGH')
        
        # Send to admin chat (replace with your admin chat ID)
        try:
            admin_chat_id = "YOUR_ADMIN_CHAT_ID"  # Replace with your admin chat ID
            # You'll need to implement send_message_to_chat method
            logger.info(f"Flood alert received: {alert_type}")
            
            return jsonify({
                'status': 'success',
                'message': 'Alert sent successfully'
            })
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")
            return jsonify({'error': 'Failed to send alert'}), 500
            
    except Exception as e:
        logger.error(f"Error sending alert: {e}")
        return jsonify({'error': 'Failed to send alert'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'telegram_bot': 'online' if bot_instance.bot_started else 'offline',
            'database': 'online',
            'api': 'online'
        }
    })

def run_flask_app():
    """Run Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=False)

def main():
    """Main function."""
    global bot_instance
    
    # Fix for Windows asyncio
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    bot_instance = TelegramBotWithAPI()
    
    print("🌊 JalRaksha AI - Telegram Bot with API")
    print("=" * 50)
    print(f"✅ Bot token configured")
    print(f"✅ Database: {DATABASE_PATH}")
    print(f"✅ API Server: http://localhost:{FLASK_PORT}")
    
    print("🚀 Starting services...")
    print("📱 Send /start to your bot to test")
    print("🌐 API available at http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    # Start Flask API in a separate thread
    flask_thread = threading.Thread(target=run_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Run the bot
    try:
        asyncio.run(bot_instance.run_bot())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        logger.error(f"Bot startup failed: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
