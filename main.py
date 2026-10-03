import os
import random
import logging
import threading
import time
import telebot
from telebot import types

import store
from recipes_data import RECIPES

# ---------- CONFIG ----------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("keto_family_bot")

TOKEN = os.environ.get("TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "515415401").strip()  # Marcello Canova — recebe as sugestões

if not TOKEN:
    raise RuntimeError("TOKEN não configurado")

bot = telebot.TeleBot(TOKEN)

# Preenchido em runtime (configure_commands) com o @username do bot, usado pra montar os links de convite.
BOT_USERNAME = None

# TODO: quando o site (ketofamily.pro) estiver publicado, troque este link.
# Por enquanto aponta pro Linktree, que já concentra tudo (whitepaper, socials, CA, etc).
ECOSYSTEM_URL = "https://linktr.ee/ketofamilybros"

# ---------- CONTEÚDO (edite aqui sem tocar na lógica abaixo) ----------

WELCOME_TEXT = (
    "🥩🥑 *KETO FAMILY OFFICIAL BOT* 🔥\n\n"
    "👨 Dad - Picanha Master\n"
    "👩 Mom - Avocado Queen\n"
    "👧👦 Kids - Fitness Squad\n\n"
    "Choose below 👇"
)

WHAT_IS_KETO_TEXT = (
    "📘 *WHAT IS KETO?*\n\n"
    "https://www.dietdoctor.com/low-carb/keto"
)

# Infográfico próprio (6 passos, estilo da marca) — substitui o link externo.
WHAT_IS_KETO_IMAGE = os.path.join(os.path.dirname(__file__), "what_is_keto.jpg")
WHAT_IS_KETO_CAPTION = "📘 *WHAT IS KETO?*\n\nOur journey to ketosis, explained in 6 easy steps! 🥑🔥"

CALCULATOR_INTRO_TEXT = (
    "🧮 *KETO MACRO CALCULATOR*\n\n"
    "Send your weight in kg with the command, like this:\n"
    "`/macros 70`\n\n"
    "I'll calculate your daily protein, fat and carbs limit.\n\n"
    "Or just type /macros with nothing after it for the full guided version (weight, height, sex, age) — more accurate, includes estimated calories too."
)

MACROS_USAGE_TEXT = (
    "🧮 Usage: `/macros <weight in kg>` for a quick calc, or just `/macros` alone for the full guided version.\n"
    "Example: `/macros 70`"
)

# ---------- Macro Calculator guiada (peso → altura → sexo → idade) ----------

MACRO_STEPS = ["weight", "height", "sex", "age"]

MACRO_PROMPTS = {
    "weight": "🧮 *Macro Calculator*\n\nWhat's your current weight in kg?\n_(e.g. 70)_",
    "height": "📏 Got it! Now your height in cm?\n_(e.g. 175)_",
    "sex": "⚧️ Thanks. What's your sex — reply *M* or *F*?\n_(only used for the calorie estimate)_",
    "age": "🎂 Last one — what's your age?",
}

# chat_id -> {"step": int, "data": {...}}
awaiting_macro_flow = {}


def start_macro_flow(chat_id):
    awaiting_macro_flow[chat_id] = {"step": 0, "data": {}}
    bot.send_message(chat_id, MACRO_PROMPTS[MACRO_STEPS[0]], parse_mode="Markdown")


def compute_macro_result(data):
    weight = data["weight"]
    height = data["height"]
    sex = data["sex"]
    age = data["age"]

    # Mifflin-St Jeor — fórmula padrão pra estimar taxa metabólica basal (BMR)
    if sex == "M":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    tdee = bmr * 1.375  # estimativa assumindo atividade leve

    protein_g = round(weight * 1.5)
    carbs_g = 20  # fixo, pra manter cetose
    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4

    fat_cal_remaining = tdee - protein_cal - carbs_cal
    min_fat_g = round(weight * 0.6)  # mínimo de gordura essencial
    fat_g = max(round(fat_cal_remaining / 9), min_fat_g)

    sex_label = "male" if sex == "M" else "female"
    return (
        "🧮 *YOUR KETO MACROS*\n"
        f"_(based on {weight:g}kg, {height:g}cm, {age}y, {sex_label})_\n\n"
        f"🔥 Estimated maintenance: *{round(tdee)} kcal/day*\n\n"
        f"🥩 Protein: *{protein_g} g/day*\n"
        f"🥑 Fat: *{fat_g} g/day*\n"
        f"🥦 Carbs: *under {carbs_g} g/day*\n\n"
        "This is an estimate assuming light activity — adjust based on your real results over 2-3 weeks."
    )

CHAT_CHANNEL_TEXT = (
    "💬 *CHAT & CHANNEL*\n\n"
    "📲 Chat: t.me/ketofamilychat\n"
    "📢 Channel: t.me/ketofamilybros\n\n"
    "Hold $KETO for VIP! 🚀"
)

MOTIVATION_QUOTES = [
    "💪 Family that trains together, stays together!",
    "🔥 Burn fat, not carbs!",
    "⚡ Zero sugar = 100% focus!",
]

ABOUT_TEXTO = "👨‍👩‍👧‍👦 KETO FAMILY is lifestyle! Keto + Family + Gains!"

SUGGESTION_PROMPT = (
    "💡 *Got an idea for Keto Family?*\n\n"
    "Type it and send — it goes straight to the team!"
)

SUGGESTION_THANKS = "✅ Thanks! Your suggestion was sent to the team. 🥑"

# Guarda quem está no meio de mandar uma sugestão (chat_id -> True)
awaiting_suggestion = set()

# ---------- TECLADOS ----------
# Estrutura: menu principal (3 pastas + Suggestions) -> cada pasta abre um submenu.

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🥑 Health and diet", callback_data="folder:health"),
        types.InlineKeyboardButton("👥 Community", callback_data="folder:community"),
        types.InlineKeyboardButton("🚀 Project", callback_data="folder:project"),
    )
    markup.add(
        types.InlineKeyboardButton("💡 Suggestions", callback_data="menu:suggestions")
    )
    return markup


