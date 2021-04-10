from Graph_interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import time
from datetime import datetime


class Green_app(Ui_MainWindow, QtWidgets.QMainWindow):
    #Створюємо метод для ініціалізації і передаємо super(), щоб батьківський клас наслідував методи дочірнього
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Назначеаємо кнопки під необхідні методи класу
        self.pushButton.pressed.connect(self.add_sowing)
        self.pushButton_2.pressed.connect(self.get_sowing)
        self.pushButton_3.pressed.connect(self.add_expenditure)
        self.pushButton_4.pressed.connect(self.add_income)
        self.pushButton_5.pressed.connect(self.get_income)

    def add_sowing(self):
        #метод для додавання в базу необхідної інформації про посів
        current_year = datetime.now()
        add_time = time.ctime()
        data = self.textEdit_2.toPlainText()
        year = current_year.year

        #підключаємо базу і додаємо та демонструємо інформацію про посів, і для перестраховки обробляємо помилки
        try:
            sqlite_connection = sqlite3.connect('Sowing_data.db')
            cursor = sqlite_connection.cursor()
            sowing = (add_time, data, year)
            cursor.execute('INSERT INTO Sowings VALUES(?, ?, ?);', sowing)
            sqlite_connection.commit()
            sqlite_connection.close()
            self.textBrowser.append(add_time + '  ' + data)
        except:
            self.textBrowser.append('Помилка бази')

        self.textEdit_2.clear()

    def get_sowing(self):
        #Метод для отримання інформації за певний період
        #Підключаємося до бази, отримуємо данні і виводимо необхідні, обов'язково обробляємо помилки при роботі з БД
        try:
            sqlite_connection = sqlite3.connect('Sowing_data.db')
            cursor = sqlite_connection.cursor()
            get_year = self.textEdit.toPlainText()
            cursor.execute('SELECT * FROM Sowings')
            data = cursor.fetchall()
            for row in data:
                if row[2] == int(get_year):
                    self.textBrowser.append(row[0] + '  ' + row[1])
            sqlite_connection.close()
        except:
            self.textBrowser.append('Помилка бази')

    def add_expenditure(self):
        sqlite_connection = sqlite3.connect('Finance_data.db')
        cursor = sqlite_connection.cursor()

    def add_income(self):
        sqlite_connection = sqlite3.connect('Finance_data.db')
        cursor = sqlite_connection.cursor()

    def get_income(self):
        sqlite_connection = sqlite3.connect('Finance_data.db')
        cursor = sqlite_connection.cursor()


app = QtWidgets.QApplication([])
window = Green_app()
window.show()
app.exec()


