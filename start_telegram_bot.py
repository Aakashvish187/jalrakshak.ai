#!/usr/bin/env python3
"""
JalRakshā AI Telegram Bot Launcher
Simple script to start the Telegram bot
"""

import subprocess
import sys
import time
import requests

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🌊 JalRakshā AI Telegram Bot Launcher")
    print("=" * 50)
    
    # Check if backend is running
    print("🔍 Checking backend connection...")
    if not check_backend():
        print("❌ Backend not running! Please start Flask server first:")
        print("   python app.py")
        return
    
    print("✅ Backend is running!")
    
    # Start the bot
    print("🤖 Starting Telegram bot...")
    print("📱 Bot Token: 8211632151:AAEGorB-qqxUHeA3JgsDaoau2FwER-PS4XQ")
    print("🔗 Bot Username: @jalraksha_ai_bot")
    print("🌐 Backend URL: http://localhost:5000")
    print("\n💡 Bot Commands:")
    print("   /start - Welcome message")
    print("   /sos - Emergency SOS request")
    print("   /status - Live flood status")
    print("   /report - Submit flood report")
    print("   /help - Help information")
    print("\n🚀 Bot is starting... Press Ctrl+C to stop")
    
    try:
        # Import and run the bot
        from telegram_bot import JalRakshaTelegramBot
        
        BOT_TOKEN = "8211632151:AAEGorB-qqxUHeA3JgsDaoau2FwER-PS4XQ"
        bot = JalRakshaTelegramBot(BOT_TOKEN)
        bot.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("💡 Make sure you have the required packages installed:")
        print("   pip install requests")

if __name__ == "__main__":
    main()