def health_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🍽️ Recipes", callback_data="folder:recipes"),
        types.InlineKeyboardButton("📘 What is keto", callback_data="item:whatiskto"),
        types.InlineKeyboardButton("🧮 Macro Calculator", callback_data="action:macroflow"),
    )
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="menu:back"))
    return markup


def recipes_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, cat in RECIPES.items():
        markup.add(types.InlineKeyboardButton(cat["label"], callback_data=f"reccat:{key}"))
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="folder:health"))
    return markup


def recipe_category_menu(catkey):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for idx, (title, _text) in enumerate(RECIPES[catkey]["items"]):
        markup.add(types.InlineKeyboardButton(title, callback_data=f"recipe:{catkey}:{idx}"))
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="folder:recipes"))
    return markup


def recipe_detail_markup(catkey):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"reccat:{catkey}"))
    return markup


def community_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔥 Daily Check-in", callback_data="action:checkin"),
        types.InlineKeyboardButton("💬 Chat and channel", callback_data="item:chatchannel"),
        types.InlineKeyboardButton("💪 Motivation", callback_data="item:motivation"),
        types.InlineKeyboardButton("🎵 TikTok", url="https://tiktok.com/@ketofamily1"),
    )
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="menu:back"))
    return markup


def project_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🌐 Ecosystem & Roadmap", url=ECOSYSTEM_URL)
    )
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="menu:back"))
    return markup


def back_to_folder(folder):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"folder:{folder}"))
    return markup


FOLDER_MENUS = {
    "health": ("🥑 *Health and diet* — pick one:", health_menu),
    "community": ("👥 *Community* — pick one:", community_menu),
    "project": ("🚀 *Project* — pick one:", project_menu),
    "recipes": ("🍽️ *Recipes* — pick a category:", recipes_menu),
}

# item_key -> (text, parse_mode, parent_folder)
ITEMS = {
    "calculator": (CALCULATOR_INTRO_TEXT, "Markdown", "health"),
    "chatchannel": (CHAT_CHANNEL_TEXT, "Markdown", "community"),
    "motivation": (None, None, "community"),  # texto sorteado na hora
    "about": (ABOUT_TEXTO, None, "community"),
}

# ---------- HANDLERS ----------

def close_photo_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="action:closephoto"))
    return markup


