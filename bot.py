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

br = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=options)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

users = []

@dp.message_handler(commands=['userlist'])
async def start(message: types.Message):
	mess = ''
	for i in range(len(users)):
		mess = mess + str(i+1) + ' '+ str(users[i][0]) + ' ' + str(users[i][1]) + '\n'
	if mess == '':
		await message.answer('список пуст')
	else:
		await message.answer(mess)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	global users, last_check
	sub = 0
	for i in range(len(users)):
		if users[i][0] == message.from_user.id:
			pos_user = i
			sub = 1
			break
	if sub == 0:
		users.append([message.from_user.id,True])
		await message.answer('Старт')
	else:
		users[pos_user][1] = True
		await message.answer('Старт')
	last_check = None

@dp.message_handler(commands=['stop'])
async def stop(message: types.Message):
	global users
	sub = 0
	for i in range(len(users)):
		if users[i][0] == message.from_user.id:
			pos_user = i
			sub = 1
			break
	if sub == 0:
		await message.answer('Вы и так не нажали старт')
		users.append([message.from_user.id,False])
	else:
		users[pos_user][1] = False
		await message.answer('Стоп')

async def parse():
	global last_check
	last_check = None
	while True:
		br.refresh()
		br.get('https://www.epicgames.com/store/ru/free-games')
		html = br.find_element_by_class_name('css-1442lgn-CardGrid-styles__group').text
		if last_check != html:
			last_check = html
			for i in range(len(users)):
				if users[i][1] == True:
					await bot.send_message(users[i][0],html)
		await asyncio.sleep(600)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.create_task(parse())
	executor.start_polling(dp, skip_updates=True, loop=loop)