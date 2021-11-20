import sys
import sqlite3
from PyQt5 import QtWidgets, QtCore, QtGui, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()

    def initUi(self):
        uic.loadUi('main.ui', self)
        self.update_data()

    def get_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        data = cursor.execute("""select sort, roasting,
         grains, description, price, volume from coffee""").fetchall()
        return data

    def update_data(self):
        data = self.get_data()

        self.table.clear()
        self.table.setRowCount(len(data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['сорт', "обжарка", "молотый/в зёрнах",
                                              "Описание", "Цена", "Объём упаковки"])

        for i, row in enumerate(data):
            for j, text in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(text))
                self.table.setItem(i, j, item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
