import webbrowser  # Для открытия ссылок в браузере
import requests  # Для проверки кода ответа от сайта
import random  # Для генерации случайной ссылки
from multiprocessing import Process  # Для работы в нескольких процессах одновременно
from time import sleep
from string import ascii_letters


alpha = ascii_letters + '1234567890'
site = 'https://goo.su' # Сайт для сокращения ссылок
is_open =  0 # Открывать ли ссылку в браузере
is_write = 1 # Записывать ли ссылку в файл
string_len = 5 # Длинна строки для подбора
max_combo_to_block = 2 # необходимое количество подряд открытых вкладок для аварийного завершения и предотвращения спама вкладками
processes = 2 # Во сколько процессов работать (больше -> быстрее, но можно получить блокировку на сайте)

def run():
    last = 0
    status_code = None
    while 1:
        s = ''
        for i in range(string_len):
            s += random.choice(alpha)

        r = requests.head(f'{site}/{s}')
        status_code = r.status_code
        print(f'{s} > {status_code}')

        if status_code != 404:
            if status_code == 429:
                print('===BLOCKED===')
                print('NOTE: Попробуй использовать меньше процессов, ведь сайт заблокировал запросы за слишком частую отправку')
                while status_code == 429:
                    sleep(3)
                    status_code = requests.head(f'{site}/{s}').status_code
                print('!UNBLOCKED')
                continue
            if last >= max_combo_to_block:
                print('>>> BLOCKED')
                print('NOTE: Сработала защита от спама вкладок в браузере, ведь подряд было открыто <max_combo_to_block> вкладок')
                sleep(5)
                exit()
            print('^^^^^===^^^===========================================')
            if is_open:
                webbrowser.open(f'{site}/{s}', new=2)
            if is_write:
                with open('urls', 'a') as f:
                    f.write(f'{site}/{s}\n')
            last += 1
        else:
            last = 0

if __name__ == '__main__':
    for w in range(processes):  
        p = Process(target=run)  
        p.start()



