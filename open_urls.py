import webbrowser

with open('urls', 'r') as f:
    urls = f.readlines()
    # if not input(f"Откроется {len(urls)} вкладок, нажми Enter чтобы отменить или введи что-то чтобы продолжить"):
    #     exit()
    for url in urls:
        start = url.find('->') + 3
        stop = url.find(' | ')
        webbrowser.open((url[start:stop]), new=2)