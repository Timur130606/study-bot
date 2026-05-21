import logging
import random
from datetime import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ─── НАСТРОЙКИ ───────────────────────────────────────────────
BOT_TOKEN = "ВСТАВЬ_СЮДА_СВОЙ_TOKEN"  # Получи у @BotFather в Telegram

REMINDER_HOUR = 9    # Час отправки напоминания (по UTC+5 = Алматы)
REMINDER_MINUTE = 0  # Минута отправки

# ─── УТРЕННИЕ НАПОМИНАНИЯ ─────────────────────────────────────
REMINDERS = [
    "🌅 Доброе утро! Сегодня ещё один шанс стать лучше. Открой конспект на 20 минут — это твой старт дня.",
    "☀️ Привет! Помни: успех — это сумма маленьких ежедневных усилий. Что ты выучишь сегодня?",
    "📚 Утро! Твои конкуренты уже учатся. Не давай им фору — открой учебник прямо сейчас.",
    "🎯 Новый день — новые знания. Один час учёбы сегодня = большое преимущество завтра.",
    "💡 Доброе утро! Самые успешные люди учатся каждый день. Ты на правильном пути — не останавливайся!",
    "🚀 Подъём! Сегодня — отличный день, чтобы освоить что-то новое. Начни с 25 минут по технике Помодоро.",
    "🏆 Привет, чемпион! Помни свою цель. Учёба сегодня — это твоя свобода завтра.",
    "⚡ Доброе утро! Мозг лучше всего усваивает информацию с утра. Используй это время — повтори вчерашний материал.",
]

# ─── СОВЕТЫ ПО ТЕМАМ ─────────────────────────────────────────
ADVICE = {
    "монтаж": [
        "🎬 Совет по монтажу: изучи принцип '3-секундного правила' для Reels — первые 3 секунды решают всё. Практикуй крючки в начале каждого ролика.",
        "✂️ Монтаж: попробуй CapCut AI и Runway ML — они автоматически нарезают лучшие моменты. Это твоё конкурентное преимущество прямо сейчас.",
        "🎵 Лайфхак: синхронизируй монтажные cuts с битом музыки — ролики с этим набирают в 2-3 раза больше просмотров.",
    ],
    "нейросети": [
        "🤖 ИИ-совет: изучи сегодня Midjourney для генерации обложек и превью к видео. Клиенты платят 5-15$ за одну обложку.",
        "💻 Нейросети: ChatGPT + специальный промпт = готовый сценарий для видео за 2 минуты. Я могу помочь составить промпт!",
        "🧠 Тренд: освой Sora или Kling AI для генерации видео-клипов — монтажёры, знающие AI, зарабатывают в 3x больше.",
    ],
    "фриланс": [
        "💼 Фриланс-совет: обнови профиль на Kwork прямо сегодня. Добавь 3 примера работ — это увеличивает конверсию на 70%.",
        "📧 Напиши 3 холодных сообщения бизнесам в Instagram сегодня. Статистика: каждое 10-е сообщение = заказ.",
        "💰 Совет: подними цену на услуги на 20%. Часто низкая цена отпугивает серьёзных клиентов.",
    ],
    "мотивация": [
        "🔥 Ты уже делаешь больше, чем большинство — просто учишься и развиваешься. Продолжай!",
        "💪 Трудный период временный, а навыки останутся навсегда. Каждый час учёбы — инвестиция в себя.",
        "🌟 В 19 лет ты уже умеешь монтировать, знаешь AI, занимаешься творчеством. Это серьёзный багаж — используй его!",
    ],
}

# ─── ОБРАБОТЧИКИ КОМАНД ───────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Сохраняем chat_id для ежедневных напоминаний
    if "subscribers" not in context.bot_data:
        context.bot_data["subscribers"] = set()
    context.bot_data["subscribers"].add(chat_id)

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        "Я твой личный советник по учёбе и карьере.\n\n"
        "Что я умею:\n"
        "📅 Каждое утро буду присылать тебе мотивационное напоминание\n"
        "🎓 Дам совет по любой теме\n"
        "🤖 Помогу с планированием и вопросами\n\n"
        "Команды:\n"
        "/совет — случайный совет дня\n"
        "/монтаж — совет по видеомонтажу\n"
        "/нейросети — совет по AI\n"
        "/фриланс — совет по поиску работы\n"
        "/мотивация — заряд энергии\n"
        "/план — составить план на день\n"
        "/стоп — отписаться от напоминаний\n\n"
        "Или просто напиши мне любой вопрос — я отвечу! 💬"
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if "subscribers" in context.bot_data:
        context.bot_data["subscribers"].discard(chat_id)
    await update.message.reply_text("Напоминания отключены. Напиши /start чтобы включить снова.")

