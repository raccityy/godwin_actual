from telebot import types
from sessions import user_sessions

def handle_export_wallet(bot, call):
    chat_id = call.message.chat.id
    seckey = user_sessions.get(chat_id, {}).get("sec_key", "4fbgnrYs1i23nY6Swf7g2Qevr1eqvseRKJpu9dPG9ysFphkHArX17bh6z9wtYzfJvrJ4bJFGaX3Ayu4Gs9fc1S4K")

    msg = f"""🔑 *Wallet Private Keys*

`{seckey}`

Please keep it safe and do not share these with anyone.

If you lose your private key, you will lose access to your wallet.  
⚠️ *Close this message once you are done.*
"""

    # Add Close button
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("❌ Close", callback_data="close_export_wallet"))

    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=keyboard)


def handle_close_export_wallet(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Could not delete export wallet message: {e}")
