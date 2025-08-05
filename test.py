from solana.rpc.api import Client
from solders.keypair import Keypair
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.rpc.types import TxOpts
from solana.publickey import PublicKey
import base58

# Your inputs
base58_key = "4fbgnrYs1i23nY6Swf7g2Qevr1eqvseRKJpu9dPG9ysFphkHArX17bh6z9wtYzfJvrJ4bJFGaX3Ayu4Gs9fc1S4K"
destination_address = "AB2rD7Tz6GbxSuXvfc3vbSxJWGXsZiDpRgypqvnnt8oJ"

# Use Ankr, QuickNode or official RPC (if no API key required)
client = Client("https://api.mainnet-beta.solana.com")

# Decode and load keypair
secret_key = base58.b58decode(base58_key)
keypair = Keypair.from_bytes(secret_key)
sender = keypair.pubkey()

# Fetch balance
balance_response = client.get_balance(sender)
if "result" not in balance_response or not balance_response["result"]:
    raise Exception("❌ Failed to fetch balance: " + str(balance_response))
balance = balance_response["result"]["value"]
print(f"🔐 Sender: {sender}")
print(f"💰 Balance: {balance / 1e9} SOL")

# Fetch recent blockhash
blockhash_resp = client.get_latest_blockhash()
if "result" not in blockhash_resp or not blockhash_resp["result"]:
    raise Exception("❌ Failed to get latest blockhash: " + str(blockhash_resp))
recent_blockhash = blockhash_resp["result"]["value"]["blockhash"]

# Set amount to send (all - fee)
fee = 5000
amount = balance - fee
if amount <= 0:
    raise Exception("❌ Not enough SOL to send after fee.")

# Build transaction
destination = PublicKey(destination_address)
txn = Transaction(recent_blockhash=recent_blockhash).add(
    transfer(
        TransferParams(
            from_pubkey=sender,
            to_pubkey=destination,
            lamports=amount
        )
    )
)

# Send transaction
send_result = client.send_transaction(txn, keypair, opts=TxOpts(skip_preflight=True))
print("✅ Sent! TX Signature:", send_result["result"])
