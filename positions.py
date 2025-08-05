from telebot import types
import startmev

def handle_positions(bot, call):
    chat_id = call.message.chat.id

    # Message text
    text = """📉 *You currently have no active positions.*

Once you start trading, your transactions will be displayed here."""

    # Buttons
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🚀 Start MEV", callback_data="StartEVSniper"),
        types.InlineKeyboardButton("❌ Close", callback_data="positions_close")
    )

    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=keyboard)


def handle_positions_callback(bot, call):
    if call.data == "positions_close":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
