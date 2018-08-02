from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout
import sys
from PyQt5.QtWidgets import QMessageBox
import sqlite3
from datetime import datetime
class Add_inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.i=0
        self.j=0
        self.conn = sqlite3.connect('test_10.db')
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        L1=QLabel()
        L2=QLabel()
        L3=QLabel()
        L4=QLabel()


        L1.setText("ITEM  NAME")
        L2.setText("ITEM  PRICE")
        L3.setText("ITEM  QUANTITY")
        L4.setText("PLACE / DETAILS")


        self.item_name=QLineEdit(self)
        self.item_name.setObjectName('item_name')
        self.item_price=QLineEdit(self)
        self.item_price.setObjectName('item_price')
        self.item_quantity=QLineEdit(self)
        self.item_place=QLineEdit(self)

        button_add = QPushButton('ADD INVENTORY', self)
        button_add.clicked.connect(self.create_Database)

        button_del = QPushButton('DELETE ITEM', self)
        button_del.clicked.connect(self.delete_db)

        button_show=QPushButton('SHOW INVENTORY',self)
        button_show.clicked.connect(self.show_db)

        button_update = QPushButton('UPDATE INVENTORY', self)
        button_update.clicked.connect(self.update_db)

        button_sold = QPushButton('ADD TO SOLD ITEMS', self)
        button_sold.clicked.connect(self.sold_db)

        button_solddb = QPushButton('SOLD DATABASE', self)
        button_solddb.clicked.connect(self.show_sold_db)

        button_search = QPushButton('SEARCH INVENTORY', self)
        button_search.clicked.connect(self.search)

        button_exit = QPushButton('Quit', self)
        button_exit.clicked.connect(QApplication.instance().quit)

        grid.addWidget(self.item_name,1,2)
        grid.addWidget(L1,1,1)
        grid.addWidget(self.item_price,2,2)
        grid.addWidget(L2,2,1)
        grid.addWidget(self.item_quantity,3,2)
        grid.addWidget(L3,3,1)
        grid.addWidget(self.item_place,4,2)
        grid.addWidget(L4,4,1)

        grid.addWidget(button_add,5,2)
        grid.addWidget(button_show,6,2)
        grid.addWidget(button_update,7,2)
        grid.addWidget(button_sold,8,2)
        grid.addWidget(button_solddb,9,2)
        grid.addWidget(button_search,10,2)
        grid.addWidget(button_del,11,2)
        grid.addWidget(button_exit,12,2)
        self.show()
        self.setGeometry(300, 100, 700, 600)
        self.setWindowTitle(' HARDWARE ')

    def search(self):
        try:
           cursor=self.conn.execute("SELECT * FROM CUSTOMER WHERE NAME LIKE ? ",
                            ('%'+self.item_name.text()+'%',))

           results = cursor.fetchall()
           table = QTableWidget()
           table.setWindowTitle("INVENTORY DETAILS")
           table.setRowCount(len(results))
           table.setColumnCount(5)
           table.horizontalHeader().setStretchLastSection(True);
           table.setHorizontalHeaderLabels(['DATE', 'ITEM NAME', 'ITEM PRICE', 'QUANTITY', 'PLACE / DETAILS'])
           cursor = self.conn.execute("SELECT * FROM CUSTOMER WHERE NAME LIKE ? ",
                                      ('%' + self.item_name.text() + '%',))

           self.i = 0
           for row in cursor:
               self.j = 0
               table.setItem(self.i, self.j, QTableWidgetItem(str(row[0])))
               self.j += 1
               table.setItem(self.i, self.j, QTableWidgetItem(str(row[1])))
               self.j += 1
               table.setItem(self.i, self.j, QTableWidgetItem(str(row[2])))
               self.j += 1
               table.setItem(self.i, self.j, QTableWidgetItem(str(row[3])))
               self.j += 1
               table.setItem(self.i, self.j, QTableWidgetItem(str(row[4])))

               self.i += 1
           table.show()
           dialog = QDialog()
           dialog.setWindowTitle("INVENTORY DETAILS")
           dialog.resize(1200, 800)
           dialog.setLayout(QVBoxLayout())
           dialog.layout().addWidget(table)

           self.i = 0
           self.j = 0
           dialog.exec()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("HARDWARE")
            msg.setInformativeText("ITEM NOT FOUND !!!")
            msg.exec()

    def show_sold_db(self):

        try:
            cursor = self.conn.execute("SELECT * from SOLD")
            results = cursor.fetchall()
            table = QTableWidget()
            table.setWindowTitle("INVENTORY DETAILS")
            table.setRowCount(len(results))
            table.setColumnCount(5)
            table.horizontalHeader().setStretchLastSection(True);
            table.setHorizontalHeaderLabels(['DATE', 'ITEM NAME', 'ITEM PRICE', 'QUANTITY', 'PLACE / DETAILS'])
            cursor = self.conn.execute("SELECT * from SOLD ORDER BY dt DESC ")
            self.i = 0
            for row in cursor:
                self.j = 0
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[0])))
                self.j += 1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[1])))
                self.j += 1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[2])))
                self.j += 1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[3])))
                self.j += 1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[4])))

                self.i += 1
            table.show()
            dialog = QDialog()
            dialog.setWindowTitle("INVENTORY DETAILS")
            dialog.resize(1200, 800)
            dialog.setLayout(QVBoxLayout())
            dialog.layout().addWidget(table)

            self.i = 0
            self.j = 0
            dialog.exec()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("KAMAL HARDWARE")
            msg.setInformativeText(" DATABASE NOT FOUND!!!")
            msg.exec()

    def sold_db(self):

        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS SOLD
                        ( dt date  , 
                        NAME           TEXT      NOT NULL,
                        PRICE            REAL     NOT NULL,
                        QUANTITY         INT      NOT NULL,
                        PLACE             TEXT    NOT NULL);''')

            self.conn.execute("INSERT INTO SOLD ( dt,NAME, PRICE, QUANTITY,PLACE) \
                          VALUES (?,?,?,?,?)", (datetime.now(),self.item_name.text(), self.item_price.text(), self.item_quantity.text(),self.item_place.text()))

            self.conn.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("HARDWARE")
            msg.setInformativeText("ADDED TO SOLD DATABASE!!!")
            msg.exec()


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("KAMAL HARDWARE")
            msg.setInformativeText(" DATABASE NOT FOUND!!!")
            msg.exec()



    def update_db(self):

        try:
           self.conn.execute("""UPDATE CUSTOMER SET QUANTITY = ? WHERE NAME  = ?;""",
                            (self.item_quantity.text(),self.item_name.text(),))

           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("message box")
           msg.setWindowTitle("HARDWARE")
           msg.setInformativeText("UPDATED !!!")
           msg.exec()


        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("HARDWARE")
            msg.setInformativeText("ITEM NOT FOUND !!!")
            msg.exec()

    def delete_db(self):

        try:
           self.conn.execute("""DELETE FROM CUSTOMER WHERE name= ?;""",
                            (self.item_name.text(),))

           msg = QMessageBox()
           msg.setIcon(QMessageBox.Information)
           msg.setText("message box")
           msg.setWindowTitle("HARDWARE")
           msg.setInformativeText("DELETED!!!")
           msg.exec()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("HARDWARE")
            msg.setInformativeText("ITEM NOT FOUND !!!")
            msg.exec()


    def create_Database(self):
        try:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS CUSTOMER
                        ( dt date, 
                        NAME           TEXT     PRIMARY KEY,
                        PRICE            REAL     NOT NULL,
                        QUANTITY         INT      NOT NULL,
                        PLACE             TEXT    NOT NULL);''')

            self.conn.execute("INSERT INTO CUSTOMER ( dt,NAME, PRICE, QUANTITY,PLACE) \
                          VALUES (?,?,?,?,?)", (datetime.now(),self.item_name.text(), self.item_price.text(), self.item_quantity.text(),self.item_place.text()))

            self.conn.commit()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("HARDWARE")
            msg.setInformativeText("RECORD CREATED!!!")
            msg.exec()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle("KAMAL HARDWARE")
            msg.setInformativeText("ITEM PRESENT IN DATABASE!!!")
            msg.exec()

    def show_db(self):
        try:

            cursor = self.conn.execute("SELECT * from CUSTOMER")
            results = cursor.fetchall()
            table = QTableWidget()
            table.setWindowTitle("INVENTORY DETAILS")
            table.setRowCount(len(results))
            table.setColumnCount(5)
            table.horizontalHeader().setStretchLastSection(True);
            table.setHorizontalHeaderLabels(['DATE', 'ITEM NAME', 'ITEM PRICE', 'QUANTITY','PLACE / DETAILS'])
            cursor = self.conn.execute("SELECT * from CUSTOMER ORDER BY dt DESC ")

            for row in cursor:

                self.j=0
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[0])))
                self.j+=1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[1])))
                self.j+=1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[2])))
                self.j+=1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[3])))
                self.j+=1
                table.setItem(self.i, self.j, QTableWidgetItem(str(row[4])))

                self.i+=1
            table.show()
            dialog = QDialog()
            dialog.setWindowTitle("INVENTORY DETAILS")
            dialog.resize(1200, 800)
            dialog.setLayout(QVBoxLayout())
            dialog.layout().addWidget(table)

            self.i=0
            self.j=0
            dialog.exec()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("message box")
            msg.setWindowTitle(" HARDWARE")
            msg.setInformativeText("DATABASE NOT FOUND!!!")
            msg.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Add_inventory()
    sys.exit(app.exec_())
    self.conn.close()
