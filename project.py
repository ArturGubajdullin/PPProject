# -*- coding: utf8 -*-
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem

import requests
from bs4 import BeautifulSoup as BS


def srez(str, start, end):
    startID = str.find(start)
    str = str[startID+len(start):]
    endID = str.find(end)
    str = str[:endID]
    return str


def get_url_ecatalog(name, platform):
    name = name.split()
    req = 'https://www.google.com/search?q=ecatalog+'
    for i in name:
        req += i+'+'
    platform = platform.split()
    for i in platform:
        req += i + '+'
    req[:-1]
    r = requests.get(req)
    soup = BS(r.text, "html.parser")
    url = 'https://www.e-katalog.ru/list/' + \
        srez(str(soup), 'https://www.e-katalog.ru/list/', '&amp')

    return ecatalog(url)


def ecatalog(url):
    table_data = {'Магазин': [], 'Название игры': [], 'Цена': [], 'Ссылка': []}

    r = requests.get(url)
    soup = BS(r.text, "html.parser")
    info = str(soup)
    ind = 0
    while ind != -1:
        ind = str(info).find('Купить в')
        info = str(info)[ind+7:]
        name_shop = srez(info, 'Купить в ', '!"')
        name_game = srez(info, '!"> ', '</a>')
        price = srez(info, 'prl_=', '"')
        href = srez(info, 'this.href="', '&amp')
        if len(name_shop) > 100:
            break

        table_data["Магазин"].append(name_shop)
        table_data['Название игры'].append(name_game)
        table_data['Цена'].append(price)
        table_data['Ссылка'].append(href)

        ind = str(info).find('Купить в')
        info = str(info)[ind+7:]
    return table_data


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 800, 300)
        self.setWindowTitle('Поиск игр')

        self.input_game_name_label = QLabel('Введите название игры:', self)
        self.input_game_name_label.resize(
            self.input_game_name_label.sizeHint())
        self.input_game_name_label.move(10, 0)

        self.input_game_name = QLineEdit(self)
        self.input_game_name.move(10, 20)
        self.input_game_name.resize(500, 40)

        self.list_platforms = QComboBox(self)
        self.list_platforms.addItems(["PS4", "PS5",
                                      "XBOX ONE/SX", "XBOX 360", "PC", "Nintendo Switch"])
        self.list_platforms.move(550, 30)

        self.button_get_games_list = QPushButton('Поиск', self)
        self.button_get_games_list.resize(
            self.button_get_games_list.sizeHint())
        self.button_get_games_list.move(245, 70)
        self.button_get_games_list.clicked.connect(self.show_game_list_window)

    def show_game_list_window(self):
        global game_list_window

        data = get_url_ecatalog(
            self.input_game_name.text(), self.list_platforms.currentText())
        game_list_window = GameListWindow(data, len(data['Цена']), 4)
        game_list_window.show()

    def get_game_name(self):
        print(self.input_game_name.text())
        print(self.list_platforms.currentText())


class GameListWindow(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setGeometry(app.desktop().availableGeometry())
        self.setWindowTitle('Найденные игры')

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = MainWindow()
    start_window.show()

    sys.exit(app.exec())
