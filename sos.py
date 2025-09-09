# ...existing code...
#!/usr/bin/env python3
"""
JalRakshā AI - SOS Emergency Bot

This script handles emergency SOS requests via Telegram/WhatsApp and integrates
with the JalRakshā AI system. It processes emergency messages, logs them to the
database, and notifies rescue teams.
"""
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import os
import sqlite3
import logging

# Telegram Bot imports
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    from telegram.constants import ParseMode
except ImportError:
    print("❌ python-telegram-bot not installed. Install with: pip install python-telegram-bot")
    exit(1)

# Configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN') or "YOUR_BOT_TOKEN_HERE"
DATABASE_PATH = os.getenv('DATABASE_PATH', 'jalraksha_ai.db')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')  # keep None if not set
RESCUE_TEAM_CHAT_ID = os.getenv('RESCUE_TEAM_CHAT_ID')

# Emergency keywords
SOS_KEYWORDS = ['HELP', 'SOS', 'EMERGENCY', 'FLOOD', 'RESCUE', 'DANGER', 'URGENT']
LOCATION_KEYWORDS = ['LOCATION', 'WHERE', 'HERE', 'AT']

@dataclass
class SOSRequest:
    """Data class for SOS request information."""
    id: Optional[int]
    user_id: str
    username: str
    chat_id: str
    message: str
    location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    status: str
    timestamp: datetime
    response_sent: bool

