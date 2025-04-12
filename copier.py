# copier.py
def start_copy_trading(master_wallet, follower_wallets):
    # Bu faqat namuna, real-time transaction sync keyin qo‘shiladi
    return (
        f"📡 Copy trading boshlandi:\n"
        f"🔰 Master: {master_wallet}\n"
        f"👥 Followerlar: {', '.join(follower_wallets)}\n"
        f"🔄 Harakatlar avtomatik ko‘chiriladi."
    )
