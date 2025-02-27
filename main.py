import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import random
import re

# Настройка бота
TOKEN = ''  # Замени на токен твоего бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователей
user_data = {}

# Список вопросов (без описаний)
questions = [
    {
        "text": "Где вы хотели бы жить?",
        "options": {
            "В джунглях 🌳": {"сила": 5, "скорость": 4, "доброта": 1, "общительность": 1},
            "На Южном полюсе ❄️": {"сила": 1, "скорость": 2, "доброта": 5, "общительность": 6},
            "В саванне 🌄": {"сила": 8, "скорость": 3, "доброта": 2, "общительность": 2},
            "В тихом лесу 🌲": {"сила": 3, "скорость": 5, "доброта": 4, "общительность": 3},
        },
        "sticker": "CAACAgIAAxkBAAEM-5tnwDa7d6wvFB73SDzpQXIxgtvZswACDQEAAvR7GQABJ6-MCHZ-F9A2BA"
    },
    {
        "text": "Какая у вас любимая еда?",
        "options": {
            "Мясо 🍖": {"сила": 7, "скорость": 6, "доброта": 1, "общительность": 1},
            "Рыба 🐟": {"сила": 1, "скорость": 3, "доброта": 5, "общительность": 6},
            "Фрукты 🍌": {"сила": 2, "скорость": 4, "доброта": 7, "общительность": 3},
            "Овощи 🥕": {"сила": 3, "скорость": 5, "доброта": 2, "общительность": 1},
        },
        "sticker": "CAACAgIAAxkBAAEM-5lnwDZsXTCylUEXDtOrodb5-HbGgAACJwEAAlKJkSMTI3f3KnjQfTYE"
    },
    {
        "text": "Как вы предпочитаете проводить время?",
        "options": {
            "Активно 💪": {"сила": 6, "скорость": 7, "доброта": 2, "общительность": 1},
            "Спокойно 🛀": {"сила": 1, "скорость": 1, "доброта": 6, "общительность": 7},
            "Общаться с друзьями 👥": {"сила": 2, "скорость": 3, "доброта": 5, "общительность": 6},
            "Наблюдать за природой 🌿": {"сила": 3, "скорость": 5, "доброта": 8, "общительность": 2},
        },
        "sticker": "CAACAgIAAxkBAAEM-59nwDb8HSCU-54jPcCRWhsimBaScAACPQEAAvR7GQABTAIrXSxZ6IA2BA"
    },
    {
        "text": "Какое качество вам ближе всего?",
        "options": {
            "Сила 💪": {"сила": 8, "скорость": 2, "доброта": 1, "общительность": 1},
            "Ум 🧠": {"сила": 1, "скорость": 4, "доброта": 6, "общительность": 7},
            "Доброта ❤️": {"сила": 3, "скорость": 5, "доброта": 7, "общительность": 3},
            "Независимость 🚀": {"сила": 4, "скорость": 6, "доброта": 2, "общительность": 1},
        },
        "sticker": "CAACAgIAAxkBAAEM-51nwDbc1Ahp2KdyJibHHVQtHWZXFgAC6gAD9HsZAAFjsXea7HRT1zYE"
    },
    {
        "text": "Какую погоду вы любите?",
        "options": {
            "Тёплую ☀️": {"сила": 3, "скорость": 4, "доброта": 3, "общительность": 4},
            "Холодную ❄️": {"сила": 1, "скорость": 2, "доброта": 6, "общительность": 6},
            "Дождливую ⛈️": {"сила": 2, "скорость": 5, "доброта": 5, "общительность": 3},
            "Ветреную 🌬️": {"сила": 4, "скорость": 6, "доброта": 2, "общительность": 1},
        },
        "sticker": "CAACAgIAAxkBAAEM-6FnwDcVMgR87ehDGmQf3d6fSR2PZgAC8AAD9HsZAAEuvf-jtAjUeTYE"
    },
]

