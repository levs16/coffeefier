import sys
import sqlite3
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.listWidget.itemSelectionChanged.connect(self.show_info)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.cursor = self.connection.cursor()
        self.fill_list()

    def fill_list(self):
        query = "SELECT * FROM coffeeInfo"
        result = self.cursor.execute(query).fetchall()
        self.listWidget.clear()
        for name in result:
            self.listWidget.addItem(name[1])

    def show_info(self):
        name = self.listWidget.currentItem().text()
        query = "SELECT * FROM coffeeInfo WHERE sortName = ?"
        result = self.cursor.execute(query, (name,)).fetchone()
        if result:
            id, name, roast, ground, taste, price, volume = result
            info = f"Sort: {name}\nRoast level: {roast}\nGround/beans: {ground}\nTaste Description: {taste}\nPrice: ${price}.\nPackage volume: {volume}."
            self.textEdit.setText(info)
        else:
            self.textEdit.clear()

    def closeEvent(self, event):
        self.connection.close()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