def send_what_is_keto(chat_id):
    try:
        with open(WHAT_IS_KETO_IMAGE, "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=WHAT_IS_KETO_CAPTION,
                parse_mode="Markdown",
                reply_markup=close_photo_markup(),
            )
    except FileNotFoundError:
        log.error(f"Imagem não encontrada: {WHAT_IS_KETO_IMAGE}")
        bot.send_message(
            chat_id, WHAT_IS_KETO_TEXT, parse_mode="Markdown", reply_markup=back_to_folder("health")
        )


@bot.message_handler(commands=["start"])
def start(message):
    awaiting_suggestion.discard(message.chat.id)
    # Garante que o usuário já existe na base de pontos (sem bônus/referral por enquanto — isso vem no próximo passo).
    store.get_or_create_user(message.chat.id, message.from_user.username)
    bot.send_message(
        message.chat.id, WELCOME_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
    )


def format_checkin_result(result):
    if not result.get("ok"):
        return "⚠️ Something went wrong, try /start first."

    if result["already_done"]:
        return (
            "✅ You already checked in today!\n\n"
            f"🔥 Current streak: *{result['streak']} day(s)*\n"
            f"⭐ Total points: *{result['total_points']}*"
        )

    bonus_line = f"\n🎁 Streak bonus: *+{result['bonus']} pts!*" if result["bonus"] else ""
    return (
        "✅ *Check-in confirmed!*\n\n"
        f"+{result['points_earned']} pts{bonus_line}\n"
        f"🔥 Streak: *{result['streak']} day(s)*\n"
        f"⭐ Total points: *{result['total_points']}*\n\n"
        "Come back tomorrow to keep your streak alive!"
    )


@bot.message_handler(commands=["checkin"])
def checkin_cmd(message):
    store.get_or_create_user(message.chat.id, message.from_user.username)
    result = store.do_checkin(message.chat.id)
    bot.reply_to(message, format_checkin_result(result), parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.chat.id in awaiting_macro_flow, content_types=["text"])
def macro_flow_step(message):
    chat_id = message.chat.id
    state = awaiting_macro_flow[chat_id]
    step_name = MACRO_STEPS[state["step"]]
    text = message.text.strip()

    if step_name == "weight":
        try:
            weight = float(text.replace(",", "."))
            if not (0 < weight <= 400):
                raise ValueError
        except ValueError:
            bot.reply_to(message, "⚠️ Enter a valid weight in kg (e.g. 70).")
            return
        state["data"]["weight"] = weight

    elif step_name == "height":
        try:
            height = float(text.replace(",", "."))
            if not (100 <= height <= 250):
                raise ValueError
        except ValueError:
            bot.reply_to(message, "⚠️ Enter a valid height in cm (e.g. 175).")
            return
        state["data"]["height"] = height

    elif step_name == "sex":
        t = text.strip().lower()
        if t in ("m", "male", "masculino", "homem", "h"):
            state["data"]["sex"] = "M"
        elif t in ("f", "female", "feminino", "mulher"):
            state["data"]["sex"] = "F"
        else:
            bot.reply_to(message, "⚠️ Please reply just *M* or *F*.", parse_mode="Markdown")
            return

    elif step_name == "age":
        try:
            age = int(text)
            if not (10 <= age <= 100):
                raise ValueError
        except ValueError:
            bot.reply_to(message, "⚠️ Enter a valid age (e.g. 30).")
            return
        state["data"]["age"] = age

        result_text = compute_macro_result(state["data"])
        del awaiting_macro_flow[chat_id]
        bot.send_message(chat_id, result_text, reply_markup=main_menu(), parse_mode="Markdown")
        return

    state["step"] += 1
    bot.send_message(chat_id, MACRO_PROMPTS[MACRO_STEPS[state["step"]]], parse_mode="Markdown")


def safe_edit_text(chat_id, message_id, text, reply_markup=None, parse_mode=None):
    """Edita a mensagem como texto. Se a mensagem original for uma foto
    (ex: a tela do 'What is keto'), o Telegram não deixa editar pra texto —
    nesse caso apaga a foto e manda uma mensagem de texto nova no lugar."""
    try:
        bot.edit_message_text(
            text, chat_id, message_id, reply_markup=reply_markup, parse_mode=parse_mode
        )
    except Exception as e:
        log.warning(f"edit_message_text falhou, reenviando como mensagem nova: {e}")
        try:
            bot.delete_message(chat_id, message_id)
        except Exception:
            pass
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)


