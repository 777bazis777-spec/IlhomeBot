from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# 🔑 TOKENINGNI YOZ
TOKEN = "8374455405:AAHnP5XXSnQ5KL1zp63QNiYW_eyxgf6kiEs"

# 📐 LISTLAR
LISTS = ["5.8kv", "5.0kv", "Xdf"]

# 🪵 5.0kv — 415 000 so‘m
MATERIALS_415 = [
    "Izmir",
    "Kamel",
    "NyuJeckson",
    "Berlin",
    "Kanada",
    "Malaziya",
    "Dub yachmenniy",
    "Karona 2025",
    "Shpondoviy Arex",
    "Varshava",
    "Koxira",
    "Marokash",
]

# 🪵 5.0kv — 335 000 so‘m
MATERIALS_335 = [
    "Granit o'rta shagren",
    "Chestorflit",
    "Jekson Och",
    "Chestorflit To'q",
    "Conoma mat",
    "Loft to'q shagren",
    "Beliy korona mat",
    "Cocna astana mat",
    "Arusha vengi och",
    "Beliy Jemchug",
    "Pikkart",
]

ALL_MATERIALS = MATERIALS_415 + MATERIALS_335


def make_keyboard(items, prefix):
    keyboard = []
    for item in items:
        keyboard.append(
            [InlineKeyboardButton(item, callback_data=f"{prefix}:{item}")]
        )
    return InlineKeyboardMarkup(keyboard)


# ▶️ START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📐 Listni tanlang:",
        reply_markup=make_keyboard(LISTS, "list"),
    )


# 📐 LIST TANLANDI
async def list_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, list_name = query.data.split(":")
    context.user_data["list"] = list_name

    await query.message.reply_text(
        f"📐 Tanlangan list: {list_name}\n\n🪵 Materialni tanlang:",
        reply_markup=make_keyboard(ALL_MATERIALS, "material"),
    )


# 🪵 MATERIAL TANLANDI
async def material_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, material = query.data.split(":")
    list_name = context.user_data.get("list", "—")

    # 💰 NARX HISOBLASH
    if list_name == "5.0kv":
        if material in MATERIALS_415:
            price = "415 000 so‘m"
        elif material in MATERIALS_335:
            price = "335 000 so‘m"
        else:
            price = "Noma’lum"
    elif list_name == "5.8kv":
        price = "450 000 so‘m"
    elif list_name == "Xdf":
        price = "280 000 so‘m"
    else:
        price = "Noma’lum"

    await query.message.reply_text(
        f"✅ BUYURTMA:\n\n"
        f"📐 List: {list_name}\n"
        f"🪵 Material: {material}\n"
        f"💰 Narx: {price}"
    )

    context.user_data.clear()


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(list_chosen, pattern="^list:"))
    app.add_handler(CallbackQueryHandler(material_chosen, pattern="^material:"))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
