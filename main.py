from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters

FROM_ADDRESS, TO_ADDRESS, PHONE, CAR_INFO = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Звідки забрати авто? (Країна, місто, вулиця)")
    return FROM_ADDRESS

async def from_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["from"] = update.message.text
    await update.message.reply_text("Куди потрібно доставити авто?")
    return TO_ADDRESS

async def to_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["to"] = update.message.text
    await update.message.reply_text("Ваш номер телефону?")
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Марка, модель, рік авто?")
    return CAR_INFO

async def car_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["car"] = update.message.text
    await update.message.reply_text("✅ Заявку прийнято! Ми скоро з вами звʼяжемось.")
    print(context.user_data)
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("AAHfRO4tUnJIaWg4sNpyEXTcV5mIfRNjN4").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FROM_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, from_address)],
            TO_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, to_address)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            CAR_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, car_info)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()
