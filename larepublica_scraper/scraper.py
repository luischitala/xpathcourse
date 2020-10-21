import requests
import lxml.html as html
#
import os
import datetime

HOME_URL = 'https://www.larepublica.co/'
XPATH_LINK_TO_ARTICLE = '//h2/a/@href'
XPATH_TITLE = '//div[@class="mb-auto"]/h2/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_AUTHOR = '//div[@class="autorArticle"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

def get_title(link):
    url = link.split('/')[-1]
    title_list = url.split('-')[:-1]
    title = " ".join(title_list)
    return(title)

def parse_new(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            new = response.content.decode('utf-8')
            parsed = html.fromstring(new)
            try:
                title = get_title(link)
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                print(summary)
                body = parsed.xpath(XPATH_BODY)
                print(body)
                author = parsed.xpath(XPATH_AUTHOR)[0]
            except IndexError:
                return
            #Manejador contextual de python
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                f.write(author)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_news = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_news)

            today = datetime.date.today().strftime('%d-%m-%Y')
            #Si no existe la carpeta escribirla
            print("Hola")
            if not os.path.isdir(today):
                print('PRro')
                os.mkdir(today)
            for link in links_to_news:
                parse_new(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()
