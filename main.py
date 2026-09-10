import os
import random
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("TOKEN não configurado")

bot = telebot.TeleBot(TOKEN)

receitas = {
    "🥑 Mom's Bread": "🥑 **MOM'S KETO BREAD**\n\n3 eggs + 100g mozzarella + 1 spoon cream cheese\nMix + 15 min airfryer at 180C\n\nMacros: 2g carbs | 25g fat | 18g protein",
    "🥩 Dad's Picanha": "🥩 **DAD'S PICANHA**\n\nCoarse salt + butter + garlic\nSear 3 min each side - medium rare\n\nThe King of Keto Family!",
    "🍳 Kids Omelette": "🍳 **KIDS OMELETTE**\n\n2 eggs + cheese + ham\n2 min pan - Kids love it!\n\nPerfect for breakfast!",
    "🥓 Keto Pancake": "🥓 **KETO PANCAKE**\n\n2 eggs + 2 spoons almond flour + cinnamon\nMix and fry! Add peanut butter on top!",
    "🍕 Fake Pizza": "🍕 **FAKE PIZZA**\n\nChicken crust: 200g chicken + 1 egg + cheese\nSauce + cheese - 10 min oven at 200C\n\nZero carbs pizza!",
}

DIETA_TEXTO = (
    "🥑 *KETO FAMILY GUIDE*\n\n"
    "📘 What is Keto? https://www.dietdoctor.com/low-carb/keto\n\n"
    "🧮 Calculator: https://www.ruled.me/keto-calculator/\n\n"
    "🥩 Recipes: https://www.wholesomeyum.com/keto-recipes/\n\n"
    "📲 Chat: t.me/ketofamilychat\n"
    "📢 Channel: t.me/ketofamilybros\n\n"
    "Hold $KETO for VIP! 🚀"
)

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(name, callback_data=name) for name in receitas]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("🥑 Keto Diet Guide", callback_data="dieta"))
    bot.send_message(message.chat.id, "🥩🥑 **KETO FAMILY OFFICIAL BOT** 🔥\n\n👨 Dad - Picanha Master\n👩 Mom - Avocado Queen\n👧👦 Kids - Fitness Squad\n\nChoose below 👇\n\n/recipes /motivation /about /diet /ca", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: True)
def callback(callback):
    if callback.data == "dieta":
        bot.answer_callback_query(callback.id)
        bot.send_message(callback.message.chat.id, DIETA_TEXTO, parse_mode="Markdown")
        return
    recipe = receitas.get(callback.data)
    if not recipe:
        bot.answer_callback_query(callback.id, "Recipe no longer available.")
        return
    bot.answer_callback_query(callback.id)
    bot.send_message(callback.message.chat.id, recipe, parse_mode="Markdown")

@bot.message_handler(commands=["recipes", "receitas"])
def recipes_cmd(message):
    bot.send_message(message.chat.id, random.choice(list(receitas.values())), parse_mode="Markdown")

@bot.message_handler(commands=["motivation", "motivacao"])
def motivation(message):
    frases = ["💪 Family that trains together, stays together!", "🔥 Burn fat, not carbs!", "⚡ Zero sugar = 100% focus!"]
    bot.reply_to(message, random.choice(frases))

@bot.message_handler(commands=["about", "sobre"])
def about(message):
    bot.reply_to(message, "👨‍👩‍👧‍👦 KETO FAMILY is lifestyle! Keto + Family + Gains!")

@bot.message_handler(commands=["dieta", "keto", "diet"])
def dieta_links(message):
    bot.reply_to(message, DIETA_TEXTO, parse_mode="Markdown")

@bot.message_handler(commands=["ca"])
def ca(message):
    bot.reply_to(message, "📜 **CAs COMING SOON** 🚀\nBSC: soon\nSOL: soon\nBASE: soon\nTON: soon", parse_mode="Markdown")

def configure_commands():
    bot.set_my_commands([
        types.BotCommand("start", "Open the KETO FAMILY menu"),
        types.BotCommand("recipes", "Get a random recipe"),
        types.BotCommand("motivation", "Get a motivation message"),
        types.BotCommand("about", "About KETO FAMILY"),
        types.BotCommand("diet", "Open the Keto diet guide"),
        types.BotCommand("ca", "Contracts coming soon"),
    ])

from keep_alive import keep_alive

if __name__ == "__main__":
    keep_alive()
    print("Bot Keto Family ATIVO!")
    try:
        configure_commands()
    except Exception as e:
        print(f"Erro ao configurar comandos: {e}")

    # Loop que nunca deixa o bot morrer
    while True:
        try:
            print("Iniciando polling...")
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print(f"Bot caiu com erro: {e} - Reiniciando em 5s...")
            import time
            time.sleep(5)

