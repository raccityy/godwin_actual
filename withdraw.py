from telebot import types
from sessions import user_sessions

def handle_withdraw(bot, call):
    chat_id = call.message.chat.id
    pubkey = user_sessions.get(chat_id, {}).get("pubkey", "Not Available")

    msg = f"""❌ *Cannot withdraw*  
because your current balance is *insufficient*!

🔑 *Your Main SOL Wallet*  
`{pubkey}` _(Tap to copy)_

💰 *Balance:* `0.0 SOL ($0.0)`

💡 _Please fund your wallet to make withdrawals._
"""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("❌ Close", callback_data="close_withdraw"))

    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=keyboard)


def handle_close_withdraw(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Could not delete withdraw message: {e}")