# Словарь животных и их характеристик
animals = {
    "тигр": {"сила": 6, "скорость": 8, "доброта": 2, "общительность": 1},  # Очень сильный и быстрый, но замкнутый
    "пингвин": {"сила": 1, "скорость": 3, "доброта": 6, "общительность": 7},  # Низкая сила, высокая доброта и общительность
    "слон": {"сила": 9, "скорость": 1, "доброта": 4, "общительность": 3},  # Самое сильное, медленное, умеренно доброе
    "лиса": {"сила": 3, "скорость": 3, "доброта": 8, "общительность": 3},  # Хитрая, быстрая и очень добрая, но менее общительная
    "змея": {"сила": 4, "скорость": 7, "доброта": 1, "общительность": 1},  # Быстрая, но недобрая и замкнутая
}

# Логирование
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Функция для начала викторины
@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id

    # Отправляем описание бота и программы опеки
    intro_message = (
        "Добро пожаловать в викторину «Какое у вас тотемное животное?»!\n\n"
        "Этот бот создан для популяризации программы опеки нашего зоопарка. Пройдите викторину, чтобы узнать, какое животное лучше всего отражает ваши черты характера.\n\n"
        "Программа опеки позволяет каждому стать опекуном выбранного животного. Ваши средства помогут обеспечить ему лучший уход, питание и комфорт. После прохождения викторины вы сможете узнать больше о программе!"
    )
    bot.send_message(chat_id, intro_message)

    # Инициализация данных пользователя
    user_data[chat_id] = {
        "scores": {"сила": 0, "скорость": 0, "доброта": 0, "общительность": 0},
        "current_question": 0,
        "awaiting_feedback": False,
        "awaiting_email": False,
        "best_animal": None
    }
    ask_question(chat_id)

# Функция для задания вопроса
def ask_question(chat_id):
    user_info = user_data.get(chat_id)
    if not user_info or user_info["current_question"] >= len(questions):  # Проверяем индекс вопроса
        show_result(chat_id)
        return

    question = questions[user_info["current_question"]]
    keyboard = InlineKeyboardMarkup()
    for option in question["options"]:
        keyboard.add(InlineKeyboardButton(option, callback_data=option))

    bot.send_message(chat_id, question["text"], reply_markup=keyboard)

    # Отправляем стикер после вопроса
    sticker_id = question.get("sticker")
    if sticker_id:
        bot.send_sticker(chat_id, sticker_id)

# Обработка ответов
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    user_info = user_data.get(chat_id)

    if not user_info:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново /start")
        return

    answer = call.data
    current_question_index = user_info["current_question"]

    if current_question_index < len(questions):  # Проверяем, что вопросы ещё есть
        question = questions[current_question_index]
        for key, value in question["options"][answer].items():
            user_info["scores"][key] += value

        user_info["current_question"] += 1
        ask_question(chat_id)
    else:
        button_handler(call)  # Если вопросы закончились, обрабатываем кнопки

# Показ результата
def show_result(chat_id):
    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново /start")
        return

    scores = user_info["scores"]
    best_animal = min(animals, key=lambda animal: sum(abs(scores[key] - animals[animal][key]) for key in scores))

    result_message = f"Ваше тотемное животное — {best_animal.capitalize()}! 🎉"

    # Отправляем изображение животного
    image_path = os.path.join("images", f"{best_animal}.jpeg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as photo:
            bot.send_photo(chat_id, photo, caption=result_message)
    else:
        bot.send_message(chat_id, result_message + "\n\nК сожалению, изображение недоступно.")

    # Мини-интро о программе опеки вместе с результатом
    patronage_intro = (
        f"Поздравляем! Вы можете поддержать {best_animal.capitalize()} через нашу программу опеки.\n\n"
        "Присоединяйтесь к программе опеки и помогите вашему тотемному животному чувствовать себя лучше!\n"
        "Нажмите кнопку «Узнать больше» для получения подробной информации."
    )
    bot.send_message(chat_id, patronage_intro)

    # Кнопки для действий после викторины
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Поделиться результатом", switch_inline_query=f"Мое тотемное животное: {best_animal}"),
        InlineKeyboardButton("Связаться с зоопарком", callback_data="contact_zoo")
    )
    keyboard.row(
        InlineKeyboardButton("Попробовать ещё раз?", callback_data="restart_quiz"),
        InlineKeyboardButton("Оставить отзыв", callback_data="leave_feedback")
    )
    keyboard.row(
        InlineKeyboardButton("Узнать больше о программе опеки", callback_data="patronage_info")
    )

    bot.send_message(chat_id, "Что дальше?", reply_markup=keyboard)

