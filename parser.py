from bs4 import BeautifulSoup
import requests as r
import time
import sys
import os.path


def how_to_download():
    choise = input('1) Искать курсы по сайту.\n2) Ввести ссылку на курс.\n')

    if choise == '1':
        choose_course(input('Введите запрос:\n'))
    elif choise == '2':
        request = input('Введите ссылку на курс:\n')
        get_course(request)
    else:
        print('Такого варианта нет.')
        sys.exit()


def choose_course(request):

    try:
        page = r.get(f'https://coursehunters.net/search?q={request}&orderBy=')
    except:
        print('Что-то не так со ссылкой. Попробуйте ещё раз, или напишите мне о проблеме. Telegram @lexani42.')

    soup = BeautifulSoup(page.text, 'lxml')
    course_names = []
    course_links = []

    for i in soup.find_all(class_='standard-course-block'):
        course_names.append(i.find(class_='standard-course-block__course-name').find(itemprop='headline').contents[0])
        course_links.append(i.find(class_='standard-course-block__course-name').find('a').get('href'))

    # delete premium courses
    for i in range (len(soup.find_all(class_='standard-block_blue'))):
        course_names.pop()
        course_links.pop()

    for i in range (len(course_names)):
        print(f'{i + 1}) {course_names[i]}')

    try:
        get_course(course_links[int(input('Введите № курса для скачивания: ')) - 1])
    except IndexError:
        print('Out of range.')
        how_to_download()


def get_course(link):

    try:
        page = r.get(link)
    except:
        print('Что-то не так со ссылкой. Попробуйте ещё раз, или напишите мне о проблеме. Telegram @lexani42.')
        sys.exit()

    soup = BeautifulSoup(page.text, 'lxml')
    course_name = {soup.find('article').find('h1').contents[0].replace(' - Видеоуроки', '')}
    print(f'Вы действительно хотите скачать этот курс? {list(course_name)[0]}\nОтветьте y если да.')
    if input()[0] == 'y':
    	pass
    else:
    	print('Отмена.')
    	sys.exit()

    lessons_list = soup.find(class_='lessons-list')
    if not lessons_list:
        input('Произошла ошибка. Возможно вы ввели ссылку не на coursehunters. Нажмите Enter для выхода.')
        sys.exit()
    lessons_links = lessons_list.find_all(itemprop='url')
    lessons_names = lessons_list.find_all(itemprop='name')

    for i in range(len(lessons_links)):
        if os.path.exists(f'lesson{i+1}.mp4'):
            print(f'lesson {i + 1} был загружен ранее.')
        else:
            print(f'Getting {i + 1} lesson')
            file = r.get(str(lessons_links[i].get('href')))
            print(f'{lessons_names[i].contents[0]} downloaded')
            with open(f'lesson{i + 1}.mp4', 'wb') as f:
                f.write(file.content)

    print('All lessons downloaded. Go to start(1) or exit(anything else)?')
    if input('\n') == '1':
        how_to_download()
    else:
        sys.exit()


try:
    how_to_download()
except KeyboardInterrupt:
    pass