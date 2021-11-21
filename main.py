import sys
import sqlite3
from PyQt5 import QtWidgets
from UI.main import Ui_MainWindow
from UI.addEditCoffeeForm import Ui_Form


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.data = None
        self.initUi()

        self.pushButton.clicked.connect(self.init_record_add)
        self.table.itemDoubleClicked.connect(self.init_record_edit)

    def initUi(self):
        self.setupUi(self)
        self.update_data()

    def get_data(self):
        connection = sqlite3.connect('data/coffee.sqlite')
        cursor = connection.cursor()
        data = cursor.execute("""select * from coffee""").fetchall()
        connection.close()
        self.data = data

    def update_data(self):
        self.get_data()

        self.table.clear()
        self.table.setRowCount(len(self.data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['сорт', "обжарка", "молотый/в зёрнах",
                                              "Описание", "Цена", "Объём упаковки"])

        for i, row in enumerate(self.data):
            for j, text in enumerate(row):
                if j == 0:
                    continue
                item = QtWidgets.QTableWidgetItem(str(text))
                self.table.setItem(i, j - 1, item)

    def init_record_edit(self):
        self.edit_coffee_form = EditCoffeeForm(self)
        self.edit_coffee_form.show()

    def init_record_add(self):
        self.add_coffee_form = AddCoffeeForm(self)
        self.add_coffee_form.show()

    def resizeEvent(self, event):
        for i in range(6):
            self.table.setColumnWidth(i, self.width() // 6)


class AddEditCoffeeForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent_form):
        super(AddEditCoffeeForm, self).__init__()
        self.parent_form = parent_form
        self.data = [None, "", "слабая", "молотый", "", "", ""]
        self.initUi()

    def initUi(self):
        self.setupUi(self)
        self.roasting_input.addItems(['слабая', "средняя", "сильная"])
        self.grain_input.addItems(["молотый", "в зёрнах"])

        self.pushButton.clicked.connect(self.save_data)

    def bind_logic(self):
        self.sort_input.textChanged.connect(self.update_data)
        self.roasting_input.currentIndexChanged.connect(self.update_data)
        self.grain_input.currentIndexChanged.connect(self.update_data)
        self.description_input.textChanged.connect(self.update_data)
        self.price_input.textChanged.connect(self.update_data)
        self.volume_input.textChanged.connect(self.update_data)

    def update_data(self):
        self.data[1] = self.sort_input.text()
        self.data[2] = self.roasting_input.currentText()
        self.data[3] = self.grain_input.currentText()
        self.data[4] = self.description_input.toPlainText()
        self.data[5] = self.price_input.text()
        self.data[6] = self.volume_input.text()

    def approve_record(self):
        if self.data[1] == '':
            return False
        if self.data[4] == '':
            return False
        if not self.data[5].isnumeric():
            return False
        if not self.data[6].isnumeric():
            return False
        reply = QtWidgets.QMessageBox.question(self, "Внимание", "Сохранить введённые данные?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        return reply == QtWidgets.QMessageBox.Yes


class AddCoffeeForm(AddEditCoffeeForm):
    def __init__(self, parent_form):
        super(AddCoffeeForm, self).__init__(parent_form)
        self.bind_logic()

    def save_data(self):
        if self.approve_record():
            connection = sqlite3.connect('data/coffee.sqlite')
            cursor = connection.cursor()
            cursor.execute("""insert into
            coffee(sort, roasting, grains, description, price, volume)
            values (?, ?, ?, ?, ?, ?)""", tuple(self.data[1:]))
            connection.commit()
            connection.close()
            self.parent_form.update_data()
            self.close()


class EditCoffeeForm(AddEditCoffeeForm):
    def initUi(self):
        super(EditCoffeeForm, self).initUi()
        self.fill_data()
        self.bind_logic()

    def get_data(self):
        self.data = list(self.parent_form.data[self.parent_form.table.currentRow()])
        self.data[5] = str(self.data[5])
        self.data[6] = str(self.data[6])

    def fill_data(self):
        self.get_data()

        self.sort_input.setText(self.data[1])
        self.roasting_input.setCurrentIndex(
            ['слабая', "средняя", "сильная"].index(self.data[2]))
        self.grain_input.setCurrentIndex(
            ["молотый", "в зёрнах"].index(self.data[3]))
        self.description_input.setPlainText(self.data[4])
        self.price_input.setText(self.data[5])
        self.volume_input.setText(self.data[6])

    def save_data(self):
        if self.approve_record():
            connection = sqlite3.connect('data/coffee.sqlite')
            cursor = connection.cursor()
            cursor.execute("""update coffee 
                              set sort = ?,
                              roasting = ?,
                              grains = ?,
                              description = ?,
                              price = ?,
                              volume = ?
                            
                              where id = ?""", (*self.data[1:], self.data[0]))
            connection.commit()
            connection.close()
            self.parent_form.update_data()
            self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
