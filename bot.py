import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from configuration import bot_token, user_token

from database import viewed_people_create_table, checking_user_data


class BotMessageUser:
    first: str = 'Приветствую Вас! Начинаем поиск подходящей кандидатуры?'
    hallmarks: str = 'Выберите, пожалуйста, критерии поиска'
    repeat: str = 'Повторим?'
    hometown: str = 'Введите, пожалуйста, название города: '
    fault_hometown: str = 'Выбранный Вами город не найден. Попробуйте ещё раз: '
    sex: str = 'Выберите интересующий вас пол:'
    butt_sex: str = 'Нажмите, пожалуйста, кнопку выбора пола'
    mans: str = 'Выбраны мужчины'
    womens: str = 'Выбраны женщины'
    age_minimum: str = 'Введите минимальный возраст (от 18 до 99):'
    search_age_minimum: str = 'Поиск кандидатов от %s лет'
    fault_age_minimum: str = 'Введите, пожалуйста, целое число от 18 до 99!'
    age_maximum: str = 'Введите максимальный возраст (от 18 до 99):'
    search_age_maximum: str = 'Поиск кандидатов от %s лет'
    fault_age_maximum: str = 'Введите, пожалуйста, целое число от 18 до 99!'


class ChatBot:

    def __init__(self, api_user, token):
        self.bot = vk_api.VkApi(token=token)
        self.api_user = api_user

    def send_msg(self, user_id, message=None, attachment=None, keyboard=None):
        self.bot.method('messages.send',
                        {'user_id': user_id,
                         'message': message,
                         'random_id': get_random_id(),
                         'attachment': attachment,
                         'keyboard': keyboard
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

    def keyboard_input(self):
        search_info_keyboard = VkKeyboard()
        search_info_keyboard.add_button('Необходимо выбрать город: ', VkKeyboardColor.PRIMARY)
        search_info_keyboard.add_button('Необходимо выбрать пол: ', VkKeyboardColor.PRIMARY)
        search_info_keyboard.add_button('Осуществляем поиск пары', VkKeyboardColor.PRIMARY)
        search_info_keyboard.add_button('Возраст от: ', VkKeyboardColor.PRIMARY)
        search_info_keyboard.add_button('Возраст до: ', VkKeyboardColor.PRIMARY)
        search_info_keyboard.add_button('Вернуться назад', VkKeyboardColor.PRIMARY)
        search_info_keyboard = search_info_keyboard.get_keyboard()
        return search_info_keyboard

    def keyboard_initial(self):
        keyboard_initial_cst = VkKeyboard()
        keyboard_initial_cst.add_button('Ну что, поехали!', VkKeyboardColor.PRIMARY)
        keyboard_initial = keyboard_initial_cst.get_keyboard()
        return keyboard_initial

    def keyboard_gender_selection(self):
        slc_gender_keyboard = VkKeyboard()
        slc_gender_keyboard.add_button('Женский', VkKeyboardColor.PRIMARY)
        slc_gender_keyboard.add_button('Мужской', VkKeyboardColor.PRIMARY)
        slc_gender_keyboard = slc_gender_keyboard.get_keyboard()
        return slc_gender_keyboard

    def set_search_params(self, user_id):

        self.send_msg(user_id, 'Выберите параметры для поиска:', keyboard=self.keyboard_input())
        for event in self.longpoll.listen():
            if ChatBot.handler(event):
                message = event.text.lower()
                user_id = event.user_id

                if message == 'назад':
                    self.send_msg(user_id, BotMessageUser.repeat, keyboard=self.keyboard_initial())
                    return

                elif message == 'выбрать город':
                    self.get_city_id(user_id)

                elif message == 'выбрать пол':
                    self.get_sex(user_id)

                elif message == 'возраст от':
                    self.get_min_age(user_id)

                elif message == 'возраст до':
                    self.get_max_age(user_id)

    def get_city_id(self, user_id):

        self.send_msg(user_id, BotMessageUser.hometown, keyboard=self.keyboard_input())
        for event in self.longpoll.listen():
            if ChatBot.handler(event):
                city_param = {
                    'q': event.text,
                    'country_id': 1,
                    'count': 1,
                    'v': 5.131
                }

                result_hometown = self.api_user.method('database.getCities', city_param).get('items')
                if not result_hometown:
                    self.send_msg(user_id, BotMessageUser.fault_hometown)
                else:
                    self.send_msg(user_id, f'Выбран город: {event.text.capitalize()}')
                    return result_hometown[0].get('id')

    def get_sex(self, user_id):

        self.send_msg(user_id, BotMessageUser.sex, keyboard=self.keyboard_gender_selection())
        for event in self.longpoll.listen():
            if ChatBot.handler(event):
                if event.text == 'Он':
                    self.send_msg(user_id, BotMessageUser.mans, keyboard=self.keyboard_input())
                    return 2
                elif event.text == 'Она':
                    self.send_msg(user_id, BotMessageUser.womens, keyboard=self.keyboard_input())
                    return 1
                else:
                    self.send_msg(user_id, BotMessageUser.butt_sex, keyboard=self.keyboard_gender_selection())

    def get_min_age(self, user_id):

        self.send_msg(user_id, BotMessageUser.age_minimum)
        for event in self.longpoll.listen():
            if ChatBot.handler(event):
                minimum_age = event.text
                if minimum_age.isdigit() and int(minimum_age) >= 18 and int(minimum_age) <= 99:
                    self.send_msg(user_id, BotMessageUser.search_age_minimum % minimum_age)
                    return minimum_age
                else:
                    self.send_msg(user_id, BotMessageUser.fault_age_minimum, keyboard=self.keyboard_input())

    def get_max_age(self, user_id):

        self.send_msg(user_id, BotMessageUser.age_maximum)
        for event in self.longpoll.listen():
            if ChatBot.handler(event):
                maximum_age = event.text
                if maximum_age.isdigit() and int(maximum_age) >= 18 and int(maximum_age) <= 99:
                    self.send_msg(user_id, BotMessageUser.search_age_maximum % maximum_age)
                    return maximum_age
                else:
                    self.send_msg(user_id, BotMessageUser.fault_age_maximum, keyboard=self.keyboard_input())


if __name__ == '__main__':
    
    viewed_people_create_table()
    checking_user_data()
    
    bot = ChatBot(bot_token)
    bot.handler()



