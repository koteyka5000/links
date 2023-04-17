import webbrowser

with open('urls', 'r') as f:
    urls = f.readlines()
    for url in urls:
        start = url.find('->') + 3
        stop = url.find(' | ')
        print(url[start:stop])