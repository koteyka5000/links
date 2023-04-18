import webbrowser  # Для открытия ссылок в браузере
import requests  # Для проверки кода ответа от сайта
import random  # Для генерации случайной ссылки
from multiprocessing import Process  # Для работы в нескольких процессах одновременно
from time import sleep
from string import ascii_letters
import datetime


alpha = ascii_letters + '1234567890'
site = 'https://goo.su' # Сайт для сокращения ссылок
is_open =  0 # Открывать ли ссылку в браузере
is_write = 1 # Записывать ли ссылку в файл
string_len = 5 # Длинна строки для подбора
max_combo_to_block = 2 # необходимое количество подряд открытых вкладок для аварийного завершения и предотвращения спама вкладками
processes = 2 # Во сколько процессов работать (больше -> быстрее, но можно получить блокировку на сайте)
try:
    with open('urls', 'r'):
        pass
except:
    print('Нету файла, возможно неверна директория')
    exit()

def write(file, url, redirected_url, after_separator=None):
    with open(file, 'a') as f:
        now = datetime.datetime.now()
        time = now.strftime("%d.%m %H:%M:%S")
        if after_separator:
            f.write(f'[{time}] -> {url} | {after_separator}\n')
        elif url == redirected_url:
            f.write(f'[{time}] -> {url} | !\n')
        else:
            f.write(f'[{time}] -> {url} | {redirected_url}\n')

def run():
    last = 0
    status_code = None
    while 1:
        s = ''
        for i in range(string_len):
            s += random.choice(alpha)
        url = f'{site}/{s}'
        try:
            r = requests.head(url)
        except:
            print('FAILED TO REQUEST!')
            sleep(3)
            continue

        status_code = r.status_code
        print(f'{s} > {status_code}')

        if status_code != 404:
            if status_code == 429:
                print('===BLOCKED===')
                #  NOTE: Попробуй использовать меньше процессов, ведь сайт заблокировал запросы за слишком частую отправку
                while status_code == 429:
                    sleep(1)
                    status_code = requests.head(url).status_code
                print('>>>UNBLOCKED')
                continue
            if last >= max_combo_to_block:
                print('>>> BLOCKED')
                print('NOTE: Сработала защита от спама вкладок в браузере, ведь подряд было открыто <max_combo_to_block> вкладок')
                sleep(5)
                exit()
            print('^^^^^===^^^===========================================')
            try:
                r = requests.get(url) # head не содержит переадресованной ссылки, а get содержит, но get работает медленнее
            except:
                write('urls', url, None, 'FATAL ERROR')
                continue

            if 'https://cards.metro-cc.ru/' in r.url: # Если сайт это metro
                print('==METRO==')
                write('urls_metro.txt', url, r.url)
                continue


            if is_open:
                webbrowser.open(url, new=2)
            if is_write:
                write('urls', url, r.url)
            last += 1
        else:
            last = 0

if __name__ == '__main__':
    for w in range(processes):  
        p = Process(target=run)  
        p.start()
