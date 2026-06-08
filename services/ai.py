import logging
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_HISTORY_MESSAGES
from data.knowledge_base import get_knowledge_base

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = f"""Ты — вежливый и полезный AI-ассистент компании «Центр красок #1» в Казахстане.
Ты отвечаешь ТОЛЬКО на основе предоставленной информации о компании ниже.

ПРАВИЛА:
1. Отвечай только на вопросы, связанные с компанией и её продукцией.
2. Если вопрос не относится к компании — вежливо объясни, что ты ассистент «Центра красок #1» и можешь помочь только по теме компании.
3. Не придумывай информацию, которой нет в базе знаний.
4. Если точного ответа нет в базе знаний — честно скажи об этом и предложи связаться по телефону +7 (777) 292-84-01.
5. Отвечай на том языке, на котором написан вопрос (русский, казахский или английский).
6. Будь дружелюбным и лаконичным. Используй эмодзи умеренно.

ИНФОРМАЦИЯ О КОМПАНИИ:
{get_knowledge_base()}
"""

genai.configure(api_key=GEMINI_API_KEY)
_model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    system_instruction=SYSTEM_PROMPT,
)

_histories: dict[int, list] = {}


def get_ai_response(chat_id: int, user_message: str) -> str:
    if chat_id not in _histories:
        _histories[chat_id] = []

    history = _histories[chat_id]

    try:
        chat_session = _model.start_chat(history=history)
        response = chat_session.send_message(user_message)
        assistant_message = response.text

        updated = list(chat_session.history)
        if len(updated) > MAX_HISTORY_MESSAGES * 2:
            updated = updated[-(MAX_HISTORY_MESSAGES * 2):]
        _histories[chat_id] = updated

        return assistant_message

    except Exception as e:
        logger.error(f"Gemini error: {type(e).__name__}: {e}")
        error_str = str(e).lower()
        if "quota" in error_str or "limit" in error_str:
            return "Превышен лимит запросов. Попробуйте через минуту или свяжитесь с нами: +7 (777) 292-84-01"
        if "api_key" in error_str or "permission" in error_str:
            return "Ошибка авторизации AI. Обратитесь к администратору."
        return "Что-то пошло не так. Пожалуйста, попробуйте ещё раз."


def clear_history(chat_id: int) -> None:
    _histories.pop(chat_id, None)
