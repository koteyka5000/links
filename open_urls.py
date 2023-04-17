import webbrowser

with open('urls', 'r') as f:
    urls = f.readlines()
    for url in urls:
        if url != '':
            webbrowser.open(url, new=2)