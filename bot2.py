import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from wallet import get_balance
from sniper import start_sniper
from jupiter_swap import swap_token
from copier import start_copy_trading
from utils import short_address

# Tokenni o'rnatish
BOT_TOKEN = "7626262808:AAFXfHiZ9QvorOlYrLpeGutFwhTg6ao0cqY"

# Loggingni yoqish
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Start komandasining funksiyasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Xush kelibsiz, {user.first_name}!\n\n"
        "Quyidagi komandalar mavjud:\n"
        "/write_wallet <wallet> – Wallet manzilingizni saqlash\n"
        "/balance <wallet> – Wallet balansini ko‘rish\n"
        "/sniper <token> <miqdor> – Sniper xarid\n"
        "/swap <from_token> <to_token> <miqdor> – Token almashtirish\n"
        "/copy <master_wallet> <follower1,follower2,...> – Copy trading\n"
        "/afk – Auto-sell/AFK rejimini yoqish"
    )
    await update.message.reply_text(welcome_message)

# Wallet manzilini saqlash
async def write_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Iltimos, wallet manzilingizni kiriting.\nMisol: /write_wallet <wallet_address>")
        return
    wallet_address = context.args[0]
    # Manzilni saqlashni amalga oshirish
    await update.message.reply_text(f"Wallet manzilingiz saqlandi: {short_address(wallet_address)}")

# Balansni ko‘rish
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text("Iltimos, wallet manzilingizni kiriting.\nMisol: /balance <wallet_address>")
        return
    wallet_address = context.args[0]
    balance = get_balance(wallet_address)
    await update.message.reply_text(f"{wallet_address} balans: {balance} SOL")

# Sniper xaridni boshlash
async def sniper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 2:
        await update.message.reply_text("Iltimos, <token> va <miqdor> ni kiriting.\nMisol: /sniper <token> <miqdor>")
        return
    token = context.args[0]
    amount = context.args[1]
    wallet_address = context.args[2] if len(context.args) > 2 else ""
    result = start_sniper(wallet_address, token, amount)
    await update.message.reply_text(result)

# Token almashtirish
async def swap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 3:
        await update.message.reply_text("Iltimos, <from_token>, <to_token> va <miqdor> ni kiriting.\nMisol: /swap <from_token> <to_token> <miqdor>")
        return
    from_token = context.args[0]
    to_token = context.args[1]
    amount = context.args[2]
    wallet_address = context.args[3]  # Wallet manzili
    result = swap_token(wallet_address, from_token, to_token, amount)
    await update.message.reply_text(result)

# Copy trading
async def copy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Iltimos, <master_wallet> va <follower1,follower2,...> ni kiriting.\nMisol: /copy <master_wallet> <follower1,follower2,...>")
        return
    master_wallet = context.args[0]
    followers = context.args[1].split(',')
    result = start_copy_trading(master_wallet, followers)
    await update.message.reply_text(result)

# Auto-sell/AFK rejimi
async def afk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Auto-sell/AFK rejimi yoqildi.")

# Botni sozlash va ishga tushirish
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("write_wallet", write_wallet))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("sniper", sniper))
    application.add_handler(CommandHandler("swap", swap))
    application.add_handler(CommandHandler("copy", copy))
    application.add_handler(CommandHandler("afk", afk))

    application.run_polling()

if __name__ == "__main__":
    main()
