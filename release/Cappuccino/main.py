import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Other_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Cappuccino/addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('Cappuccino/coffee.sqlite')
        self.pushButton.clicked.connect(self.change)
        self.pushButton_2.clicked.connect(self.delete)

    def change(self):
        cur = self.con.cursor()
        res = cur.execute(""" SELECT * FROM coffee """).fetchall()
        for i in range(len(res)):
            if res[i][0] == int(self.lineEdit_2.text()):
                cur.execute(""" DELETE FROM coffee WHERE ID = ? """, (res[i][0],)).fetchall()
                cur.execute(""" INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?) """, (self.lineEdit_2.text(),
                self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(),
                self.lineEdit_6.text(), self.lineEdit_7.text(), self.lineEdit_8.text())).fetchall()
        self.con.commit()

    def delete(self):
        cur = self.con.cursor()
        res = cur.execute(""" SELECT * FROM coffee """).fetchall()
        for i in range(len(res)):
            if res[i][0] == int(self.lineEdit.text()):
                cur.execute(""" DELETE FROM coffee WHERE ID = ? """, (res[i][0],)).fetchall()
                break
        self.con.commit()


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Cappuccino/main.ui', self)
        self.con = sqlite3.connect('Cappuccino/coffee.sqlite')
        self.pushButton.clicked.connect(self.show_all)
        self.pushButton_2.clicked.connect(self.change_del)
    
    def show_all(self):
        cur = self.con.cursor()
        res = cur.execute(""" SELECT * FROM coffee """).fetchall()
        if not len(res):
            return
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название_сорта', 'Степень_обжарки',
                                                    'Молотый_или_в_зернах', 'Описание_вкуса',
                                                    'Цена', 'Объем_упаковки'])
        for i in range(len(res)):
            for j in range(7):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(res[i][j])))

    def change_del(self):
        self.copy = Other_window()
        self.copy.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.exit(app.exec())