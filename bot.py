import os
import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from school_data import search_schools_by_eiin, search_schools_by_text

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("bd_school_info_bot")
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

HELP = (
    "BD School Info Bot\n\n"
    "/start — বট চালু\n/help — ব্যবহারবিধি\n"
    "/search নাম বা এলাকা — স্কুল খোঁজা\n"
    "/eiin 123456 — EIIN দিয়ে খোঁজা\n"
    "/district — জেলা/উপজেলা লিখে খোঁজা\n/about — বট সম্পর্কে\n\n"
    "এই সংস্করণে কেবল school_data.py-তে যোগ করা যাচাইকৃত তথ্য দেখানো হয়।"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "আসসালামু আলাইকুম! BD School Info Bot চালু হয়েছে।\n"
        "স্কুলের নাম বা EIIN লিখুন। সাহায্যের জন্য /help দিন।"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(HELP)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "এই বট স্কুলের প্রকাশ্য, যাচাইকৃত তথ্য খোঁজে। "
        "সরকারি তথ্যসূত্র যোগ না করা থাকলে কোনো ফলাফল বানিয়ে দেখায় না।"
    )

async def show_results(update: Update, query: str, results):
    if not results:
        await update.effective_message.reply_text(
            f"“{query}” এর জন্য বর্তমানে যোগ করা যাচাইকৃত ডেটায় ফলাফল নেই।\n"
            "স্কুলটি নেই—এমন সিদ্ধান্ত এর অর্থ নয়; ডেটাসেটে তথ্য যোগ করতে হবে।"
        )
        return
    lines = [f"🔎 ফলাফল: {query}", ""]
    for s in results[:10]:
        lines.extend([
            f"🏫 {s.get('name', 'নাম নেই')}",
            f"EIIN: {s.get('eiin', 'তথ্য নেই')}",
            f"ধরন: {s.get('school_type', 'তথ্য নেই')}",
            f"এলাকা: {s.get('upazila', 'তথ্য নেই')}, {s.get('district', 'তথ্য নেই')}",
            f"তথ্যসূত্র: {s.get('source_url', 'যোগ করা হয়নি')}",
        ])
        staff = s.get("staff", [])
        if staff:
            lines.append("প্রকাশ্য পেশাগত তথ্য:")
            for p in staff[:10]:
                lines.append(f"• {p.get('name', 'নাম নেই')} — {p.get('designation', 'পদবি নেই')}")
                if p.get("subject"):
                    lines.append(f"  বিষয়: {p['subject']}")
                if p.get("source_url"):
                    lines.append(f"  উৎস: {p['source_url']}")
        else:
            lines.append("এই ডেটায় শিক্ষক/কর্মচারীর যাচাইকৃত প্রকাশ্য তালিকা নেই।")
        lines.append("")
    await update.effective_message.reply_text("\n".join(lines), disable_web_page_preview=True)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = " ".join(context.args).strip()
    if not q:
        await update.effective_message.reply_text("ব্যবহার: /search স্কুলের নাম বা জেলা")
        return
    await show_results(update, q, search_schools_by_text(q))

async def eiin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = " ".join(context.args).strip()
    if not re.fullmatch(r"\d{4,8}", q):
        await update.effective_message.reply_text("ব্যবহার: /eiin 123456 (৪–৮ সংখ্যার EIIN)")
        return
    await show_results(update, q, search_schools_by_eiin(q))

async def district_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("জেলা বা উপজেলা লিখে পাঠান, যেমন: কুড়িগ্রাম বা নাগেশ্বরী।")

async def text_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = (update.effective_message.text or "").strip()
    if not q:
        return
    if re.fullmatch(r"\d{4,8}", q):
        results = search_schools_by_eiin(q)
    else:
        results = search_schools_by_text(q)
    await show_results(update, q, results)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Unhandled Telegram bot error: %s", context.error)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN সেট করা নেই। Render Environment-এ BOT_TOKEN যোগ করুন।")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("eiin", eiin_command))
    app.add_handler(CommandHandler("district", district_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_search))
    app.add_error_handler(error_handler)
    logger.info("BD School Info Bot starting")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
