links = []
count_repeats = 0

file = 'urls_tg.txt'
with open(file, 'r') as f:
    urls = f.readlines()
    for url in urls:
        start = url.find('->') + 3
        stop = url.find(' | ')
        url = url[start:stop]
        if url in links:
            print(url)
            count_repeats += 1
        links.append(url)

print(f'Повторений: {count_repeats}')