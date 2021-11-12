from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox
from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCompleter
#импорт составляющих частей главного окна
from GameListWindow import GameListWindow
from Parser import Parsing_Manager
#импорт класса для работы с парсингом магазинов
from DB import DB_Manager
#импорт класса для управления базами данных
from Dialog import Custom_Dialog


class MainWindow(QWidget):
    game_list = []

    def __init__(self):
        super().__init__()
        self.initUI()
    #инициализация объекта

    def initUI(self):
        """Инициализация внешнего вида"""

        self.setGeometry(800, 300, 800, 300)
        #установка размеров окна
        self.setWindowTitle('Поиск игр')
        #установка наименования окна

        self.input_game_name_label = QLabel('Введите название игры:', self)
        self.input_game_name_label.resize(
            self.input_game_name_label.sizeHint())
        self.input_game_name_label.move(10, 50)
        self.input_game_name_label.hide()

        self.input_game_name = QLineEdit(self)
        #поле ввода названия игры
        self.game_name_completer = QCompleter(
            self.game_list, self.input_game_name)
        #выпадающий список предлогаемых игр
        self.game_name_completer.setCaseSensitivity(0)
        #чувствительность к регистру = 0(для избежания проблем с капсом)
        self.input_game_name.setCompleter(self.game_name_completer)
        self.input_game_name.move(10, 65)
        self.input_game_name.resize(500, 40)
        self.input_game_name.textChanged.connect(
            self.on_input_game_name_changed)
        self.input_game_name.hide()

        self.input_platform_label = QLabel('Выберите платформу:', self)
        self.input_platform_label.resize(
            self.input_platform_label.sizeHint())
        self.input_platform_label.move(10, 0)

        self.list_platforms = QComboBox(self)
        self.list_platforms.addItems(["", "PS4", "PS5",
                                      "XBOX ONE", "XBOX Series S/X", "Nintendo Switch"])
        #выпадающий список с платформами
        self.list_platforms.move(10, 20)
        self.list_platforms.currentTextChanged.connect(
            self.on_combobox_changed)

        self.button_get_games_list = QPushButton('Поиск', self)
        self.button_get_games_list.resize(
            self.button_get_games_list.sizeHint())
        self.button_get_games_list.move(10, 120)
        self.button_get_games_list.clicked.connect(self.show_game_list_window)
        self.button_get_games_list.hide()

        self.button_update_BD = QPushButton('Обновить базу данных', self)
        self.button_update_BD.resize(
            self.button_update_BD.sizeHint())
        self.button_update_BD.move(170, 15)
        self.button_update_BD.clicked.connect(lambda: self.fill_db(None))
        self.button_update_BD.hide()

        dlg_update_DB_question = Custom_Dialog('update_DB_question')
        #диалоговое окно "обновлять базу данных или нет?"
        answer = dlg_update_DB_question.exec()
        #получение ответа через фунцию .exec
        if answer == 1:
            #если ответ да
            dlg_update_DB = Custom_Dialog('update_DB')
            #диалоговое окно "для чего?"
            if dlg_update_DB.exec() == 1:
                #если ответ
                QMessageBox.information(
                    self, 'Внимание', 'Не закрывайте браузер, который будет открыт! (Его можно свернуть)')
                #.information это встроенное диалоговое окно с форматом "для информации"
                print(dlg_update_DB.list_platforms_dlg.currentText())
                self.fill_db(dlg_update_DB.list_platforms_dlg.currentText())

    def on_combobox_changed(self):
        """Вызывается при выборе другой платформы"""
        if self.list_platforms.currentText() != '':
            self.input_game_name.show()
            self.input_game_name_label.show()
            #показ поле ввода игры если платформа выбрана
            self.game_list = self.get_game_list_for_cur_platform(
                self.list_platforms.currentText())
            self.game_name_completer = QCompleter(
                self.game_list, self.input_game_name)
            self.input_game_name.setCompleter(self.game_name_completer)
            self.game_name_completer.setCaseSensitivity(0)

            if self.game_list == []:
                self.input_game_name_label.hide()
                self.input_game_name.hide()
                self.input_game_name.setText('')
        else:
            self.input_game_name_label.hide()
            self.input_game_name.setText('')
            self.input_game_name.hide()
            self.input_game_name_label.hide()

    def on_input_game_name_changed(self):
        """"Вызывается при вводе другой игры"""
        if self.input_game_name.text() in self.game_list:
            self.button_get_games_list.show()
            #если введеная игра есть в списке, то показать кнопку поиска
        else:
            self.button_get_games_list.hide()
            #иначе скрыть кнопку поиска

    def show_game_list_window(self):
        """Вывод второго окна с таблицей игр"""
        global game_list_window

        DB = DB_Manager('Games.db')
        #открытие объекта для управления базой данных
        data = DB.get_game_cards(self.input_game_name.text())
        #призыв функции для получения товаров из всех карточек товаров и передача названия
        table_data = {'Магазин': [], 'Название игры': [],
                      'Цена': [], 'Наличие': [], 'Ссылка': []}
        #создание столбцов для ввода информации
        for game in data:
            table_data['Название игры'].append(game[1])
            table_data['Магазин'].append(game[2])
            table_data['Цена'].append(str(game[3]))
            table_data['Наличие'].append(game[5])
            table_data['Ссылка'].append(game[4])
        DB.close()
        #закрытия базы данных
        game_list_window = GameListWindow(
            table_data, len(table_data['Ссылка']), len(table_data.keys()))
        game_list_window.show()

    def get_game_list_for_cur_platform(self, platform):
        """Вывод списка игр из базы данных для текущей платформы"""
        DB = DB_Manager('Games.db')
        game_list = []
        for game in DB.get_game_list_for_cur_platform(platform):
            game_list.append(game[0])
        DB.close()
        if game_list == []:
            self.button_update_BD.show()
            QMessageBox.warning(
                self, 'Ошибка', 'База данных пуста, нажмите "обновить базу"')
        else:
            self.button_update_BD.hide()

        return game_list

    def srez(self, str, start, end):
        """обрезает строку для нужных параметров"""
        startID = str.find(start)
        str = str[startID+len(start):]
        endID = str.find(end)
        str = str[:endID]
        return str

    def fill_db(self, platform_name=None):
        """заполнение базы данных"""
        DB = DB_Manager('Games.db')
        #обращение к базе данных
        list_gamecards, list_games = ([], [])
        #создание двух списков для подбора названия игры игры и платформы из базы данных в виде кортежа

        parser = Parsing_Manager()
        if platform_name == None:
            if self.list_platforms.currentText() != '':
                #подбор данных из выпадающего списка в главном окне и обновление всех баз банных
                for shop, link in parser.URLS[self.list_platforms.currentText()].items():
                    if shop != 'Eldorado':

                        tup = parser.get_from_shop(
                            shop, link, self.list_platforms.currentText())
                        list_gamecards, list_games = tup
                        DB.push_games_list_to_games(list_games)
                        DB.push_gamecards_list_to_gamecards(list_gamecards)
            else:
                for platform_name, dict in parser.URLS.items():
                    for shop, link in dict.items():
                        if shop != 'Eldorado':

                            list_gamecards, list_games = parser.get_from_shop(
                                shop, link, platform_name)
                            DB.push_games_list_to_games(list_games)
                            DB.push_gamecards_list_to_gamecards(list_gamecards)
        else:
            if platform_name != '':
                for shop, link in parser.URLS[platform_name].items():
                    if shop != 'Eldorado':
                        tup = parser.get_from_shop(
                            shop, link, platform_name)
                        # заполнение кортежа с магазином, ссылкой и платформой
                        list_gamecards, list_games = tup
                        DB.push_games_list_to_games(list_games)
                        DB.push_gamecards_list_to_gamecards(list_gamecards)
            else:
                for platform_name, dict in parser.URLS.items():
                    for shop, link in dict.items():
                        if shop != 'Eldorado':
                            list_gamecards, list_games = parser.get_from_shop(
                                shop, link, platform_name)
                            DB.push_games_list_to_games(list_games)
                            DB.push_gamecards_list_to_gamecards(list_gamecards)

        QMessageBox.information(self, 'Успешно', 'База данных обновлена!')
        DB.close()
