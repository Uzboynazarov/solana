# wallet.py
from solana.rpc.api import Client

def get_balance(wallet_address):
    client = Client("https://api.mainnet-beta.solana.com")
    try:
        response = client.get_balance(wallet_address)
        lamports = response['result']['value']
        sol = lamports / 1e9
        return round(sol, 4)
    except Exception as e:
        return f"❌ Xatolik: {e}"
