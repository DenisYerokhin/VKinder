import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from configuration import bot_token, user_token



class Chat_bot:

    def __init__(self, token):
        self.bot = vk_api.VkApi(token=bot_token)

    def send_msg(self, user_id, message):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id()
                        }
                       )

    def handler(self):
        longpoll = VkLongPoll(self.bot)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    self.send_msg(event.user_id, 'Добрый день')
                elif event.text.lower() == 'поиск':
                    pass
                elif event.text.lower() == 'далее':
                    pass
                else:
                    self.send_msg(event.user_id, 'неизвестная команда')




