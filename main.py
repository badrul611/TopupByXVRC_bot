import time
from telebot import TeleBot, types

cooldown = {}
last_pressed = {}

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

bot = TeleBot('8238863597:AAEOF2PiRObtaNL11eu048cwU4AFdmSKI7U')

cooldown = {}
user_loading = []

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
        order_with_cooldown(call)
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

@bot.callback_query_handler(func=lambda call: call.data == "order")
def order_with_cooldown(call):
    user_id = call.from_user.id
    now = time.time()

    if user_id in cooldown and now - cooldown[user_id] < 5:
        bot.answer_callback_query(
            call.id,
            text="⛔ Whoa whoa, one click is enough! 😂",
            show_alert=True
        )
        return

    cooldown[user_id] = now

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

    bot.send_message(call.message.chat.id, text, parse_mode="HTML", reply_markup=markup)
    bot.answer_callback_query(call.id)

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


@bot.callback_query_handler(func=lambda call: call.data == "order")
def handle_order_now(call):
    handle_order(call)

# ⬇️ Fungsi ini untuk View Payment Details + /payment command
def send_terms(chat_id):
    text = (
        "⚠️Terms of Payment to XVRC SHOP⚠️\n\n"
        "By pressing the button below, you confirm that you have read and understood the following terms:\n\n"
        "1. All payments (via QR or manual transfer) are for verified customers of XVRC SHOP only.\n"
        "2. Do not share or distribute our payment details to third parties without consent.\n"
        "3. XVRC SHOP is not responsible for any misuse by external parties.\n"
        "4. XVRC SHOP is not involved in any scam, mule account, or fraudulent activities.\n"
        "5. All transactions are final and valid once payment is made.\n"
        "6. False claims or misuse will be reported to the authorities.\n"
        "7. You agree that all payments are made at your own risk.\n\n"

        "✅ Please click the button below if you agree to the terms above."
    )

    agree_markup = types.InlineKeyboardMarkup()
    agree_markup.add(types.InlineKeyboardButton("✅ I Agree & Saya Setuju", callback_data="confirm_terms"))

    bot.send_message(chat_id, text, reply_markup=agree_markup)

@bot.callback_query_handler(func=lambda call: call.data == "show_qr")
def handle_show_qr(call):
    send_terms(call.message.chat.id)

@bot.message_handler(commands=["payment"])
def payment(message):
    user_id = message.from_user.id
    now = time.time()

    if user_id in cooldown and now - cooldown[user_id] < 3:
        bot.send_message(message.chat.id, "⛔ Give me a sec… I’m just a robot 🤖💨")
        return

    cooldown[user_id] = now
    bot.send_message(message.chat.id, "✅ Request accepted. Showing payment info...")
    send_terms(message.chat.id)

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

@bot.callback_query_handler(func=lambda call: call.data == "payment")
def handle_payment_button(call):
    user_id = call.from_user.id
    now = time.time()

    if user_id in cooldown and now - cooldown[user_id] < 3:
        bot.answer_callback_query(call.id, "⛔ Give me a sec… I’m just a robot 🤖💨", show_alert=True)
        return

    cooldown[user_id] = now
    send_terms(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == "contact")
def contact_social(call):
    loading = types.InlineKeyboardMarkup()
    loading.add(types.InlineKeyboardButton("⏳ Loading...", callback_data="none"))
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=loading
    )
    contact_buttons = types.InlineKeyboardMarkup(row_width=2)
    contact_buttons.add(
        types.InlineKeyboardButton(" Telegram Chat", url="https://t.me/XVRC_SHOP"),
        types.InlineKeyboardButton(" WhatsApp Chat", url="https://wa.me/601140549179"),
        types.InlineKeyboardButton(" Telegram Group", url="https://t.me/XVRCShop"),
        types.InlineKeyboardButton(" WhatsApp Group", url="https://chat.whatsapp.com/BjSWmTIjH2IEbKlfKPafHP"),
        types.InlineKeyboardButton(" Instagram", url="https://www.instagram.com/xvrc.gamingshop/"),
        types.InlineKeyboardButton(" Facebook", url="https://www.facebook.com/xvrcshop"),
        types.InlineKeyboardButton(" TikTok", url="https://tiktok.com/@xvrc.gamingshop"),
        types.InlineKeyboardButton(" Shopee", url="https://shopee.com.my/xvrc.gamingshop?smtt=0.262404361-1662092615.3")
    )
    
    contact_buttons.add(
        types.InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu")
    )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="📲 Choose a platform:",
        reply_markup=contact_buttons
    )

@bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
def back_to_menu(call):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton('💎 MLBB Price List', callback_data='price'),
        types.InlineKeyboardButton('🧾 How To Order', callback_data='order'),
        types.InlineKeyboardButton('💰 Payment Info', callback_data='payment'),
        types.InlineKeyboardButton('☎️ Contact & Social Media', callback_data='contact'),
        types.InlineKeyboardButton('❓ FAQ', callback_data='faq'),
    )
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            "👋 <b>Welcome back to XVRC SHOP!</b>\n\n"
            "Fast • Affordable • Secure\n"
            "Trusted by gamers, powered by speed.\n"
            "Compare our prices and order now! 💥"
        ),
        parse_mode="HTML",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "faq")
def handle_faq(call):
    text = (
        "<b>❓ Frequently Asked Questions (FAQ)</b>\n\n"

        "🔹 <b>1. Berapa lama proses topup?</b>\n"
        "⏱️ 1 - 5 minit (kecuali waktu sibuk atau masalah server).\n\n"

        "🔹 <b>2. Saya dah bayar tapi belum dapat?</b>\n"
        "📩 Pastikan anda hantar bukti bayaran, ID, Server & Username kepada admin.\n\n"

        "🔹 <b>3. ID/Server salah, boleh refund?</b>\n"
        "❌ Maaf, tiada refund jika info salah diberikan.\n\n"

        "🔹 <b>4. Macam mana nak tahu ID dan Server MLBB saya?</b>\n"
        "👤 Buka game > Profile > Lihat User ID dan nombor dalam kurungan (Server).\n\n"

        "🔹 <b>5. Boleh topup akaun negara lain?</b>\n"
        "🌍 Boleh , tapi jumlah diamond tak sama .\n\n"

        "📌 Masih ada soalan? Tekan butang di bawah untuk hubungi admin."
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📨 Contact Admin", url="https://t.me/XVRC_SHOP"))
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📨 Contact Admin", url="https://t.me/XVRC_SHOP"),
        types.InlineKeyboardButton("⬅️ Back to Menu", callback_data="back_to_menu")
    ) 

    @bot.callback_query_handler(func=lambda call: call.data == "back_to_menu")
    def back_to_menu(call):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton('💎 MLBB Price List', callback_data='price'),
            types.InlineKeyboardButton('🧾 How To Order', callback_data='order'),
            types.InlineKeyboardButton('💰 Payment Info', callback_data='payment'),
            types.InlineKeyboardButton('☎️ Contact & Social Media', callback_data='contact'),
            types.InlineKeyboardButton('❓ FAQ', callback_data='faq'),
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=(
                "👋 <b>Welcome back to XVRC SHOP!</b>\n\n"
                "Fast • Affordable • Secure\n"
                "Trusted by gamers, powered by speed.\n"
                "Compare our prices and order now! 💥"
            ),
            parse_mode="HTML",
            reply_markup=markup
        )

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        parse_mode="HTML",
        reply_markup=markup
    )

# ⬇️ Start polling
print("Bot is running...")
bot.infinity_polling()
