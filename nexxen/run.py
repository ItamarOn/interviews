import requests
from bs4 import BeautifulSoup
import validators

def get_urls():
    with open('urls.txt', 'r') as f:
        urls = f.readlines()
    return [u.replace('\n', '') for u in urls]

if __name__ == '__main__':
    urls = get_urls()
    contents = {}
    for url in urls:
        try:
            response = requests.get(url)
        except Exception as ex:
            print(f"{url}  - Error: {ex}")
            continue
        if response.ok:
            contents[url] = response.text

    print('contents')

    cont = {}
    for url, content in contents.items():
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title').text
        links = set()
        for a in soup.find_all('a'):
            if a.get('href').startswith('/'):
                link = requests.compat.urljoin(url, a.get('href'))
            else:
                link = a.get('href')

            if validators.url(link):
                links.add(link)

        cont[url] = {'title': title, 'links': links}


    print('----------')
    print(cont)
    print('----------')
"""
url: { title: '',  # <title . text
       links: [",'', '', ''],  # <a . href
       }
       
relative 2 absulte
http://www.google.com/a/b
href=/about
http://www.google.com/about
"""
