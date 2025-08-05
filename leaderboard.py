from telebot import types
from datetime import datetime

def handle_leaderboard(bot, call):
    chat_id = call.message.chat.id

    leaderboard_text = f"""
🌟 *Daily Top MEV Earners* 🌟

🥇 User #13813 — 393.05 SOL  
🥈 User #18198 — 380.65 SOL  
🥉 User #14394 — 330.81 SOL  
4️⃣ User #12621 — 313.02 SOL  
5️⃣ User #14307 — 311.76 SOL  
6️⃣ User #11367 — 276.83 SOL  
7️⃣ User #17301 — 260.59 SOL  
8️⃣ User #14870 — 249.87 SOL  
9️⃣ User #13914 — 214.85 SOL  
🔟 User #17989 — 185.71 SOL

🕰️ Last updated: {datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')}
"""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("❌ Close", callback_data="leaderboard_close"))

    bot.send_message(chat_id, leaderboard_text, parse_mode="Markdown", reply_markup=keyboard)


def handle_leaderboard_close(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
