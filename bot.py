import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
import os

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

br = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=options)

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