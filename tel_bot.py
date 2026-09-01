import sys
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from engine.game_engine import game_engine


logging.basicConfig(level=logging.INFO)

async def send_scene(update_or_query, scene_data):
    """تابع کمکی برای نمایش صحنه و دکمه‌ها"""
    text = scene_data.get("text", "بدون متن")
    buttons = scene_data.get("buttons", [])
    
    keyboard = []
    for i, btn_text in enumerate(buttons, start=1):
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"choice_{i}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    
    if hasattr(update_or_query, 'edit_message_text'):
        await update_or_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update_or_query.message.reply_text(text=text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    scene = game_engine.start(user_id)
    await send_scene(update, scene)

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    index = int(query.data.split("_")[1])
    
    user_id = query.from_user.id
    new_scene = game_engine.choose(user_id, index)
    
    await send_scene(query, new_scene)

def main():
    # توکن ربات خود را اینجا قرار دهید
    TOKEN = "8611849223:AAF4xRxd9Pi2zWx0eWsVUUnxc5rZM_k2m7s"
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_choice, pattern="^choice_"))
    
    print("ربات در حال اجراست...")
    app.run_polling()

if __name__ == '__main__':
    main()
