from bs4 import BeautifulSoup
import requests as r
import time
import sys
import os.path

def get_course(link):
    
    try:
        page = r.get(link)
    except:
        print('Вы ввели нерабочую ссылку.')
        sys.exit()

    soup = BeautifulSoup(page.text, 'lxml')

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

try:
    get_course(input('Введите ссылку на курс\n'))
except KeyboardInterrupt:
    pass