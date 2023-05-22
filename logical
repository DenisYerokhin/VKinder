from vkbottle.bot import Bot, Message
from configuration import bot_token

bot = Bot(token=bot_token)


@bot.on.message(text='Привет')
async def first_handler(message: Message):
    await message.answer('Приветствую Вас!')

bot.run_forever()
