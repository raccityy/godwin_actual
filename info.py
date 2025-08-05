from telebot import types

def handle_info(bot, call):
    chat_id = call.message.chat.id

    info_text = """
🧠 *What is Solana Sniper MEV?*

Solana Sniper MEV is your automated MEV execution engine, built for raw speed and total control. It’s designed to dominate the Solana trading landscape with high-speed strategies like front-running and back-running — fully automated and ruthlessly fast.
"""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("❌ Close", callback_data="close_info")
    )

    bot.send_message(chat_id, info_text, parse_mode="Markdown", reply_markup=keyboard)

def handle_close_info(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
