from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import itertools

# =============================
# CONFIGURATION
# =============================
TOKEN = "8282083267:AAENF1hlggsOZ6G_u6C8x2l8afw-Dt18-xI"   # <-- ដាក់ TOKEN ពិតពី BotFather
SOURCE_GROUP_ID = -1002943091860    # <-- ដាក់ Group ID របស់អ្នក

# បញ្ជីវីដេអូ (ប្រើ file_id ឬវីដេអូដែលយកពី group)
video_list = [
    "BAACAgUAAxkBAAEB12345examplevideo1",
    "BAACAgUAAxkBAAEB12346examplevideo2",
    "BAACAgUAAxkBAAEB12347examplevideo3"
]

# =============================
# MEMORY
# =============================
user_language = {}
video_queue = {}

# =============================
# FUNCTIONS
# =============================

# 1️⃣ START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ភាសាខ្មែរ 🇰🇭", callback_data='lang_kh')],
        [InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')]
    ]
    await update.message.reply_text(
        "Please select your language / សូមជ្រើសរើសភាសា៖",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 2️⃣ LANGUAGE SELECTION
async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data
    user_language[query.from_user.id] = lang

    if lang == 'lang_kh':
        text = "ជ្រើសរើសមុខងារ៖"
        btn_send = "ផ្ញើវីដេអូ 📹"
        btn_join = "ចូលជាផ្លូវការ 📢"
    else:
        text = "Choose an option:"
        btn_send = "Send Video 📹"
        btn_join = "Join Channel 📢"

    keyboard = [
        [InlineKeyboardButton(btn_send, callback_data='send_video')],
        [InlineKeyboardButton(btn_join, url="https://t.me/YourChannelLink")]
    ]
    await query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(keyboard))

# 3️⃣ SEND VIDEO
async def send_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id not in video_queue:
        video_queue[user_id] = itertools.cycle(video_list)

    next_video = next(video_queue[user_id])
    await context.bot.send_video(chat_id=user_id, video=next_video)

    lang = user_language.get(user_id, 'lang_en')
    btn = "ផ្ញើវីដេអូបន្ថែម ▶️" if lang == 'lang_kh' else "Send More Video ▶️"
    keyboard = [[InlineKeyboardButton(btn, callback_data='send_more')]]
    await context.bot.send_message(chat_id=user_id, text="", reply_markup=InlineKeyboardMarkup(keyboa
