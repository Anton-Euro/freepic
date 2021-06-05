import config
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
import os
from sqlitemanager import SQLmanager

options = webdriver.ChromeOptions()
options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

br = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=options)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)		

db = SQLmanager('db.db')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	if not db.subscriber_exists(message.from_user.id):
		db.add_subscriber(message.from_user.id)
	else:
		db.update_subscription(message.from_user.id, True)
	await message.answer('Старт')

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
	if not db.subscriber_exists(message.from_user.id):
		db.add_subscriber(message.from_user.id, False)
	else:
		db.update_subscription(message.from_user.id, False)
	await message.answer('Стоп')

async def parse():
	while True:
		br.get('https://www.epicgames.com/store/ru/free-games')
		html = br.find_element_by_class_name('css-1442lgn-CardGrid-styles__group').text
		subs = db.get_subscriptions()
		for sub in subs:
			await bot.send_message(sub[1],html)
		await asyncio.sleep(600)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(parse())
	executor.start_polling(dp, skip_updates=True)