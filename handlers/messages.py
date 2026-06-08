import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.ai import get_ai_response, clear_history

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    clear_history(chat_id)
    await update.message.reply_text(
        "👋 Привет! Я AI-ассистент компании **Центр красок #1**.\n\n"
        "Я помогу вам узнать:\n"
        "- Какие товары и бренды есть в наличии\n"
        "- Где мы работаем и как связаться\n"
        "- Режим работы магазина\n"
        "- Ответы на другие вопросы о компании\n\n"
        "Просто напишите ваш вопрос в свободной форме!",
        parse_mode="Markdown",
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clear_history(update.effective_chat.id)
    await update.message.reply_text(
        "История диалога очищена. Начнём сначала! Задайте ваш вопрос."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text.strip()
    if not user_text:
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    logger.info(f"[chat_id={chat_id}] User: {user_text}")

    response = get_ai_response(chat_id, user_text)
    logger.info(f"[chat_id={chat_id}] Bot: {response[:80]}...")

    await update.message.reply_text(response, parse_mode="Markdown")


async def handle_non_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Я понимаю только текстовые сообщения. "
        "Напишите ваш вопрос о компании «Центр красок #1»!"
    )
