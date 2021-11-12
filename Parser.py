from platform import platform
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


class Parsing_Manager():
    def __init__(self):
        self.URLS = {
            'PS5': {'MVideo': 'https://www.mvideo.ru/playstation-4327/ps5-igry-22780',
                    'DNS': 'https://www.dns-shop.ru/catalog/17a897ed16404e77/?f[s04a]=13tfwb&p=1',
                    'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya-sony-playstation-5/?page=1'},

            'PS4': {'MVideo': 'https://www.mvideo.ru/playstation-4327/ps4-igry-4331/f/category=igry-dlya-playstation-4-ps4-4343',
                    'DNS': 'https://www.dns-shop.ru/catalog/17a897ed16404e77/igry-dlya-playstation/?f[s04a]=13tfwc&f[s03t]=13tgsr&p=1',
                    'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/281308688/?f_278744964=4314&page=1'},

            'XBOX Series S/X': {'MVideo': 'https://www.mvideo.ru/xbox-4330/xbox-igry-4338/f/category=igry-dlya-xbox-1443/platforma=xbox-series-x',
                                'DNS': 'https://www.dns-shop.ru/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?f[s055]=16ikdl-13tidz&f[s054]=13thn1&p=1',
                                'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya-microsoft-xbox-series-x-s/?page=1'},

            'XBOX ONE': {'MVideo': 'https://www.mvideo.ru/xbox-4330/xbox-igry-4338/f/category=igry-dlya-xbox-1443/platforma=xbox-one,xbox-series-x---xbox-one',
                         'DNS': 'https://www.dns-shop.ru/catalog/17a9f99116404e77/igry-dlya-microsoft-xbox/?f[s055]=13tidy&f[s054]=13thn1&p=1',
                         'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/281308700/?page=1'},

            'Nintendo Switch': {'MVideo': 'https://www.mvideo.ru/nintendo-4927/nintendo-igry-4929/f/category=igry-dlya-nintendo-switch-1242',
                                'DNS': 'https://www.dns-shop.ru/catalog/17a8b09516404e77/igry-dlya-nintendo/?f[s05z]=13tk4k&f[s060]=13tkvd&p=1',
                                'Eldorado': 'https://www.eldorado.ru/c/vse-igry/f/dlya_nintendo_switch/?page=1'}
        }
        #хранение всех ссылок для будущего взятия

    def srez(str, start, end):
        """обрезает строку для нужных параметров"""
        startID = str.find(start)
        str = str[startID+len(start):]
        endID = str.find(end)
        str = str[:endID]
        return str

    def get_from_shop(self, shop_name_from_dictionary, url, platform):
        """вызов нужной функции для каждого магазина"""
        if shop_name_from_dictionary == 'DNS':
            return self.dns(url, platform)
        #если вызывается ДНС, то выводит ДНС
        elif shop_name_from_dictionary == 'MVideo':
            return self.mvideo(url, platform)
        #если вызывается Мвидео, то выводит Мвидео
        # elif shop_name_from_dictionary == 'Eldorado': # временно не работает
        #    return self.eldorado(url, platform)

    def mvideo(self, url, platform):
        """парсинг Мвидео"""
        shop_name = 'Мвидео'
        get_url = url + '?page=1'
        #перебор страниц
        games_count = [None]
        #количество найденных игр

        all_games_list = []
        #таблица с играми
        all_gamecards_list = []
        #таблица с товарами

        browser = webdriver.Chrome(ChromeDriverManager().install())
        #создание браузера

        def get_html(url):

            browser.get(url)
            #открытие ссылки в браузере
            browser.maximize_window()
            time.sleep(10)
            #10 секунд ждет подгрузки

            scrollHeight = browser.execute_script(
                "return document.documentElement.scrollHeight")

            height = 500
            #объем просмотра страницы для браузера 500 пикселей
            while height <= scrollHeight:
                #пока не дойду до конца страницы
                browser.execute_script(f'window.scrollTo(0, "{str(height)}");')
                height += 250
                #одна прокрутка = 250 пикселей
                time.sleep(1)
                #ожидание прогрузки каждой страницы

            html = browser.execute_script(
                "return document.body.innerHTML;")
            #получение полного кода html

            if games_count[0] == None:
                games_count[0] = int(
                    Parsing_Manager.srez(html, 'class="count ng-star-inserted">', '</span>')) - 24
                #количество найденных игр - уже рассмотренные игры

            time.sleep(2)
            #ожидание полного процесса осмотра

            return html

        def get_game_mvideo(html):
            games_list = []
            gamecards_list = []
            while 'product-picture-link' in html:
                url = Parsing_Manager.srez(
                    html, 'product-picture-link" href="', '"')
                html = html[html.find('product-picture-link"') + 1:]
                url = url.strip()

                stock = Parsing_Manager.srez(
                    html, 'class="product-notification">', '<')
                html = html[html.find('class="product-notification">') + 1:]
                stock = stock.replace('\n', '')
                #убирание всех переходов к следующей строке
                stock = stock.strip()

                name = Parsing_Manager.srez(
                    html, f'clamp" href="{url}"> ', '<')
                html = html[html.find(f'clamp" href="{url}"> ') + 1:]
                name = name.replace('игра', '')
                name = name.replace('Игра', '')
                name = name.replace('Игра Nintendo Switch ', '')
                name = name.replace('PS5', '')
                name = name.replace('PS4', '')
                name = name.replace('PC', '')
                name = name.replace('Xbox', '')
                publishers = ('Ubisoft', '505 Games', 'Activision', 'Bandai Namco', 'Bethesda', 'Cl Games', 'Capcom', 'Deep Silver', 'EA',
                              'Focus Home', 'Microids', 'Milestone', 'Sega', 'Sony', 'Square Enix', 'Take-Two', 'Techland', 'Ubisoft', 'WB')
                for el in publishers:
                    name = name.replace(el, '')

                name = name.strip()
                #выброс лишних слов из названия игры

                price = Parsing_Manager.srez(
                    html, '="price__main-value">', '<')
                html = html[html.find('="price__main-value">') + 1:]
                price = price.replace('&nbsp;', '')
                #выброс знака пробела
                price = price.replace('₽', '')
                #выброс знака рубля
                price = price.strip()

                if 'Подписка' not in name:
                    gamecards_list.append(
                        (name+' '+platform, shop_name, price, url, stock, platform))
                    games_list.append((name+' '+platform, platform))

            return (gamecards_list, games_list)
            #возвращение кортежа их двух списков

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
            #пока страница не последняя или пока есть еще игры
            lists = get_game_mvideo(get_html(get_url))
            #призыв функции get_html и получение всез игр с первой страницы
            all_gamecards_list += lists[0]
            #добавление к all_gamecards_list все найденные данные на текущей странице
            all_games_list += lists[1]
            #добавление к all_gamecards_list все найденные данные на следующей странице
            current_page += 1
            #переход к следующей странице
            get_url = get_url[:-1] + str(current_page)
            #изменение полседнего символа(который меняется) на новый
            games_count[0] -= 24
            #вычитание уже рассмотренных игр
        #перебор страниц

        browser.quit()
        #завершение работы с браузером

        for index, game in enumerate(all_gamecards_list):
            for i, el in enumerate(game):
                if 'mvideo' in el and i != 3:
                    #если есть mvideo и i №3
                    all_gamecards_list.remove(game)
                    #удаление неправильной цены
                    break
        return (all_gamecards_list, all_games_list)
        #проверка на правильное получение цены


    def dns(self, url, platform):
        """"парсинг днс"""
        shop_name = 'DNS'
        get_url = url
        games_count = [None]
        all_gamecards_list = []
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
                count = Parsing_Manager.srez(
                    html, 'class="products-count">', '</span>')
                games_count[0] = int(
                    ''.join(i for i in count if i.isdigit())) - 18

            time.sleep(2)

            return html

        def get_game_dns(html):
            games_list = []
            gamecards_list = []
            while 'image-link" href="' in html:
                url = 'https://www.dns-shop.ru/' + \
                    Parsing_Manager.srez(html, 'image-link" href="', '"')
                html = html[html.find('image-link" href="') + 1:]
                url = url.strip()

                name = Parsing_Manager.srez(html, 'webp"><img alt="', '"')
                html = html[html.find('webp"><img alt="') + 1:]
                name = name.replace('&amp; ', '')
                name = name.replace('&quot;', '')
                name = name.replace('PS5', '')
                name = name.replace('PS4', '')
                name = name.replace('Switch', '')
                name = name.replace('Xbox ONE', '')
                name = name.replace('Xbox Series X', '')
                name = name.replace('Xbox Series S', '')
                name = name.replace('Xbox 360', '')
                name = name.replace('()', '')
                name = name.replace('(,)', '')
                name = name.replace('(,,)', '')
                name = name.replace('(,,,)', '')
                name = name.replace('(,,,,)', '')
                name = name.replace('Игра', '')
                name = name.strip()
                #выброс лишних слов из названия
                price = Parsing_Manager.srez(
                    html, 'class="product-buy__price">', '<')
                html = html[html.find('class="product-buy__price">') + 1:]
                price = price.replace('₽', '')
                price = price.replace(' ', '')
                price = price.strip()
                #выброс лишних символов из цены

                stock = Parsing_Manager.srez(
                    html, 'span class="available">', '<')
                html = html[html.find('span class="available">') + 1:]
                stock = stock.replace(':', '')
                #удаление лишних символом из stock
                stock = stock.replace('В магазинах', 'В наличии')
                #изменение надписи для единого стиля
                stock = stock.strip()

                if '₽' not in stock:
                    gamecards_list.append(
                        (name+' '+platform, shop_name, price, url, stock, platform))
                    games_list.append((name+' '+platform, platform))
                #добавление символа при его наличии

            return (gamecards_list, games_list)

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
        # #пока страница не последняя или пока есть еще игры
            lists = get_game_dns(get_html(get_url))
            #призыв функции get_html и получение всез игр с первой страницы
            all_gamecards_list += lists[0]
            #добавление к all_gamecards_list все найденные данные на текущей странице
            all_games_list += lists[1]
            #добавление к all_gamecards_list все найденные данные на следующей странице
            current_page += 1
            #переход к следующей странице
            get_url = get_url[:-1] + str(current_page)
            #изменение полседнего символа(который меняется) на новый
            games_count[0] -= 18
            #вычитание уже рассмотренных игр

        browser.quit()
        # завершение работы с браузером

        # for index, game in enumerate(all_gamecards_list):
        #     for i, el in enumerate(game):
        #         if 'mvideo' in el and i != 3:
        #             all_gamecards_list.pop(index)
        return (all_gamecards_list, all_games_list)

    def eldorado(self, url, platform):
        """"парсинг эльдорадо"""
        shop_name = 'Эльдорадо'
        get_url = url
        games_count = [None]
        all_gamecards_list = []
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
                    Parsing_Manager.srez(html, 'data-pc="offers_cnt">', '</span>')) - 36

            time.sleep(2)

            return html

        def get_game_eldorado(html):
            gamecards_list = []
            games_list = []
            while '"><a class="qD" href="' in html:
                url = 'https://www.eldorado.ru' + \
                    Parsing_Manager.srez(html, '"><a class="qD" href="', '"')
                html = html[html.find('"><a class="qD" href="') + 1:]

                if '<span class="bK dK">' in html[:5000]:
                    stock = 'Нет в наличии'
                else:
                    stock = 'В наличии'

                name = Parsing_Manager.srez(html, 'data-dy="title">', '<')
                html = html[html.find('data-dy="title">') + 1:]

                price = Parsing_Manager.srez(
                    html, 'data-pc="offer_price">', '<')
                html = html[html.find('data-pc="offer_price">') + 1:]

                gamecards_list.append(
                    (name+' '+platform, shop_name, price, url, stock, platform))
                games_list.append((name+' '+platform, platform))

            return (gamecards_list, games_list)

        current_page = 1
        while games_count[0] == None or games_count[0] > 0:
            lists = get_game_eldorado(get_html(get_url))
            all_gamecards_list += lists[0]
            all_games_list += lists[1]
            current_page += 1
            get_url = get_url[:-1] + str(current_page)
            games_count[0] -= 36

        browser.quit()
        return (all_gamecards_list, all_games_list)