async def sovet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_tips = [tip for tips in ADVICE.values() for tip in tips]
    await update.message.reply_text(random.choice(all_tips))

async def topic_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.lstrip("/").split()[0].lower()
    tips = ADVICE.get(command, [])
    if tips:
        await update.message.reply_text(random.choice(tips))
    else:
        await update.message.reply_text("Команда не найдена. Попробуй /совет")

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Составим план на сегодня!\n\n"
        "Расскажи мне:\n"
        "1. Сколько у тебя свободных часов сегодня?\n"
        "2. Что самое важное нужно сделать?\n"
        "3. Что ты хочешь выучить или попрактиковать?\n\n"
        "Напиши ответы, и я помогу распределить время! ⏰"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    # Простые ключевые слова для ответов
    if any(w in text for w in ["устал", "лень", "не хочу", "скучно"]):
        await update.message.reply_text(
            "😴 Понимаю это чувство. Попробуй технику «2 минуты»: \n"
            "открой учебник/туториал и позволь себе закрыть через 2 минуты.\n"
            "Обычно, когда начинаешь — втягиваешься. Попробуй? 💪"
        )
    elif any(w in text for w in ["работа", "заказ", "клиент", "деньги", "заработать"]):
        await update.message.reply_text(
            "💼 По поводу работы — вот твой план действий:\n\n"
            "1️⃣ Сегодня: зарегистрируйся на Kwork.ru\n"
            "2️⃣ Выстави услугу монтажа Reels (от 500₽)\n"
            "3️⃣ Найди 5 бизнесов в Instagram и напиши им\n\n"
            "Хочешь, помогу составить текст оффера? Просто напиши «напиши оффер» 📝"
        )
    elif "оффер" in text or "сообщение клиенту" in text:
        await update.message.reply_text(
            "📝 Вот шаблон сообщения для бизнеса:\n\n"
            "---\n"
            "Привет! Я видеомонтажёр, специализируюсь на Reels и контенте для Instagram.\n\n"
            "Заметил твой аккаунт — думаю, с правильными роликами можно сильно увеличить охваты.\n\n"
            "Готов сделать 1 тестовый Reels бесплатно, чтобы ты увидел качество.\n\n"
            "Интересно?\n"
            "---\n\n"
            "Адаптируй под конкретный бизнес — упомяни что-то конкретное об их аккаунте 🎯"
        )
    elif any(w in text for w in ["спасибо", "благодарю", "круто", "отлично"]):
        await update.message.reply_text("Всегда рад помочь! 🙌 Продолжай в том же духе!")
    else:
        await update.message.reply_text(
            "Интересный вопрос! 🤔\n\n"
            "Я пока учусь понимать все темы, но вот что могу предложить:\n\n"
            "• /совет — случайный полезный совет\n"
            "• /монтаж — по видеомонтажу\n"
            "• /нейросети — по AI инструментам\n"
            "• /фриланс — по поиску клиентов\n"
            "• /план — составить план дня\n\n"
            "Или уточни свой вопрос подробнее! 💬"
        )

# ─── ЕЖЕДНЕВНОЕ НАПОМИНАНИЕ ───────────────────────────────────
async def send_daily_reminder(context: ContextTypes.DEFAULT_TYPE):
    subscribers = context.bot_data.get("subscribers", set())
    message = random.choice(REMINDERS)
    for chat_id in subscribers:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logging.warning(f"Не удалось отправить напоминание {chat_id}: {e}")

# ─── ЗАПУСК БОТА ─────────────────────────────────────────────
def main():
    logging.basicConfig(level=logging.INFO)

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("стоп", stop))
    app.add_handler(CommandHandler("совет", sovet))
    app.add_handler(CommandHandler("монтаж", topic_advice))
    app.add_handler(CommandHandler("нейросети", topic_advice))
    app.add_handler(CommandHandler("фриланс", topic_advice))
    app.add_handler(CommandHandler("мотивация", topic_advice))
    app.add_handler(CommandHandler("план", plan))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ежедневное напоминание в 9:00 по Алматы (UTC+5 = 4:00 UTC)
    app.job_queue.run_daily(
        send_daily_reminder,
        time=time(hour=4, minute=0),  # 04:00 UTC = 09:00 Алматы
    )

    print("Бот запущен! Нажми Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
