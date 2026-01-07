from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

OWNER_ID = 8579215373
PRICE_PER_KM = 0.6

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Звідки забрати авто? (Країна, місто, вулиця)")

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    d = context.user_data

    if "from_place" not in d:
        d["from_place"] = t
        await update.message.reply_text("Куди потрібно доставити авто?")
        return

    if "to_place" not in d:
        d["to_place"] = t
        await update.message.reply_text("Скільки кілометрів приблизно?")
        return

    if "km" not in d:
        if not t.isdigit():
            await update.message.reply_text("Введіть тільки число.")
            return
        d["km"] = int(t)
        d["price"] = int(d["km"] * PRICE_PER_KM)
        kb = ReplyKeyboardMarkup([["Подати заявку","Скасувати"]], resize_keyboard=True)
        await update.message.reply_text(f"Сума доставки: {d['price']} €\nПодавати заявку?", reply_markup=kb)
        return

    if "confirm" not in d:
        if t == "Скасувати":
            d.clear()
            await update.message.reply_text("Заявку скасовано. Напишіть /start")
            return
        d["confirm"] = True
        await update.message.reply_text("Ваше імʼя?")
        return

    if "name" not in d:
        d["name"] = t
        await update.message.reply_text("Ваш номер телефону?")
        return

    if "phone" not in d:
        d["phone"] = t
        await update.message.reply_text("Марка, модель, рік авто?")
        return

    if "car" not in d:
        d["car"] = t
        kb = ReplyKeyboardMarkup([["На ходу","Не на ходу"]], resize_keyboard=True)
        await update.message.reply_text("Стан авто?", reply_markup=kb)
        return

    if "status" not in d:
        d["status"] = t
        await update.message.reply_text("Країна реєстрації авто?")
        return

    if "reg_country" not in d:
        d["reg_country"] = t
        kb = ReplyKeyboardMarkup([["Потрібне розмитнення","Не потрібно"]], resize_keyboard=True)
        await update.message.reply_text("Чи потрібне розмитнення?", reply_markup=kb)
        return

    if "customs" not in d:
        d["customs"] = t

        text = f"""
🚚 НОВА ЗАЯВКА TOWIX

Звідки: {d['from_place']}
Куди: {d['to_place']}
Км: {d['km']}
Ціна: {d['price']} €

Клієнт: {d['name']}
Телефон: {d['phone']}
Авто: {d['car']}
Стан: {d['status']}
Реєстрація: {d['reg_country']}
Розмитнення: {d['customs']}
"""

        await context.bot.send_message(chat_id=OWNER_ID, text=text)
        await update.message.reply_text("Дякуємо! Ваша заявка відправлена менеджеру.")
        d.clear()

def main():
    app = ApplicationBuilder().token("AAHfRO4tUnJIaWg4sNpyEXTcV5mIfRNjN4").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
    app.run_polling()

if name == "__main__":
    main()
