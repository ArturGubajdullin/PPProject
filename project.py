# -*- coding: utf8 -*-
import sys
#импорт системных файлов
from PyQt5.QtWidgets import QApplication
#импорт библиотеки для главного окна
from MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #создание главного окна
    start_window = MainWindow()
    #присваивание класса к переменной чтобы окно не закрывалось при открытии
    start_window.show()
    sys.exit(app.exec())
    #закрытие главного окна и передача данных о закрытии