# Обработка кнопок после викторины
def button_handler(call):
    chat_id = call.message.chat.id
    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново /start")
        return

    if call.data == "contact_zoo":
        contact_zoo(chat_id)
    elif call.data == "restart_quiz":
        restart_quiz(chat_id)
    elif call.data == "leave_feedback":
        leave_feedback(chat_id)
    elif call.data == "patronage_info":
        show_patronage_info(chat_id)

# Информация о программе опеки (подробный блок)
def show_patronage_info(chat_id):
    patronage_info = (
        "🌟 Программа опеки зоопарка:\n\n"
        "Станьте опекуном своего любимого животного и помогите ему чувствовать себя как дома!\n\n"
        "Что включает программа опеки:\n"
        "- Ежемесячное финансирование для питания и ухода за животным.\n"
        "- Возможность посещать животное в зоопарке.\n"
        "- Регулярные отчёты о состоянии здоровья и жизни вашего подопечного.\n"
        "- Участие в специальных мероприятиях для опекунов.\n\n"
        "Для участия свяжитесь с нами через кнопку «Связаться с зоопарком» или напишите нам на email: zoo@example.com."
    )
    bot.send_message(chat_id, patronage_info)

# Контактный механизм (запрос email)
def contact_zoo(chat_id):
    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново /start")
        return

    scores = user_info["scores"]
    best_animal = min(animals, key=lambda animal: sum(abs(scores[key] - animals[animal][key]) for key in scores))

    # Предлагаем пользователю ввести email
    user_info["awaiting_email"] = True
    user_info["best_animal"] = best_animal
    bot.send_message(chat_id, "Пожалуйста, введите ваш email, чтобы связаться с сотрудником зоопарка.")

# Обработка ввода email
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("awaiting_email", False))
def handle_email(message):
    chat_id = message.chat.id
    email = message.text.strip()

    # Валидация email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        bot.send_message(chat_id, "Некорректный email. Пожалуйста, попробуйте снова.")
        return

    user_info = user_data.get(chat_id)
    if not user_info:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново /start")
        return

    # Сохраняем email пользователя
    user_info["email"] = email
    best_animal = user_info.get("best_animal", "неизвестное животное")

    # Отправляем данные сотруднику (например, в логи или через email)
    logger.info(f"User {chat_id} contacted the zoo with email: {email}, totem animal: {best_animal}")
    bot.send_message(chat_id, f"Спасибо! Сотрудник зоопарка скоро свяжется с вами.\n"
                              f"Он уже знает, что ваше тотемное животное — это {best_animal.capitalize()}.")

    # Сбрасываем флаг ожидания email
    user_info["awaiting_email"] = False
    user_info.pop("best_animal", None)

# Перезапуск викторины
def restart_quiz(chat_id):
    user_data[chat_id] = {  # Полная очистка данных пользователя
        "scores": {"сила": 0, "скорость": 0, "доброта": 0, "общительность": 0},
        "current_question": 0,
        "awaiting_feedback": False,
        "awaiting_email": False,
        "best_animal": None
    }
    ask_question(chat_id)

# Механизм обратной связи
def leave_feedback(chat_id):
    bot.send_message(chat_id, "Оставьте свой отзыв о боте:\n\nПросто отправьте сообщение, и мы учтём ваши пожелания!")
    user_data[chat_id]["awaiting_feedback"] = True

# Сохранение отзыва
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("awaiting_feedback", False))
def save_feedback(message):
    chat_id = message.chat.id
    feedback = message.text
    logger.info(f"Received feedback from user {chat_id}: {feedback}")
    bot.send_message(chat_id, "Спасибо за ваш отзыв! Мы обязательно учтём его при улучшении бота.")
    user_data[chat_id]["awaiting_feedback"] = False

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling()