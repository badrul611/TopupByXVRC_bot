from keep_alive import keep_alive
from telebot import TeleBot, types

PRICE_PAGES = [
"""84 💎 RM 7.00
182 💎 RM 14.00
210 💎 RM 16.00
284 💎 RM 21.00
326 💎 RM 24.50
355 💎 RM 26.50
429 💎 RM 32.00
513 💎 RM 38.50
583 💎 RM 44.00
716 💎 RM 53.00""",
"""772 💎 RM 58.00
870 💎 RM 65.00
1071 💎 RM 80.00
1145 💎 RM 85.00
1285 💎 RM 95.00
1446 💎 RM 105.00
1586 💎 RM 116.00
1656 💎 RM 122.00
1889 💎 RM 138.00
2162 💎 RM 158.00""",
"""2302 💎 RM 169.00
2531 💎 RM 186.00
2703 💎 RM 199.00
2976 💎 RM 212.00
3102 💎 RM 220.00
3274 💎 RM 234.00
3345 💎 RM 238.00
3475 💎 RM 248.00
3517 💎 RM 252.00
3692 💎 RM 265.00""",
"""3734 💎 RM 268.00
3846 💎 RM 277.00
3976 💎 RM 286.00
4121 💎 RM 297.00
4331 💎 RM 313.00
4436 💎 RM 319.00
4632 💎 RM 334.00
4851 💎 RM 350.00
5138 💎 RM 371.00
5278 💎 RM 382.00""",
"""5422 💎 RM 393.00
5637 💎 RM 409.00
5854 💎 RM 425.00
6092 💎 RM 435.00
6236 💎 RM 446.00
6307 💎 RM 451.00
6668 💎 RM 478.00
7502 💎 RM 525.00
7786 💎 RM 546.00
7931 💎 RM 557.00""",
"""8218 💎 RM 578.00
8948 💎 RM 630.00
9377 💎 RM 662.00
9664 💎 RM 683.00
10478 💎 RM 736.00
12640 💎 RM 894.00
15046 💎 RM 1054.00
16004 💎 RM 1125.00
17890 💎 RM 1262.00
20956 💎 RM 1472.00"""
]

bot = telebot.TeleBot("7431663028:AAFV49gw_JPYXOmmkt5sf7GQyIgV-KSaeHc")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('💎 MLBB Price List', callback_data='price'),
        types.InlineKeyboardButton('🧾 How To Order', callback_data='order'),
        types.InlineKeyboardButton('💰 Payment Info', callback_data='payment'),
        types.InlineKeyboardButton('☎️ Contact & Social Media', callback_data='contact'),
        types.InlineKeyboardButton('❓ FAQ', callback_data='faq'),
    )
    bot.send_message(
        message.chat.id,
        """👋 Welcome to XVRC SHOP!

Fast • Affordable • Secure
Trusted by gamers, powered by speed.
Compare our prices and order now! 💥""",
        reply_markup=markup
    )

@bot.message_handler(commands=['price'])
def handle_price(message):
    page = 0
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
    markup.add(types.InlineKeyboardButton("🛒 Order Now", callback_data="order"))
    bot.send_message(message.chat.id, PRICE_PAGES[page], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("page_") or call.data in ["order", "price"])
def callback_query(call):
    if call.data == "price":
        page = 0
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
        markup.add(types.InlineKeyboardButton("🛒 Order Now", callback_data="order"))
        bot.send_message(call.message.chat.id, PRICE_PAGES[page], reply_markup=markup)
        return

    if call.data == "order":
        order(call.message)  # Terus panggil fungsi /order
        return

    page = int(call.data.split("_")[1])
    markup = types.InlineKeyboardMarkup()
    if page > 0:
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"page_{page-1}"))
    if page < len(PRICE_PAGES) - 1:
        markup.add(types.InlineKeyboardButton("➡️ Next", callback_data=f"page_{page+1}"))
    markup.add(types.InlineKeyboardButton("🛒 Order Now", callback_data="order"))
    bot.edit_message_text(
        PRICE_PAGES[page],
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.message_handler(commands=["order"])
def order(message):
    text = (
        "🛒 How to Order MLBB Diamonds:\n\n"
        "1. Choose the diamond amount you want (refer to /price).\n\n"
        "2. Make payment via <b>QR Code or Official Account</b>.\n"
        "👉 Tap the button below to view full payment details.\n\n"
        "3. Send payment proof along with the following details:\n\n"
        "Username:\n"
        "User ID:\n"
        "Server:\n"
        "Diamond Quantity:\n"
        "📸 Screenshot of receipt:\n\n"
        "📩 Send to admin on Telegram: @XVRC_SHOP\n\n"
        "⚠️ Ensure all details are complete to avoid delays.\n"
        "⚠️ No refunds for incorrect ID or server information."
    )

    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("📷 View Payment Details", callback_data="show_qr")
    )
    markup.row(
        types.InlineKeyboardButton("📋 Copy Format", callback_data="copy_format"),
        types.InlineKeyboardButton("📨 Contact Admin", url="https://t.me/XVRC_SHOP")
    )

    bot.send_message(message.chat.id, text, parse_mode="HTML", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "copy_format")
