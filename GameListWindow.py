from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
from tabulate import tabulate
from Dialog import Custom_Dialog


class GameListWindow(QTableWidget):

    def __init__(self, data, *args):
        #создание нового окна с аргументом data
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        #количество колонок
        self.resizeRowsToContents()
        #количество строк
        self.showMaximized()
        #вывод на весь экран
        self.setWindowTitle('Найденные игры')
        #наименование окна
        self.write_to_file(data)

    def setData(self):
        """построение таблицы"""
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            #перебор переданных данных из table_data с порчдковым номером n в списке
            horHeaders.append(key)
            #добавление подписи стобца
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                #создание специального объекта дял каждого столбца для размещения в таблице
                self.setItem(m, n, newitem)
                #размещение в таблице с координата m и n
        self.setHorizontalHeaderLabels(horHeaders)
        #выдача наименования столбцов

    def write_to_file(self, data):
        dlg_update_DB_question = Custom_Dialog('write_to_file_question')
        answer = dlg_update_DB_question.exec()
        if answer == 1:
            try:
                with open('out.txt', 'w', encoding='utf-8') as file:
                    file.write(tabulate(data, headers="keys"))
                    QMessageBox.information(
                        self, 'Успешно', "Данные успешно записаны в 'out.txt'")
            except:
                QMessageBox.critical(
                    self, 'Ошибка', "Данные не были записаны в 'out.txt'")
