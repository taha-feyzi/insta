import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "7592032083:AAExDpAAFm9C2OmcDikNpRC_IAllzT_vbCA"
ADMIN_CHAT_ID = "6280971679"  # آیدی چت ادمین را اینجا قرار دهید

# متغیرهای آمار
download_requests = 0
successful_downloads = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! لینک ویدیو اینستاگرام رو برام ارسال کن تا برات دانلود کنم.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global download_requests, successful_downloads
    url = update.message.text
    chat_id = update.effective_chat.id

    download_requests += 1  # شمارش درخواست دانلود

    if "instagram.com" not in url:
        await update.message.reply_text("فقط لینک‌های معتبر اینستاگرام پذیرفته می‌شوند.")
        return

    await update.message.reply_text("به ایلیا گفتم بره ویدیو رو بیاره @F7LAsh8 ...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            file_name = f"{video_info['title']}.{video_info['ext']}"

            with open(file_name, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=video_file,
                    caption="ویدیو رو پیدا کرد و تقدیم شما کرد!")

            os.remove(file_name)
            successful_downloads += 1  # شمارش دانلود موفق

    except Exception as e:
        await update.message.reply_text("در دانلود ویدیو مشکلی پیش آمد. لطفاً دوباره امتحان کنید.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) == ADMIN_CHAT_ID:  # بررسی اینکه آیا کاربر ادمین است یا نه
        stats_message = (
            f"تعداد درخواست‌های دانلود: {download_requests}\n"
            f"تعداد دانلودهای موفق: {successful_downloads}"
        )
        await update.message.reply_text(stats_message)
    else:
        await update.message.reply_text("شما دسترسی به این اطلاعات را ندارید.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'خطایی رخ داده: {context.error}')
    await update.message.reply_text("مشکلی رخ داد. لطفاً دوباره تلاش کنید.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^https://www.instagram.com'), download_video))
    app.add_handler(CommandHandler("stats", stats))  # اضافه کردن دستور آمار
    app.add_error_handler(error_handler)

    print("ربات شروع به کار کرد...")
    app.run_polling()

if __name__ == '__main__':
    main()
