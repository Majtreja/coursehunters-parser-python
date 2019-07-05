# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests as r
import time
import sys
import os.path


def check_version():
    print('Checking for new updates. Please, wait.')
    todays_commit_name = 'v3.2.1 completely translate'
    github_page = r.get('https://github.com/Lexani42/coursehunters-parser-python')
    soup = BeautifulSoup(github_page.text, 'lxml')
    github_commit_name = soup.find(class_='message text-inherit').get('title')
    if github_commit_name == todays_commit_name:
        print('It\'s OK, you use last version.')
        how_to_download()
    else:
        print('Sorry, but you use old version of my product. It can work extraordinary, you should update it to new version.')
        how_to_download()


def how_to_download():
    result = True
    while result:
        choice = input('1) Find courses.\n2) Paste link to course.\n')

        if choice == '1':
            result = search_course(input('Input request:\n'))
        elif choice == '2':
            result = get_course(input('Input link:\n'))
        else:
            print('There isn\'t such variant.')
            sys.exit()


def search_course(request):
    request = request.replace(' ','+')

    try:
        page = r.get(f'https://coursehunters.net/search?q={request}&orderBy=')
    except:
        print('Hmm, it\'s looks like your link is not correct. If you think that it\'s an error, notify me about it.\nTelegram @lexani42.')

    soup = BeautifulSoup(page.text, 'lxml')
    course_list = soup.find(class_='course-list')
    if not course_list:
        print('Hmm, there is one error. I don\'t know a reason. Try again or notify me about this problem, I\'ll try to fix it.\nTelegram @lexani42.')
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
        course_number = int(input('Input course number to download: '))
    except ValueError:
        print('I\'m sorry, but you should call your math teacher. That is not number.\n1) Go to start.')
        return input() == '1'

    if 0 < course_number <= len(course_links):
        return get_course(course_links[course_number - 1])
    else:
        print('Out of range.\n1) Go to start.')
        return input() == '1'


def get_course(link):
    try:
        page = r.get(link)
    except:
        print('Hmm, it\'s looks like your link is not correct. If you think that it\'s an error, notify me about it.\nTelegram @lexani42.')
        sys.exit()

    soup = BeautifulSoup(page.text, 'lxml')

    if 'Премиум' in page.text:
        print('Oh, I\'m so sorry... It seems to me that this course is premium-only... If you think that it\'s an error, you can write me in Telegram, but firstly I want you to check this course. There is a link - ' + link + '. Thanks for understanding.\nTelegram: @lexani42.')
        return input() == '1'

    lesson_list = soup.find(class_='lessons-list')
    if not lesson_list:
        print('Hmm, I think there is not a coursehunters link... What did you say? That was an error? Or, try to notice me about it.\nTelegram: @lexani42\n1) Go to start.')
        return input() == '1'
    lessons = lesson_list.find_all(class_='lessons-item')
    lesson_names = []
    lesson_links = []
    for i in lessons:
        lesson_names.append(i.find(class_='lessons-name').contents[0])
        lesson_links.append(i.find(itemprop='url').get('href'))

    for i in range(len(lesson_links)):
        if os.path.exists(f'lesson{i+1}.mp4'):
           print(f'lesson {i+1} was downloaded earlier')
        else:
            print(f'Getting {i+1} lesson')
            file = r.get(str(lesson_links[i]))
            print(f'{lesson_names[i]} downloaded')
            with open(f'lesson{i+1}.mp4', 'wb') as f:
                f.write(file.content)

    print('All lessons downloaded. Go to start(1) or exit?')
    return input() == '1'

try:
    check_version()
except KeyboardInterrupt:
    pass