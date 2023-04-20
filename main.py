import webbrowser  # Для открытия ссылок в браузере
import requests  # Для проверки кода ответа от сайта
import random  # Для генерации случайной ссылки
from multiprocessing import Process, current_process  # Для работы в нескольких процессах одновременно
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
continue_if_blocked = True # Продолжать ли выполнение программы при блокировке со стороны сайта
exit_if_wrong_dir = True  # Завершать ли программу если она запустилась в месте, где нет файла urls 

#  'текст, который нужно найти в ссылке': 'файл для записи ссылки, если в ней есть этот текст'
#   Файлы самим создавать не надо, всё автоматически
split_sites = {'https://cards.metro-cc.ru/': 'urls_metro.txt',
               '.img.avito.st/image': 'urls_avito.txt',
               'https://t.me': 'urls_tg.txt',
               'google': 'urls_google_yandex.txt',
               'yandex': 'urls_google_yandex.txt',
               }
write_in_both_files = False  # Записывать ли ссылки, для которых есть свой файл, 
                             # указанный в split_sites, дополнительно и в основной файл urls (кроме metro)
write_errors_in_extra_file = True  # Записывать ли ссылки, которые выдали ошибку при запросе в отдельный файл для ошибок

try:
    with open('urls', 'r'):
        pass
except:
    print('Нету файла, возможно неверна директория')
    if exit_if_wrong_dir:
        exit()

def write(file, url, redirected_url, after_separator=None):
    with open(file, 'a') as f:
        now = datetime.datetime.now()
        time = now.strftime("%d.%m %H:%M:%S")
        if after_separator:
            f.write(f'[{time}] -> {url} | {after_separator}\n')
        elif url == redirected_url:
            if write_errors_in_extra_file:  # Если записывать ошибки в отдельный файл
                write('urls_error.txt', url, None, '!')
            else:
                f.write(f'[{time}] -> {url} | !\n')
        else:
            f.write(f'[{time}] -> {url} | {redirected_url}\n')

def run():
    combo_opened_urls = 0
    status_code = None
    
    while 1:
        s = ''
        for i in range(string_len):
            s += random.choice(alpha)
        url = f'{site}/{s}'

        # Первая защита
        try:
            r = requests.head(url)
        except:
            print('FAILED TO REQUEST!')
            sleep(3)
            continue

        status_code = r.status_code
        print(f'{s} > {status_code}')

        if status_code != 404:
            # Вторая защита
            if status_code == 429:
                print(f'===BLOCKED=== via > {current_process().name}')
                if not continue_if_blocked:
                    exit()
                #  NOTE: Попробуй использовать меньше процессов, ведь сайт заблокировал запросы за слишком частую отправку
                while status_code == 429:
                    sleep(1)
                    status_code = requests.head(url).status_code
                print(f'>>>UNBLOCKED via > {current_process().name}')
                continue

            print('^^^^^===^^^===========================================')

            # Третья защита
            if combo_opened_urls >= max_combo_to_block:
                print(f'>>> BLOCKED via > {current_process().name}')
                print('NOTE: Сработала защита от спама вкладок в браузере, ведь подряд было открыто <max_combo_to_block> вкладок')
                sleep(5)
                exit()

            # Четвёртая защита
            try:
                r = requests.get(url) # head не содержит переадресованной ссылки, а get содержит, но get работает медленнее
            except:
                if write_errors_in_extra_file:
                    write('urls_error.txt', url, None, 'FATAL ERROR')
                else:
                    write('urls', url, None, 'FATAL ERROR')
                continue

            combo_opened_urls += 1

            if is_open:  # Если открывать ссылку
                webbrowser.open(url, new=2)

            if is_write: # Если вообще хоть что-то записывать 
                wrote_in_extra_file = False
                for split_site in split_sites:
                    if split_site in r.url:
                        print(f'=={split_site}==')
                        write(split_sites[split_site], url, r.url)
                        wrote_in_extra_file = True
                        break

            

                if 'https://cards.metro-cc.ru/' in r.url:  # Метро всегда записываем в отдельный файл
                    continue

                if wrote_in_extra_file and not write_in_both_files:  # Если мы уже записали в файл и не хотим чтобы ссылка была в обоих
                    continue

              
                write('urls', url, r.url)
            
        else:
            combo_opened_urls = 0

if __name__ == '__main__':
    if processes == 1:
        run()
    else:
        for w in range(processes):  
            p = Process(target=run)  
            p.start()
