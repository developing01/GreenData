from Graph_interface import Ui_MainWindow
from PyQt5 import QtWidgets
import sqlite3
import time
from datetime import datetime


class Green_app(Ui_MainWindow, QtWidgets.QMainWindow):
    #Створюємо метод для ініціалізації і передаємо super(), щоб батьківський клас наслідував методи дочірнього
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #Запускаємо метод для створення баз данних якщо вони ще не існують
        self.create_DB()

        #Назначеаємо кнопки під необхідні методи класу
        self.pushButton.pressed.connect(self.add_sowing)
        self.pushButton_2.pressed.connect(self.get_sowing)
        self.pushButton_3.pressed.connect(self.add_expenditure)
        self.pushButton_4.pressed.connect(self.add_income)
        self.pushButton_5.pressed.connect(self.get_income)

        #При запуску додатку виводить список останніх доданих фінансових данних
        self.show_activity()


    #метод для створення баз данних
    def create_DB(self):
        sqlite_connection_sowing = sqlite3.connect('Sowing_data.db')
        sqlite_connection_finance = sqlite3.connect('Finance_data.db')
        sowing_cursor = sqlite_connection_sowing.cursor()
        finance_cursor = sqlite_connection_finance.cursor()

        sowing_cursor.execute('''CREATE TABLE IF NOT EXISTS Sowings(
                              time TEXT,
                              data TEXT,
                              year INT);
                              ''')
        sqlite_connection_sowing.commit()

        finance_cursor.execute('''CREATE TABLE IF NOT EXISTS Finances(
                                object TEXT,
                                data INT,
                                year INT);
                                ''')
        sqlite_connection_finance.commit()
        sqlite_connection_sowing.close()
        sqlite_connection_finance.close()

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
            self.textBrowser.append('Треба ввести необхідні данні, або виникла помилка бази данних...')

        self.textEdit_2.clear()

    def get_sowing(self):
        #Метод для отримання інформації за певний період
        #Підключаємося до бази, отримуємо данні і виводимо необхідні, обов'язково обробляємо помилки при роботі з БД
        self.textBrowser.clear()
        try:
            sqlite_connection = sqlite3.connect('Sowing_data.db')
            cursor = sqlite_connection.cursor()
            get_year = self.textEdit.toPlainText()
            cursor.execute('SELECT * FROM Sowings;')
            data = cursor.fetchall()
            for row in data:
                if row[2] == int(get_year):
                    self.textBrowser.append(row[0] + '  ' + row[1])
            sqlite_connection.close()
        except:
            self.textBrowser.append('Треба ввести необхідні данні, або виникла помилка бази данних...')
    #метод для виведення данних при запуску
    def show_activity(self):
        try:
            sql_connection = sqlite3.connect('Finance_data.db')
            cursor = sql_connection.cursor()
            cursor.execute('SELECT * FROM Finances;')
            data = cursor.fetchall()
            for row in data:
                self.textBrowser_2.append('рік ' + str(row[2]) + '    ' + row[0] + '  ' + str(row[1]))
            sql_connection.close()
        except:
            self.textBrowser_2.append('POW')

    #метод для додавання витрати, для фінансових данних створили іншу базу
    def add_expenditure(self):
        object_exp = self.textEdit_3.toPlainText()
        current_year = datetime.now()
        year = current_year.year
        data = int(self.textEdit_4.toPlainText())

        expenditure = (object_exp, -data, year)

        try:
            sqlite_connection = sqlite3.connect('Finance_data.db')
            cursor = sqlite_connection.cursor()
            cursor.execute('INSERT INTO Finances VALUES(?, ?, ?);', expenditure)
            sqlite_connection.commit()
            self.textBrowser_2.append(time.ctime() + '  ' + object_exp + '  -' + str(data))

            sqlite_connection.close()
        except:
            self.textBrowser_2.append('Треба ввести необхідні данні, або виникла помилка бази данних...')

    #метод для додавання доходів
    def add_income(self):
        data = self.textEdit_5.toPlainText()
        current_year = datetime.now()
        year = current_year.year
        income = ('', data, year)
        try:
            sqlite_connection = sqlite3.connect('Finance_data.db')
            cursor = sqlite_connection.cursor()
            cursor.execute('INSERT INTO Finances VALUES(?, ?, ?);', income)
            sqlite_connection.commit()
            self.textBrowser_2.append(time.ctime() + '  +' + str(data))

            sqlite_connection.close()
        except:
            self.textBrowser_2.append('Треба ввести необхідні данні, або виникла помилка бази данних...')

    #метод для отримання доходу за певний рік
    def get_income(self):
        self.textBrowser_3.clear()
        year = self.textEdit_6.toPlainText()
        try:
            sqlite_connection = sqlite3.connect('Finance_data.db')
            cursor = sqlite_connection.cursor()
            cursor.execute('SELECT * FROM Finances;')
            data = cursor.fetchall()
            all_income = 0
            for row in data:
                if row[2] == int(year):
                    all_income += row[1]
            self.textBrowser_3.append(str(all_income))
            sqlite_connection.close()
        except:
            self.textBrowser_3.append('Треба ввести необхідні данні, або виникла помилка бази данних...')


#для запуску додатку створюємо об'єкт класу Green_app і запускаємо за допомогою методу show
app = QtWidgets.QApplication([])
window = Green_app()
window.show()
app.exec()
