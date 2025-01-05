import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "7322283869:AAE-czVd2aSD4s8VR5yU4zDMsIA3U6PZD_E"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! لینک ویدیو اینستاگرام رو برام ارسال کن تا برات دانلود کنم."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.effective_chat.id
    
    if "instagram.com" not in url:
        await update.message.reply_text("فقط لینک‌های معتبر اینستاگرام پذیرفته می‌شوند.")
        return
    
    await update.message.reply_text("در حال پردازش و دانلود ویدیو، لطفاً منتظر بمانید...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            file_name = f"{video_info['title']}.{video_info['ext']}"
            
            with open(file_name, 'rb') as video_file:
                await context.bot.send_video(chat_id=chat_id, video=video_file, caption="ویدیو آماده است!")
            
            os.remove(file_name)
            
    except Exception as e:
        await update.message.reply_text("در دانلود ویدیو مشکلی پیش آمد. لطفاً دوباره امتحان کنید.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'خطایی رخ داده: {context.error}')
    await update.message.reply_text("مشکلی رخ داد. لطفاً دوباره تلاش کنید.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.add_error_handler(error_handler)
    
    print("ربات شروع به کار کرد...")
    app.run_polling()

if name == 'main':
    main()