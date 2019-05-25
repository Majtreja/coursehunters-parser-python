from bs4 import BeautifulSoup as bs
import requests as r
import time
import pprint
import sys

link = input('Введите ссылку на курс\n')

try:
	page = r.get(link)


	soup = bs(page.text, 'lxml')

	try:
		lessonsList = soup.find(class_='lessons-list')

		lessonsLinks = lessonsList.find_all(itemprop='url')

		lessonsNames = lessonsList.find_all(itemprop='name')

		length = len(lessonsLinks)

		i = 0

		while (i < length):
			try:
				file = open('lesson' + str((i+1)) + '.mp4', 'r')
				print('lesson' + str((i+1)) + ' был загружен ранее.')
				i += 1
			except:
				print('Getting ' + str((i+1)) + ' lesson')
				name = lessonsNames[i].contents[0]
				link = str(lessonsLinks[i].get('href'))
				try:
					file = r.get(link)
					print(name + ' downloaded')
					with open('lesson' + str((i+1)) + '.mp4', 'wb') as f:
						f.write(file.content)
					i += 1
				except:
					pprint.pprint('Произошла ошибка. Возможно вы ввели ссылку не на coursehunters курс.')
					time.sleep(5)


 
	except:
		pprint.pprint('Судя по всему, вы ввели ссылку НЕ на coursehunters')
		time.sleep(5)
		sys.exit()

except KeyboardInterrupt:
	pprint.pprint('Вы ввели непонятно что')
	time.sleep(5)
	sys.exit()