@bot.callback_query_handler(func=lambda c: True)
def callback(callback):
    try:
        data = callback.data
        chat_id = callback.message.chat.id

        if data == "menu:back":
            awaiting_suggestion.discard(chat_id)
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                WELCOME_TEXT,
                reply_markup=main_menu(),
                parse_mode="Markdown",
            )

        elif data.startswith("folder:"):
            folder = data.split(":", 1)[1]
            text, menu_fn = FOLDER_MENUS[folder]
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                text,
                reply_markup=menu_fn(),
                parse_mode="Markdown",
            )

        elif data.startswith("reccat:"):
            catkey = data.split(":", 1)[1]
            cat = RECIPES[catkey]
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                f"{cat['label']} — pick a recipe:",
                reply_markup=recipe_category_menu(catkey),
                parse_mode="Markdown",
            )

        elif data.startswith("recipe:"):
            _, catkey, idx = data.split(":", 2)
            title, text = RECIPES[catkey]["items"][int(idx)]
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                text,
                reply_markup=recipe_detail_markup(catkey),
                parse_mode="Markdown",
            )

        elif data == "item:whatiskto":
            bot.answer_callback_query(callback.id)
            send_what_is_keto(chat_id)

        elif data == "action:closephoto":
            bot.answer_callback_query(callback.id)
            try:
                bot.delete_message(chat_id, callback.message.message_id)
            except Exception as e:
                log.warning(f"Não consegui apagar a foto, escondendo os botões: {e}")
                try:
                    bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
                except Exception:
                    pass

        elif data.startswith("item:"):
            key = data.split(":", 1)[1]
            text, parse_mode, parent = ITEMS[key]
            if key == "motivation":
                text = random.choice(MOTIVATION_QUOTES)
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                text,
                reply_markup=back_to_folder(parent),
                parse_mode=parse_mode,
            )

        elif data == "action:macroflow":
            bot.answer_callback_query(callback.id)
            start_macro_flow(chat_id)

        elif data == "action:checkin":
            store.get_or_create_user(chat_id, callback.from_user.username)
            result = store.do_checkin(chat_id)
            bot.answer_callback_query(callback.id)
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                format_checkin_result(result),
                reply_markup=back_to_folder("community"),
                parse_mode="Markdown",
            )

        elif data == "menu:suggestions":
            awaiting_suggestion.add(chat_id)
            bot.answer_callback_query(callback.id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="menu:back"))
            safe_edit_text(
                chat_id,
                callback.message.message_id,
                SUGGESTION_PROMPT,
                reply_markup=markup,
                parse_mode="Markdown",
            )

        else:
            bot.answer_callback_query(callback.id)

    except Exception as e:
        log.error(f"Erro no callback '{callback.data}': {e}")
        try:
            bot.answer_callback_query(callback.id, "Something went wrong, try again.")
        except Exception:
            pass


@bot.message_handler(commands=["recipes", "receitas"])
def recipes_cmd(message):
    bot.send_message(
        message.chat.id,
        "🍽️ *Recipes* — pick a category:",
        reply_markup=recipes_menu(),
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["motivation", "motivacao"])
def motivation_cmd(message):
    bot.reply_to(message, random.choice(MOTIVATION_QUOTES))


@bot.message_handler(commands=["about", "sobre"])
def about_cmd(message):
    bot.reply_to(message, ABOUT_TEXTO)


@bot.message_handler(commands=["dieta", "keto", "diet"])
def dieta_links(message):
    send_what_is_keto(message.chat.id)
    bot.send_message(
        message.chat.id,
        f"{CALCULATOR_INTRO_TEXT}\n\n{CHAT_CHANNEL_TEXT}",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["macros"])
