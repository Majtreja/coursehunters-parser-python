from bs4 import BeautifulSoup as bs
import requests as r
import time
import pprint

link = input('Введите ссылку на курс\n')

try:
	page = r.get(link)


	soup = bs(page.text, 'lxml')

	try:
		lessonsList = soup.find(class_='lessons-list')

		lessonsLinks = lessonsList.find_all(itemprop='url')

		lessonsNames = lessonsList.find_all(itemprop='name')

		lenght = len(lessonsLinks)

		i = 0

		while (i < lenght):
			print('Getting ' + str((i+1)) + ' lesson')
			name = lessonsNames[i].contents[0]
			link = str(lessonsLinks[i].get('href'))
			try:
				file = r.get(link)
				print('Writing ' + str((i+1)) + ' lesson')
				with open('lesson' + str((i+1)) + '.mp4', 'wb') as f:
					f.write(file.content)
				i += 1
			except:
				pprint.pprint('Что-то явно пошло не так. Возможно вы ввели ссылку не на coursehunters.')

	except:
		pprint.pprint('Судя по всему, вы ввели ссылку НЕ на coursehunters')

except:
	pprint.pprint('Вы ввели непонятно что')