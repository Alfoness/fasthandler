from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

map = {
    'Майнкрафт сервер': {
        'Подключение': 'how_connect_server',
        'Информация': 'server_info'
    },
    'Управление профилем': {
        'Изменить аву': 'change_avatar',
        'Изменить имя': 'change_name',
        'Изменить описание': 'change_about'
    },
    'В чём прикол бота?': 'info_bot'
}

class InlineMenu:
    def __init__(self,
                 trigger_text: str,
                 response_text: str,
                 map: dict):
        self.trigger_text = trigger_text
        self.response_text = response_text
        self.map = map
        self.main_keyboard = InlineKeyboardMarkup()
    
    
    def back(self, bot: TeleBot) -> TeleBot:
        def temp_function(callback: CallbackQuery, bot: TeleBot):
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id,
                                          reply_markup=self.main_keyboard)    

        bot.register_callback_query_handler(callback=temp_function,
                                            func=lambda call: call.data == self.trigger_text,
                                            pass_bot=True)
        
        return bot  
        

    def capture(self, cdata: str, map: dict, bot: TeleBot) -> TeleBot:
        keyboard = InlineKeyboardMarkup()
        
        for key, data in map.items():
            if isinstance(data, dict):
                keyboard.add(InlineKeyboardButton(text=cdata, callback_data=key))
                bot = self.capture(cdata=key, map=data, bot=bot) 
            else:
                keyboard.add(InlineKeyboardButton(text=key, callback_data=data))
        
        
        keyboard.add(InlineKeyboardButton(text='Назад', callback_data=self.trigger_text))
        
        def temp_function(callback: CallbackQuery, bot: TeleBot):
            bot.edit_message_reply_markup(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id,
                                          reply_markup=keyboard)
        
        bot.register_callback_query_handler(callback=temp_function,
                                            func=lambda call: call.data == cdata,
                                            pass_bot=True)
        
        return bot


    def main_capture(self, bot: TeleBot) -> TeleBot:
        for key, data in self.map.items():
            if isinstance(data, dict):
                self.main_keyboard.add(InlineKeyboardButton(text=key, callback_data=key))
                bot = self.capture(cdata=key, map=data, bot=bot)
            else:
                self.main_keyboard.add(InlineKeyboardButton(text=key, callback_data=data))
            
        bot = InlineMenu.register_menu(keyboard=self.main_keyboard,
                                       response_text=self.response_text,
                                       trigger_text=self.trigger_text,
                                       bot=bot)
        
        bot = InlineMenu.back(self=self, bot=bot)
        return bot


    def register_menu(keyboard: InlineKeyboardMarkup,
                      response_text: str,
                      trigger_text: str,
                      bot: TeleBot) -> TeleBot:
        def temp_function(message: Message, bot: TeleBot):
            bot.send_message(chat_id=message.chat.id,
                             text=response_text,
                             reply_markup=keyboard)
        
        bot.register_message_handler(callback=temp_function,
                                     commands=[trigger_text],
                                     pass_bot=True)
    
        return bot


if __name__ == "__main__":
    token = "8718029801:AAGM1AqvDW_I0Tjm2A5mHX1H2qpcLTbdg7Y"
    bot = TeleBot(token=token)
    test = InlineMenu(trigger_text='testmenu', response_text='Меню менеджера', map=map)
    bot = test.main_capture(bot)
    bot.polling()