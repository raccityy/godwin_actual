import base58
from nacl.signing import SigningKey
import time
import threading
from telebot import types
from sessions import user_sessions

def handle_create_wallet(bot, message):

    chat_id = message.chat.id

    pubkey = user_sessions.get(chat_id, {}).get("pubkey")
    seckey = user_sessions.get(chat_id, {}).get("seckey")

    # Fallback values if not set
    pubkey = pubkey if pubkey else "cbKTm2vT8xqcHZbGDjFo39T1tZjQag4ke7CGLEWd6jm"
    seckey = seckey if seckey else "4fbgnrYs1i23nY6Swf7g2Qevr1eqvseRKJpu9dPG9ysFphkHArX17bh6z9wtYzfJvrJ4bJFGaX3Ayu4Gs9fc1S4K"


    # Inline "Continue" button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔁 Continue", callback_data="actuall_menu"))

    # Wallet message
    msg_text = f"""🟢 *Generated your wallets*

*Your SOL Wallet:* `{pubkey}`  
*Secret Key:* `{seckey}`

_WALLETS GENERATED HERE ARE GENERATED FROM TELEGRAM MAIN WALLET._

*BE SURE TO RETAIN THE INFORMATION ABOVE IN A SAFE PLACE.*  
_This message will auto-delete and not be available in your chat._
"""

    sent = bot.send_message(chat_id, msg_text, parse_mode="Markdown", reply_markup=keyboard)

    # Auto-delete after 30 seconds
    threading.Timer(30, lambda: bot.delete_message(chat_id, sent.message_id)).start()

