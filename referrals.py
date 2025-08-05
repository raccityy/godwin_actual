from telebot import types

def handle_referrals(bot, call):
    chat_id = call.message.chat.id

    msg = """
🚀 *Earn 20% SOL From Every Friend You Invite!*

Invite your friends, and once they start MEV trading, you earn *20% of their deposit* — instantly.

🔍 *Here’s how it works:*
1. Share your unique referral link.
2. Friend deposits and starts MEV.
3. You receive 20% of their deposit to your wallet — auto.

🔥 No limits. No waiting.  
Keep inviting, keep stacking SOL.

[Your Referral Link](https://t.me/SniperMEV_Bot?start={chat_id})  
📤 *Copy & Start Earning*

_P.S. Rewards auto-claim. The more friends, the fatter your SOL stack._
"""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("❌ Close", callback_data="close_referrals")
    )

    bot.send_message(chat_id, msg, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=keyboard)

def handle_close_referrals(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        pass
