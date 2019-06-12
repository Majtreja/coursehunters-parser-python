from bs4 import BeautifulSoup
import requests as r
import time
import sys
import os.path


def how_to_download():
    result = True
    while result:
        choice = input('1) Искать курсы по сайту.\n2) Ввести ссылку на курс.\n')

        if choice == '1':
            result = search_course(input('Введите запрос:\n'))
        elif choice == '2':
            result = get_course(input('Введите ссылку на курс:\n'))
        else:
            print('Такого варианта нет.')
            sys.exit()
    print(result)


def search_course(request):
    request = request.replace(' ','+')

    try:
        page = r.get(f'https://coursehunters.net/search?q={request}&orderBy=')
    except:
        print('Что-то не так с ссылкой. Попробуйте ещё раз, или напишите мне о проблеме. Telegram @lexani42.')

    soup = BeautifulSoup(page.text, 'lxml')
    course_list = soup.find(class_='course-list')
    if not course_list:
        print('Произошла ошибка. Попробуйте ещё раз, или напишите мне о проблеме. Telegram @lexani42.')
        input()

    course_names = []
    course_links = []
    all_courses = course_list.find_all(class_='course')

    for i in all_courses:
        course_names.append(i.find(class_='course-primary-name').contents[0])
        course_links.append(i.find(class_='course-btn btn').get('href'))

    for i in range (len(course_names)):
        print(f'{i+1} {course_names[i]}')

    try:
        course_number = int(input('Введите № курса для скачиавния: '))
    except ValueError:
        print('Вы ввели не число.\n1) Вернуться в начало.')
        return input() == '1'

    if 0 < course_number <= len(course_links):
        return get_course(course_links[course_number - 1])
    else:
        print('Out of range.\n1) Вернуться в начало.')
        return input() == '1'


def get_course(link):
    try:
        page = r.get(link)
    except:
        print('Что-то не так со ссылкой. Попробуйте ещё раз, или напишите мне о проблеме. Telegram @lexani42.')
        sys.exit()

    soup = BeautifulSoup(page.text, 'lxml')

    if soup.find(class_='btn mb-20').contents[0] == 'Course Paid':
        print('К сожалению, этот курс является платным. Оформите подписку на coursehunters для просмотра. 1) Переход к началу выполнения скрипта.')
        return input() == '1'

    lesson_list = soup.find(class_='lessons-list')
    if not lesson_list:
        print('Произошла ошибка. Возможно вы ввели ссылку не на coursehunters. 1) Вернуться к началу скрипта.')
        return input() == '1'
    lessons = lesson_list.find_all(class_='lessons-item')
    lesson_names = []
    lesson_links = []
    for i in lessons:
        lesson_names.append(i.find(class_='lessons-name').contents[0])
        lesson_links.append(i.find(itemprop='url').get('href'))

    for i in range(len(lesson_links)):
        if os.path.exists(f'lesson{i+1}.mp4'):
           print(f'lesson {i+1} был загружен ранее')
        else:
            print(f'Getting {i+1} lesson')
            file = r.get(str(lesson_links[i]))
            print(f'{lesson_names[i]} downloaded')
            with open(f'lesson{i+1}.mp4', 'wb') as f:
                f.write(file.content)

    print('All lessons downloaded. Go to start(1) or exit?')
    return input() == '1'

try:
    how_to_download()
except KeyboardInterrupt:
    pass