def send_copy_format(call):
    format_text = (
        "Username:\n"
        "User ID:\n"
        "Server:\n"
        "Diamond Quantity:\n"
        "📸 Screenshot of payment"
    )
    bot.answer_callback_query(call.id, "Format copied!")
    bot.send_message(call.message.chat.id, f"\n{format_text}\n", parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "order_now")
def handle_order_now(call):
    order(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "show_qr")
def send_terms(call):
    text = (
        "⚠️ <b>Terms of Payment to XVRC SHOP</b> ⚠️\n\n"
        "By pressing the button below, you confirm that you have read and understood the following terms:\n\n"
        "1. All payments (via QR or manual transfer) are for verified customers of XVRC SHOP only.\n"
        "2. Do not share or distribute our payment details to third parties without consent.\n"
        "3. XVRC SHOP is not responsible for any misuse by external parties.\n"
        "4. XVRC SHOP is not involved in any scam, mule account, or fraudulent activities.\n"
        "5. All transactions are final and valid once payment is made.\n"
        "6. False claims or misuse will be reported to the authorities.\n"
        "7. You agree that all payments are made at your own risk.\n\n"
        "— — — — — — — — — — —\n\n"
        "⚠️ <b>Syarat Pembayaran ke Akaun XVRC SHOP</b> ⚠️\n\n"
        "Dengan menekan butang di bawah, anda mengesahkan bahawa anda telah membaca dan memahami syarat berikut:\n\n"
        "1. Segala bayaran (QR atau pindahan manual) hanya untuk pelanggan sah XVRC SHOP.\n"
        "2. Dilarang berkongsi atau sebarkan maklumat pembayaran kepada pihak ketiga tanpa kebenaran.\n"
        "3. XVRC SHOP tidak bertanggungjawab atas sebarang penyalahgunaan oleh pihak luar.\n"
        "4. XVRC SHOP tidak terlibat dalam kegiatan 'scam', akaun keldai atau penipuan.\n"
        "5. Semua transaksi adalah sah dan muktamad selepas pembayaran dibuat.\n"
        "6. Sebarang tuntutan palsu atau salah guna akan dilaporkan kepada pihak berkuasa.\n"
        "7. Anda bersetuju bahawa segala pembayaran dibuat atas tanggungjawab sendiri.\n\n"
        "✅ Please click the button below if you agree to the terms above."
    )

    agree_markup = types.InlineKeyboardMarkup()
    agree_markup.add(types.InlineKeyboardButton("✅ I Agree & Saya Setuju", callback_data="confirm_terms"))

    bot.send_message(call.message.chat.id, text, parse_mode="HTML", reply_markup=agree_markup)


@bot.callback_query_handler(func=lambda call: call.data == "confirm_terms")
def handle_confirm_terms(call):
    try:
        with open("maybank_qr.jpg", "rb") as qr_img:
            bot.send_photo(
                call.message.chat.id,
                photo=qr_img,
                caption="✅ You have agreed to the terms.\nPlease make payment to:\n\n🐯 Maybank\n563064175427\nXVRC SHOP"
            )
        bot.answer_callback_query(call.id, "QR sent.")
    except Exception as e:
        bot.send_message(call.message.chat.id, "❌ Failed to open QR.")
        print("Error QR:", e)

keep_alive()
print("Bot is running...")
bot.remove_webhook()
bot.infinity_polling()
