# _*_coding: utf-8_*_
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


class Parser():
    PS5_links = {'MVideo': 'https://www.mvideo.ru/playstation-4327/ps5-igry-22780',
                 'DNS': 'https://www.dns-shop.ru/catalog/17a897ed16404e77/?f[s04a]=13tfwb&p=1',
                 'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya-sony-playstation-5/?page=1'}

    PS4_links = {'MVideo': 'https://www.mvideo.ru/playstation-4327/ps4-igry-4331/f/category=igry-dlya-playstation-4-ps4-4343',
                 'DNS': 'https://www.dns-shop.ru/catalog/17a897ed16404e77/igry-dlya-playstation/?f[s04a]=13tfwc&f[s03t]=13tgsr&p=1',
                 'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/281308688/?f_278744964=4314&page=1'}

    XBSX_links = {'MVideo': 'https://www.mvideo.ru/xbox-4330/xbox-igry-4338/f/category=igry-dlya-xbox-1443/platforma=xbox-series-x',
                  'DNS': 'https://www.dns-shop.ru/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?f[s055]=16ikdl-13tidz&f[s054]=13thn1&p=1',
                  'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya-microsoft-xbox-series-x-s/?page=1'}

    XBO_links = {'MVideo': 'https://www.mvideo.ru/xbox-4330/xbox-igry-4338/f/category=igry-dlya-xbox-1443/platforma=xbox-one,xbox-series-x---xbox-one',
                 'DNS': 'https://www.dns-shop.ru/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?f[s055]=13tidy&f[s054]=13thn1&p=1',
                 'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/281308700/?page=1'}

    NS_links = {'MVideo': 'https://www.mvideo.ru/nintendo-4927/nintendo-igry-4929/f/category=igry-dlya-nintendo-switch-1242',
                'DNS': 'https://www.dns-shop.ru/catalog/17a8b09516404e77/igry-dlya-nintendo/?f[s05z]=13tk4k&f[s060]=13tkvd&p=1',
                'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya_nintendo_switch/?page=1'}

    def srez(str, start, end):
        startID = str.find(start)
        str = str[startID+len(start):]
        endID = str.find(end)
        str = str[:endID]
        return str

    def mvideo(self, url):
        get_url = url + '?page=1'
        games_count = [None]
        all_games_list = []

        browser = webdriver.Chrome(ChromeDriverManager().install())

        def get_html(url):

            browser.get(url)
            browser.maximize_window()
            time.sleep(10)

            scrollHeight = browser.execute_script(
                "return document.documentElement.scrollHeight")

            height = 500
            while height <= scrollHeight:
                browser.execute_script(f'window.scrollTo(0, "{str(height)}");')
                height += 250
                time.sleep(1)

            html = browser.execute_script(
                "return document.body.innerHTML;")

            if games_count[0] == None:
                games_count[0] = int(
                    self.srez(html, 'class="count ng-star-inserted">', '</span>')) - 24

            time.sleep(2)

            return html

        def get_game_mvideo(html):
            games_list = []
            while 'product-picture-link' in html:
                url = self.srez(html, 'product-picture-link" href="', '"')
                html = html[html.find('product-picture-link"') + 1:]
                url = url.strip()

                stock = self.srez(html, 'class="product-notification">', '<')
                html = html[html.find('class="product-notification">') + 1:]
                stock = stock.replace('\n', '')
                stock = stock.strip()

                name = self.srez(html, f'clamp" href="{url}"> ', '<')
                html = html[html.find(f'clamp" href="{url}"> ') + 1:]
                name = name.replace('игра', '')
                name = name.replace('Игра Nintendo Switch ', '')
                name = name.replace('PS5', '')
                name = name.replace('PS4', '')
                name = name.replace('PC', '')
                name = name.replace('Xbox', '')
                name = name.strip()

                price = self.srez(html, '="price__main-value">', '<')
                html = html[html.find('="price__main-value">') + 1:]
                price = price.replace('&nbsp;', '')
                price = price.replace('₽', '')
                price = price.strip()

                if 'Подписка' not in name:
                    games_list.append([name, price, stock, url])

            return games_list

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
            all_games_list += get_game_mvideo(get_html(get_url))
            current_page += 1
            get_url = get_url[:-1] + str(current_page)
            games_count[0] -= 24

        browser.quit()

        for index, game in enumerate(all_games_list):
            for i, el in enumerate(game):
                if 'mvideo' in el and i != 3:
                    all_games_list.pop(index)
        return all_games_list

    def dns(self, url):
        get_url = url
        games_count = [None]
        all_games_list = []

        browser = webdriver.Chrome(ChromeDriverManager().install())

        def get_html(url):

            browser.get(url)
            browser.maximize_window()
            time.sleep(10)

            scrollHeight = browser.execute_script(
                "return document.documentElement.scrollHeight")

            height = 500
            while height <= scrollHeight:
                browser.execute_script(f'window.scrollTo(0, "{str(height)}");')
                height += 250
                time.sleep(1)

            html = browser.execute_script(
                "return document.body.innerHTML;")

            if games_count[0] == None:
                count = self.srez(html, 'class="products-count">', '</span>')
                games_count[0] = int(
                    ''.join(i for i in count if i.isdigit())) - 18

            time.sleep(2)

            return html

        def get_game_dns(html):
            games_list = []
            while 'image-link" href="' in html:
                url = 'https://www.dns-shop.ru/' + \
                    self.srez(html, 'image-link" href="', '"')
                html = html[html.find('image-link" href="') + 1:]
                url = url.strip()

                name = self.srez(html, 'webp"><img alt="', '"')
                html = html[html.find('webp"><img alt="') + 1:]
                name = name.replace('&amp; ', '')
                name = name.replace('&amp;', '')
                name = name.replace('(PS5)', '')
                name = name.replace('(PS4)', '')
                name = name.replace('Xbox ONE', '')
                name = name.replace('Xbox Series X', '')
                name = name.replace('Xbox Series S', '')
                name = name.replace('Xbox 360', '')
                name = name.replace('()', '')
                name = name.replace('(,)', '')
                name = name.replace('(,,)', '')
                name = name.replace('(,,,)', '')
                name = name.replace('(,,,,)', '')
                name = name.replace('(Switch)', '')
                name = name.replace('Игра', '')
                name = name.strip()

                price = self.srez(html, 'class="product-buy__price">', '<')
                html = html[html.find('class="product-buy__price">') + 1:]
                price = price.replace('₽', '')
                price = price.replace(' ', '')
                price = price.strip()

                stock = self.srez(html, 'span class="available">', '<')
                html = html[html.find('span class="available">') + 1:]
                stock = stock.replace(':', '')
                stock = stock.replace('В магазинах', 'В наличии')
                stock = stock.strip()

                if '₽' not in stock:
                    games_list.append([name, price, stock, url])

            return games_list

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
            all_games_list += get_game_dns(get_html(get_url))
            current_page += 1
            get_url = get_url[:-1] + str(current_page)
            games_count[0] -= 18

        browser.quit()

        # for index, game in enumerate(all_games_list):
        #     for i, el in enumerate(game):
        #         if 'mvideo' in el and i != 3:
        #             all_games_list.pop(index)
        return all_games_list

    def eldorado(self, url):
        get_url = url
        games_count = [None]
        all_games_list = []

        browser = webdriver.Chrome(ChromeDriverManager().install())

        def get_html(url):

            browser.get(url)
            browser.maximize_window()
            time.sleep(10)

            scrollHeight = browser.execute_script(
                "return document.documentElement.scrollHeight")

            height = 500
            while height <= scrollHeight:
                browser.execute_script(f'window.scrollTo(0, "{str(height)}");')
                height += 250
                time.sleep(1)

            html = browser.execute_script(
                "return document.body.innerHTML;")

            if games_count[0] == None:
                games_count[0] = int(
                    self.srez(html, 'data-pc="offers_cnt">', '</span>')) - 36

            time.sleep(2)

            return html

        def get_game_eldorado(html):
            games_list = []
            while '"><a class="qD" href="' in html:
                url = 'https://www.eldorado.ru' + \
                    self.srez(html, '"><a class="qD" href="', '"')
                html = html[html.find('"><a class="qD" href="') + 1:]

                if '<span class="bK dK">' in html[:5000]:
                    stock = 'Нет в наличии'
                else:
                    stock = 'В наличии'

                name = self.srez(html, 'data-dy="title">', '<')
                html = html[html.find('data-dy="title">') + 1:]

                price = self.srez(html, 'data-pc="offer_price">', '<')
                html = html[html.find('data-pc="offer_price">') + 1:]

                games_list.append([name, price, stock, url])

            return games_list

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
            all_games_list += get_game_eldorado(get_html(get_url))
            current_page += 1
            get_url = get_url[:-1] + str(current_page)
            games_count[0] -= 36

        browser.quit()
        return all_games_list
