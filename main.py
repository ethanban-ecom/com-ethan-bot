
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_USERNAME = "@etbsrb"

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    bot.send_message(chat_id, 
        "Hey, I’m going to ask you 4 quick questions to understand your goals and send you a free eBook! 📖🥵\n\n👇 What’s your goal income?",
        reply_markup=goal_income_markup())

def goal_income_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("💰 10k per month", callback_data="goal_10k"),
        InlineKeyboardButton("💶 10–25k per month", callback_data="goal_10_25k"),
        InlineKeyboardButton("🚀 6-figure+ per month", callback_data="goal_6fig")
    )
    return markup

def yes_no_markup(step):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Yes", callback_data=f"{step}_yes"),
        InlineKeyboardButton("❌ No", callback_data=f"{step}_no")
    )
    return markup

def contact_choice_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📩 I will do now", callback_data="contact_now"),
        InlineKeyboardButton("💬 Not yet, let’s talk on WhatsApp", callback_data="contact_whatsapp")
    )
    return markup

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("goal_"):
        user_data[chat_id]["goal_income"] = data.replace("goal_", "").replace("_", "-")
        bot.send_message(chat_id, "👇 Do you have any current store or eCommerce experience?", reply_markup=yes_no_markup("exp"))
    elif data.startswith("exp_"):
        user_data[chat_id]["experience"] = "Yes" if "yes" in data else "No"
        bot.send_message(chat_id, "👇 What’s your Instagram @ or WhatsApp number?\n✍️ Please type it below (include country code):")
        bot.register_next_step_handler(call.message, handle_contact_input)
    elif data.startswith("contact_"):
        user_data[chat_id]["contacted"] = "Instagram" if "now" in data else "WhatsApp"
        summary = generate_summary(call.from_user, chat_id)
        bot.send_message(chat_id, "🤑 Thanks for applying — I’ll personally reach out and send you the eBook.\n\n📲 Message me on IG if you prefer: @ethanban 🚀")
        bot.send_message(chat_id=ADMIN_USERNAME, text=summary)

def handle_contact_input(message):
    chat_id = message.chat.id
    user_data[chat_id]["contact_info"] = message.text
    bot.send_message(chat_id, "👇 Have you contacted me on Instagram before? (@ethanban)", reply_markup=contact_choice_markup())

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
