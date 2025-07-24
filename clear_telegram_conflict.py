import telebot

bot = telebot.TeleBot("7431663028:AAFV49gw_JPYXOmmkt5sf7GQyIgV-KSaeHc")

# Remove webhook
bot.remove_webhook()
print("Webhook removed")

# Test polling sekejap
bot.get_updates()
print("getUpdates tested")