def macros_cmd(message):
    parts = message.text.strip().split()

    if len(parts) < 2:
        start_macro_flow(message.chat.id)
        return

    raw_weight = parts[1].replace(",", ".")

    try:
        weight = float(raw_weight)
    except ValueError:
        bot.reply_to(
            message,
            f"⚠️ '{parts[1]}' doesn't look like a number.\n\n{MACROS_USAGE_TEXT}",
            parse_mode="Markdown",
        )
        return

    if weight <= 0 or weight > 400:
        bot.reply_to(
            message,
            f"⚠️ That weight doesn't look right. Enter your weight in kg (e.g. 70).\n\n{MACROS_USAGE_TEXT}",
            parse_mode="Markdown",
        )
        return

    protein_g = round(weight * 1.5)
    fat_g = round(weight * 1)
    carbs_g = 20  # limite fixo pra manter cetose, independente do peso

    result_text = (
        f"🧮 *YOUR KETO MACROS* (based on {weight:g} kg)\n\n"
        f"🥩 Protein: *{protein_g} g/day*\n"
        f"🥑 Fat: *{fat_g} g/day*\n"
        f"🥦 Carbs: *under {carbs_g} g/day*\n\n"
        f"Build & repair muscle · Energy & satiety · Stay in ketosis"
    )
    bot.reply_to(message, result_text, parse_mode="Markdown")


@bot.message_handler(commands=["suggestions", "sugestao", "sugestoes"])
def suggestions_cmd(message):
    awaiting_suggestion.add(message.chat.id)
    bot.reply_to(message, SUGGESTION_PROMPT, parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.chat.id in awaiting_suggestion, content_types=["text"])
def capture_suggestion(message):
    awaiting_suggestion.discard(message.chat.id)

    if ADMIN_CHAT_ID:
        try:
            user = message.from_user
            username = f"@{user.username}" if user.username else user.first_name
            bot.send_message(
                ADMIN_CHAT_ID,
                f"💡 New suggestion from {username} (id {user.id}):\n\n{message.text}",
            )
        except Exception as e:
            log.error(f"Não consegui encaminhar sugestão: {e}")

    bot.reply_to(message, SUGGESTION_THANKS, reply_markup=main_menu())


WELCOME_DELETE_DELAY = 15  # segundos até a msg de boas-vindas ser apagada


def _delete_after_delay(chat_id, message_id, delay=WELCOME_DELETE_DELAY):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        log.error(f"Erro ao apagar mensagem de boas-vindas: {e}")


@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message):
    bot_id = bot.get_me().id
    for new_user in message.new_chat_members:
        if new_user.id == bot_id:
            continue  # o próprio bot foi adicionado ao grupo, ignora

        name = new_user.first_name or "friend"
        text = (
            f"👋 Welcome to Keto Family, {name}!\n\n"
            f"Here you'll find low-carb recipes, a macro calculator, daily check-ins "
            f"and the latest project updates. Pick an option below 👇"
        )
        try:
            sent = bot.send_message(message.chat.id, text, reply_markup=main_menu())
        except Exception as e:
            log.error(f"Erro ao enviar boas-vindas: {e}")
            continue

        threading.Thread(
            target=_delete_after_delay,
            args=(message.chat.id, sent.message_id),
            daemon=True,
        ).start()


@bot.message_handler(func=lambda m: True, content_types=["text"])
def fallback(message):
    bot.reply_to(message, "Use /start to open the menu 👇", reply_markup=main_menu())


# ---------- SETUP ----------

def configure_commands():
    bot.set_my_commands([
        types.BotCommand("start", "Open the KETO FAMILY menu"),
        types.BotCommand("recipes", "Get the recipes link"),
        types.BotCommand("motivation", "Get a motivation message"),
        types.BotCommand("about", "About KETO FAMILY"),
        types.BotCommand("diet", "Open the Keto diet guide"),
        types.BotCommand("macros", "Guided macro calculator (or /macros 70 for a quick calc)"),
        types.BotCommand("checkin", "Daily check-in — earn points and build your streak"),
        types.BotCommand("suggestions", "Send an idea to the team"),
    ])


from keep_alive import keep_alive

if __name__ == "__main__":
    keep_alive()
    log.info("Bot Keto Family ATIVO!")
    try:
        configure_commands()
    except Exception as e:
        log.error(f"Erro ao configurar comandos: {e}")

    # Loop que nunca deixa o bot morrer
    while True:
        try:
            log.info("Iniciando polling...")
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            log.error(f"Bot caiu com erro: {e} - Reiniciando em 5s...")
            import time
            time.sleep(5)