class SOSDatabase:
    """Database manager for SOS requests."""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """Initialize the database connection."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SOS requests table."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create SOS requests table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sos_requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        username TEXT,
                        chat_id TEXT NOT NULL,
                        message TEXT NOT NULL,
                        location TEXT,
                        latitude REAL,
                        longitude REAL,
                        status TEXT DEFAULT 'PENDING',
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        response_sent BOOLEAN DEFAULT FALSE,
                        rescue_team_notified BOOLEAN DEFAULT FALSE,
                        notes TEXT
                    )
                ''')
                
                # Create rescue teams table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS rescue_teams (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        team_name TEXT NOT NULL,
                        location TEXT NOT NULL,
                        contact TEXT NOT NULL,
                        status TEXT DEFAULT 'IDLE',
                        assigned_sos_id INTEGER,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (assigned_sos_id) REFERENCES sos_requests (id)
                    )
                ''')
                
                conn.commit()
                logging.info("✅ Database initialized successfully")
                
        except Exception as e:
            logging.error(f"❌ Database initialization failed: {e}")
            raise
    
    def save_sos_request(self, sos_request: SOSRequest) -> int:
        """Save SOS request to database and return inserted id."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sos_requests
                    (user_id, username, chat_id, message, location, latitude, longitude, status, timestamp, response_sent)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    sos_request.user_id,
                    sos_request.username,
                    sos_request.chat_id,
                    sos_request.message,
                    sos_request.location,
                    sos_request.latitude,
                    sos_request.longitude,
                    sos_request.status,
                    sos_request.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    int(sos_request.response_sent)
                ))
                conn.commit()
                inserted_id = cursor.lastrowid
                logging.info(f"✅ Saved SOS request id={inserted_id}")
                return inserted_id
        except Exception as e:
            logging.error(f"❌ Failed to save SOS request: {e}")
            raise
    
    def get_sos_requests(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent SOS requests."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, user_id, username, chat_id, message, location, latitude, longitude, status, timestamp, response_sent, rescue_team_notified, notes
                    FROM sos_requests
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (limit,))
                rows = cursor.fetchall()
                results = []
                for r in rows:
                    results.append({
                        'id': r['id'],
                        'user_id': r['user_id'],
                        'username': r['username'],
                        'chat_id': r['chat_id'],
                        'message': r['message'],
                        'location': r['location'],
                        'latitude': r['latitude'],
                        'longitude': r['longitude'],
                        'status': r['status'],
                        'timestamp': r['timestamp'],
                        'response_sent': bool(r['response_sent']),
                        'rescue_team_notified': bool(r['rescue_team_notified']),
                        'notes': r['notes']
                    })
                return results
        except Exception as e:
            logging.error(f"❌ Failed to get SOS requests: {e}")
            return []
    
    def update_sos_status(self, sos_id: int, status: str, notes: str = None):
        """Update SOS request status."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if notes is not None:
                    cursor.execute('''
                        UPDATE sos_requests
                        SET status = ?, notes = ?
                        WHERE id = ?
                    ''', (status, notes, sos_id))
                else:
                    cursor.execute('''
                        UPDATE sos_requests
                        SET status = ?
                        WHERE id = ?
                    ''', (status, sos_id))
                conn.commit()
                logging.info(f"🔄 Updated SOS {sos_id} to status={status}")
        except Exception as e:
            logging.error(f"❌ Failed to update SOS status: {e}")
    
    def get_rescue_teams(self) -> List[Dict[str, Any]]:
        """Get all rescue teams."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, team_name, location, contact, status, assigned_sos_id, created_at, updated_at
                    FROM rescue_teams
                    ORDER BY id DESC
                ''')
                rows = cursor.fetchall()
                teams = []
                for r in rows:
                    teams.append({
                        'id': r['id'],
                        'team_name': r['team_name'],
                        'location': r['location'],
                        'contact': r['contact'],
                        'status': r['status'],
                        'assigned_sos_id': r['assigned_sos_id'],
                        'created_at': r['created_at'],
                        'updated_at': r['updated_at']
                    })
                return teams
        except Exception as e:
            logging.error(f"❌ Failed to get rescue teams: {e}")
            return []

class SOSBot:
    """Main SOS Bot class for handling emergency requests."""
    
    def __init__(self, token: str):
        """Initialize the SOS bot."""
        self.token = token
        self.db = SOSDatabase()
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
        # Statistics
        self.stats = {
            "total_sos_requests": 0,
            "resolved_requests": 0,
            "active_requests": 0,
            "start_time": datetime.now()
        }
    
    def setup_handlers(self):
        """Setup bot command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("sos", self.sos_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.LOCATION, self.handle_location))
        
        # Callback query handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
🌊 **JalRakshā AI - Emergency Response System**

Welcome to the flood emergency response bot!

**Available Commands:**
• `/sos` - Send emergency SOS request
• `/help` - Get help information
• `/status` - Check system status

**Emergency Keywords:**
Type any of these words to trigger emergency response:
HELP, SOS, EMERGENCY, FLOOD, RESCUE, DANGER, URGENT

**Location Sharing:**
Share your location for faster rescue response.

Stay safe! 🚁
        """
        
        await update.message.reply_text(welcome_message, parse_mode=ParseMode.MARKDOWN)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_message = """
🚨 **Emergency Response Help**

**To request help:**
1. Type `/sos` or send a message with "HELP"
2. Share your location if possible
3. Describe your emergency situation


**Emergency Keywords:**
• HELP, SOS, EMERGENCY
• FLOOD, RESCUE, DANGER, URGENT

**Location Sharing:**
Use the location button to share your exact position for faster rescue.

**Response Time:**
Emergency requests are processed immediately and rescue teams are notified within minutes.

Stay calm and provide clear information! 🆘
        """
        
        await update.message.reply_text(help_message, parse_mode=ParseMode.MARKDOWN)
    
    async def sos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /sos command."""
        await self.process_sos_request(update, context, "SOS command triggered")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        requests = self.db.get_sos_requests(10)
        active_requests = [r for r in requests if r['status'] in ['PENDING', 'ASSIGNED']]
        
        status_message = f"""
📊 **System Status**

**Active SOS Requests:** {len(active_requests)}
**Total Requests Today:** {len(requests)}
**System Uptime:** {datetime.now() - self.stats['start_time']}

**Recent Activity:**
        """
        
        for req in requests[:3]:
            status_emoji = "🚨" if req['status'] == 'PENDING' else "✅" if req['status'] == 'RESOLVED' else "🔄"
            status_message += f"\n{status_emoji} {req['status']} - {req['timestamp']}"
        
        await update.message.reply_text(status_message, parse_mode=ParseMode.MARKDOWN)
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command (admin only)."""
        user_id = str(update.effective_user.id)
        
        if ADMIN_CHAT_ID is None or user_id != str(ADMIN_CHAT_ID):
            await update.message.reply_text("❌ Access denied. Admin only.")
            return
        
        # Get detailed statistics
        requests = self.db.get_sos_requests(50)
        teams = self.db.get_rescue_teams()
        
        admin_message = f"""
🔧 **Admin Dashboard**

**SOS Requests:** {len(requests)}
**Rescue Teams:** {len(teams)}
**Active Requests:** {len([r for r in requests if r['status'] == 'PENDING'])}

**Recent SOS Requests:**
        """
        
        for req in requests[:5]:
            admin_message += f"""
🚨 ID: {req['id']}
👤 User: {req['username']}
📝 Message: {req['message'][:50]}...
📍 Location: {req['location'] or 'Not provided'}
⏰ Time: {req['timestamp']}
📊 Status: {req['status']}
---
            """
        
        await update.message.reply_text(admin_message, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages."""
        message_text = update.message.text.upper()
        
        # Check for emergency keywords
        if any(keyword in message_text for keyword in SOS_KEYWORDS):
            await self.process_sos_request(update, context, update.message.text)
        else:
            # Regular message - provide help
            await update.message.reply_text(
                "Type 'HELP' or '/sos' for emergency assistance. Use /help for more information."
            )
    
    async def handle_location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle location messages."""
        location = update.message.location
        lat, lon = location.latitude, location.longitude
        
        # Store location in context for potential SOS request
        context.user_data['last_location'] = {
            'latitude': lat,
            'longitude': lon,
            'timestamp': datetime.now()
        }
        
        await update.message.reply_text(
            f"📍 Location received: {lat:.6f}, {lon:.6f}\n"
            "Location saved for emergency response. Type 'HELP' if you need assistance."
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline keyboards."""
        query = update.callback_query
        await query.answer()
        
        # Handle different callback actions
        if query.data.startswith('resolve_'):
            sos_id = int(query.data.split('_')[1])
            await self.resolve_sos_request(query, sos_id)
    
    async def process_sos_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Process an SOS request."""
        user = update.effective_user
        chat_id = str(update.effective_chat.id)
        
        # Get location if available
        location_info = context.user_data.get('last_location', {})
        
        # Create SOS request object
        sos_request = SOSRequest(
            id=None,
            user_id=str(user.id),
            username=user.username or user.first_name or "Unknown",
            chat_id=chat_id,
            message=message,
            location=f"{location_info.get('latitude', 0):.6f}, {location_info.get('longitude', 0):.6f}" if location_info else None,
            latitude=location_info.get('latitude'),
            longitude=location_info.get('longitude'),
            status='PENDING',
            timestamp=datetime.now(timezone.utc),
            response_sent=False
        )
        
        # Save to database
        sos_id = self.db.save_sos_request(sos_request)
        self.stats["total_sos_requests"] += 1
        self.stats["active_requests"] += 1
        
        # Send confirmation to user
        confirmation_message = f"""
🚨 **JalRakshā AI received your SOS request!**

**Request ID:** #{sos_id}
**Status:** PENDING
**Time:** {sos_request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

✅ **Rescue team has been notified**
🚁 **Emergency response is on the way**

**Stay safe and wait for rescue team!**

If you have additional information, please share it now.
        """
        
        # Create inline keyboard for admin actions
        keyboard = [
            [InlineKeyboardButton("📍 Share Location", callback_data=f"location_{sos_id}")],
            [InlineKeyboardButton("📞 Call Emergency", url="tel:108")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            confirmation_message, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        
        # Notify rescue team
        await self.notify_rescue_team(sos_request, sos_id)
        
        # Notify admin
        await self.notify_admin(sos_request, sos_id)
        
        logging.info(f"🚨 SOS request processed: ID {sos_id}, User: {user.username}")
    
    async def notify_rescue_team(self, sos_request: SOSRequest, sos_id: int):
        """Notify rescue team about new SOS request."""
        if not RESCUE_TEAM_CHAT_ID:
            logging.warning("⚠️ Rescue team chat ID not configured")
            return
        
        alert_message = f"""
🚨 **NEW EMERGENCY SOS REQUEST**

**Request ID:** #{sos_id}
**User:** {sos_request.username}
**Message:** {sos_request.message}
**Location:** {sos_request.location or 'Not provided'}
**Time:** {sos_request.timestamp.strftime('%Y-%m-%d %H:%M:%S')}

**IMMEDIATE ACTION REQUIRED**
🚁 Deploy rescue team immediately
📞 Contact emergency services if needed
        """
        
        try:
            chat = int(RESCUE_TEAM_CHAT_ID) if str(RESCUE_TEAM_CHAT_ID).isdigit() else RESCUE_TEAM_CHAT_ID
            await self.application.bot.send_message(
                chat_id=chat,
                text=alert_message,
                parse_mode=ParseMode.MARKDOWN
            )
            logging.info(f"✅ Rescue team notified for SOS {sos_id}")
        except Exception as e:
            logging.error(f"❌ Failed to notify rescue team: {e}")
    
    async def notify_admin(self, sos_request: SOSRequest, sos_id: int):
        """Notify admin about new SOS request."""
        if not ADMIN_CHAT_ID:
            logging.debug("Admin chat ID not configured; skipping admin notification.")
            return
        
        admin_message = f"""
🔔 **New SOS Request Alert**

**ID:** {sos_id}
**User:** {sos_request.username} (@{sos_request.user_id})
**Message:** {sos_request.message}
**Location:** {sos_request.location or 'Not provided'}
**Time:** {sos_request.timestamp}

**Database Status:** Saved successfully
        """
        try:
            chat = int(ADMIN_CHAT_ID) if str(ADMIN_CHAT_ID).isdigit() else ADMIN_CHAT_ID
            await self.application.bot.send_message(
                chat_id=chat,
                text=admin_message,
                parse_mode=ParseMode.MARKDOWN
            )
            logging.info(f"✅ Admin notified for SOS {sos_id}")
        except Exception as e:
            logging.error(f"❌ Failed to notify admin: {e}")

    # Placeholder for resolve action used in callback handler (simple example)
    async def resolve_sos_request(self, query, sos_id: int):
        self.db.update_sos_status(sos_id, "RESOLVED", notes="Resolved via admin action")
        await query.edit_message_text(f"✅ SOS #{sos_id} marked as RESOLVED")
        self.stats["resolved_requests"] += 1
        self.stats["active_requests"] = max(0, self.stats["active_requests"] - 1)

# ...existing code...
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    parser = argparse.ArgumentParser(description="JalRakshā AI SOS Bot")
    parser.add_argument("--telegram", action="store_true", help="Run Telegram bot")
    parser.add_argument("--api", action="store_true", help="Start API (not implemented)")
    args = parser.parse_args()

    if args.telegram:
        if BOT_TOKEN in (None, "", "YOUR_BOT_TOKEN_HERE"):
            print("❌ TELEGRAM_BOT_TOKEN not set. Set TELEGRAM_BOT_TOKEN env var or edit BOT_TOKEN in the file.")
            exit(1)

        bot = SOSBot(BOT_TOKEN)
        try:
            # Blocking call; starts polling for updates
            bot.application.run_polling()
        except KeyboardInterrupt:
            print("Stopped by user")
    else:
        print("No action selected. Use --telegram to run the Telegram bot.")
# ...existing code...