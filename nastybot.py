import telebot
from telebot import types as telebotTypes
from gigachat import GigaChat

class NastyBotClass:
    def __init__(self, telegram_token, gigachat_token):
        self.bot = telebot.TeleBot(telegram_token)
        self.systemMessage = "Ты бот-ассистент, который ПОМОГАЕТ ФОРМИРОВАТЬ ПРОДУКТ, ОПИСЫВАТЬ ЗАДАЧИ, ПОДСКАЗЫВАТЬ ВАРИАНТЫ РЕШЕНИЙ, ИЗУЧАТЬ НЕИЗВЕСТНЫЕ ТЕМЫ, ПОМОГАТЬ ПИСАТЬ КОД, ПОМОГАТЬ ГОТОВИТЬСЯ К ЗАЩИТЕ ПРОЕКТА, ПЕРЕВОДИТЬ ТЕКСТ С АНГЛИЙСКОГО ЯЗЫКА НА РУССКИЙ"
        self.communication = [{"role": "system", "content": self.systemMessage}]
        self._setup_handlers()
        self._gigachat_token = gigachat_token

    def _setup_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            markup = telebotTypes.ReplyKeyboardMarkup(resize_keyboard=True)
            button = telebotTypes.KeyboardButton("Новая генерация")
            markup.add(button)
            self.bot.send_message(message.chat.id, "Привет! Я бот-ассистент для хакатона. Чем могу помочь? Для начала работы нажмите кнопку ниже.", reply_markup=markup)

        @self.bot.message_handler(func=lambda message: True)
        def handle_message(message):
            if message.text == "Новая генерация":
                self.communication = [{"role": "system", "content": self.systemMessage}]
                msg = self.bot.reply_to(message, "Пожалуйста, опишите задачу, которую нужно решить.")
                self.bot.register_next_step_handler(msg, self.process_task)
            else:
                self.process_task(message)

    def process_task(self, message):
        if message.text in "Очистить историю":
            self.bot.send_message(message.chat.id, "История сообщений очищена")
            self.reset()
        elif message.text.lower() == 'спасибо':
            self.bot.send_message(message.chat.id, "Всегда рад помочь")
        else:
            if len(self.communication) <= 2:
               self.communication.append({"role": "user", "content": message.text})
            else:
               self.communication[1] = self.communication[2]
               self.communication[2] = {"role": "user", "content": message.text}
            system_message = self.generate_response(message)
            self.bot.send_message(message.chat.id, system_message)

    def generate_response(self):
        content = self.send_request_to_gigachat()
        
        if content:
            return content
        else:
            return 'Ошибка при генерации ответа. Попробуйте снова позже.'
    

    def send_request_to_gigachat(self):
        client = GigaChat(
                model="GigaChat-Pro",
                scope="GIGACHAT_API_PERS",
                verify_ssl_certs=False,
                credentials=self._gigachat_token
            )
        
        payload = {
            "messages": self.communication
        }

        giga_chat_coroutine = client.chat(payload)

        while True:
            try:
                return giga_chat_coroutine.choices[0].message.content
            except StopIteration:
                break

    
    def reset(self):
        self.communication.clear()

    def start(self):
        self.bot.polling(none_stop=True)

    def run(self):
        self.start()
