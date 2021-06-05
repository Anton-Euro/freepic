import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')

br = webdriver.Chrome(options=options)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)		

@dp.message_handler(commands=['start'])
async def start_pars(message: types.Message):
	await message.answer('Старт')
	while True:
		br.get('https://www.epicgames.com/store/ru/free-games')
		html = br.find_element_by_class_name('css-1442lgn-CardGrid-styles__group').text
		await message.answer(html)
		await asyncio.sleep(10)
#86400
if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)