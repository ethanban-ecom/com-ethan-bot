
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8015442876  # User's Telegram numeric ID

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, 
        "Hey, so good you want to get into making money online 💶\n\n"
        "I have 100s of clients doing the same.. while doing 6 figure months on my stores. The opportunity is endless 🤑\n\n"
        "I’m going to ask you 4 quick questions to understand your goals and send you a free eBook! 📖🥵\n\n"
        "⬇️ What’s your goal income?",
        reply_markup=goal_income_markup())

def goal_income_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💰 10k per month", callback_data="goal_10k"))
    markup.add(InlineKeyboardButton("💶 10–25k per month", callback_data="goal_10_25k"))
    markup.add(InlineKeyboardButton("🚀 6-figure+ per month", callback_data="goal_6fig"))
    return markup

def experience_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Yes", callback_data="exp_yes"))
    markup.add(InlineKeyboardButton("❌ No", callback_data="exp_no"))
    markup.add(InlineKeyboardButton("😬 I’ve tried, and failed..", callback_data="exp_failed"))
    return markup

def contacted_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📩 I will do now", callback_data="contact_now"))
    markup.add(InlineKeyboardButton("💬 Not yet, let’s talk on WhatsApp", callback_data="contact_whatsapp"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("goal_"):
        user_data[chat_id]["goal_income"] = data.replace("goal_", "").replace("_", "-")
        bot.send_message(chat_id, "⬇️ Do you have any current store or eCommerce experience?", reply_markup=experience_markup())
    elif data.startswith("exp_"):
        user_data[chat_id]["experience"] = {
            "exp_yes": "Yes",
            "exp_no": "No",
            "exp_failed": "Tried and failed"
        }[data]
        bot.send_message(chat_id,
            "⬇️ What’s your Instagram @ or WhatsApp number?\n\n"
            "📲 Please type it below (include country code)\n"
            "_Example: @ yourhandle or +123456789_")
        bot.register_next_step_handler(call.message, handle_contact_input)
    elif data.startswith("contact_"):
        user_data[chat_id]["contacted"] = "Instagram" if "now" in data else "WhatsApp"
        if "now" in data:
            bot.send_message(chat_id, "Great — let’s chat there and get you a store built and start making some sales 🚀")
        summary = generate_summary(call.from_user, chat_id)
        bot.send_message(chat_id,
            "🤑 Thanks for applying — I’ll personally reach out and send you the eBook below.\n\n"
            "You can read over this and get a full rundown of how it all works.\n\n"
            "📲 I’ll be in touch today and we can chat about getting you live 🥵👌🏽\n\n"
            "<YOUR_EBOOK_LINK_HERE>")
        bot.send_message(chat_id=ADMIN_ID, text=summary)

def handle_contact_input(message):
    chat_id = message.chat.id
    user_data[chat_id]["contact_info"] = message.text
    bot.send_message(chat_id, "⬇️ Have you contacted me on Instagram before? (@ ethanban)", reply_markup=contacted_markup())

def generate_summary(user, chat_id):
    data = user_data.get(chat_id, {})
    return f"""
New Ecom Applicant:

🎯 Goal Income: {data.get('goal_income')}
📦 Experience: {data.get('experience')}
📱 Contact Info: {data.get('contact_info')}
👀 Contacted You?: {data.get('contacted')}
☎️ Telegram: @{user.username or 'N/A'} (ID: {user.id})
"""

bot.polling()
