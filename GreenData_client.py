from Graph_interface import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets


class Green_app(Ui_MainWindow, QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)





app = QtWidgets.QApplication([])
window = Green_app()
window.show()
app.exec()

