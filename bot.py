import config
import telebot
import time
# from selenium import webdriver

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "начало")
	while True:
		# browser = webdriver.Chrome()
		# browser.get('https://www.epicgames.com/store/ru/free-games')

		# html = browser.find_element_by_class_name('css-1nzrk0w-CardGrid-styles__groupWrapper').text
		# browser.quit()

		# bot.send_message(message.chat.id, html)
		bot.send_message(message.chat.id, 'https://www.epicgames.com/store/ru/free-games')
		time.sleep(86400)

bot.polling(none_stop=True)