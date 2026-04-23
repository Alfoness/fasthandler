from telebot import TeleBot
from telebot import types


class FastMessageHandler:
    def __init__(self,
                 trigger_text: str,\
                 response_text: str | None, #HTML markdown
                 keyboard: types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup = None,
                 photo: str = None,
                 params: dict = None,
                 set_command: bool = False,
                 description_command: str = "🔸"):
        
        self.trigger_text = trigger_text
        self.description_command = description_command
        self.response_text = response_text
        self.keyboard = keyboard
        self.photo = photo
        if photo is None:
            self.method = "sendMessage"
        else:
            self.method = "sendPhoto"
        self.params = params
        self.set_command = set_command
        

    def add_command(self, bot: TeleBot) -> TeleBot:
        commands = bot.get_my_commands()
        commands_triggers = []
        for cmd in commands:
            commands_triggers.append(cmd.command)
        
        if self.trigger_text not in commands:
            commands.append(types.BotCommand(command=self.trigger_text, description=self.description_command))
            bot.set_my_commands(commands)
        else:
            pass
        
        return bot
    
    
    def fast_register_obj(self, bot: TeleBot) -> TeleBot:
        if self.method == "sendMessage":
            def temp_function(message: types.Message, bot: TeleBot):
                bot.send_message(chat_id=message.chat.id,
                                 text=self.response_text,
                                 reply_markup=self.keyboard)
        
        elif self.method == "sendPhoto":
            def temp_function(message: types.Message, bot: TeleBot):
                bot.send_photo(chat_id=message.chat.id,
                               photo=self.photo,
                               caption=self.response_text,
                               reply_markup=self.keyboard)
        
        if self.set_command:
            self.add_command(bot)
            
        bot.register_message_handler(
            callback=temp_function,
            commands=[self.trigger_text],
            pass_bot=True
        )
        
        return bot
    
    def fast_register_list(objects: list, bot: TeleBot) -> TeleBot:
        for obj in objects:
            if obj.method == "sendMessage":
                def temp_function(message: types.Message, bot: TeleBot):
                    bot.send_message(chat_id=message.chat.id,
                                     text=obj.response_text,
                                     reply_markup=obj.keyboard)
                    
            elif obj.method == "sendPhoto":
                def temp_function(message: types.Message, bot: TeleBot):
                    bot.send_photo(chat_id=message.chat.id,
                                    photo=obj.photo,
                                    caption=obj.response_text,
                                    reply_markup=obj.keyboard)
                    
            if obj.set_command:
                obj.add_command(bot)
                        
            bot.register_message_handler(
                callback=temp_function,
                commands=[obj.trigger_text],
                pass_bot=True
            )
                    
        return bot