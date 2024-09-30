#Add Sale Report

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from database import *


class SalereportWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SalereportWidget, self).__init__(parent)
        uic.loadUi('UI/SaleWidget.ui', self)


        self.dailydateedit.setDate(QtCore.QDate.currentDate())

        self.loadData()
        #self.dailydateedit.dateChanged.connect(self.dailydateeditchanged)

    def setHeaders(self):
        self.saledatatable.setColumnCount(5)
        self.saledatatable.setHorizontalHeaderLabels([ 'Barcode','Date/Time', 'Cutomer Name', 'Customer Number', 'Total'])
        #set appropriate column width relative to talbe width
        self.saledatatable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.saledatatable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.saledatatable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.saledatatable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.saledatatable.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)


    def loadData(self):
        #clear table
        self.saledatatable.clearContents()
        self.setHeaders()
        self.saledatatable.setRowCount(0)
        self.sales = DBgetsale()
        for sale in self.sales:
            self.saledatatable.insertRow(self.saledatatable.rowCount())

            self.saledatatable.setItem(self.saledatatable.rowCount()-1, 0, QtWidgets.QTableWidgetItem(sale.barcode))
            self.saledatatable.setItem(self.saledatatable.rowCount()-1, 1, QtWidgets.QTableWidgetItem(sale.date.strftime("%d-%m-%Y %H:%M:%S")))
            self.saledatatable.setItem(self.saledatatable.rowCount()-1, 2, QtWidgets.QTableWidgetItem(sale.customer_name))
            self.saledatatable.setItem(self.saledatatable.rowCount()-1, 3, QtWidgets.QTableWidgetItem(sale.customer_number))
            self.saledatatable.setItem(self.saledatatable.rowCount()-1, 4, QtWidgets.QTableWidgetItem(str(sale.total)))

        #item double click
        self.saledatatable.itemDoubleClicked.connect(self.openSaleDetailDialog)
        #row double click

    #Double click item open ViewSaleDialog
    def openSaleDetailDialog(self,id):

        sale_barcode = self.saledatatable.item(self.saledatatable.currentRow(),0).text()

        self.checkoutDialog = ViewSaleDialog(self,sale_barcode)
        self.checkoutDialog.exec_()


        


class ViewSaleDialog(QtWidgets.QDialog):
    def __init__(self, parent=None,sale_barcode=None):
        super(ViewSaleDialog, self).__init__(parent)
        uic.loadUi('UI/ViewSaleDialog.ui', self)

        self.sale,self.saleitems = DBgetsalebybarcode(barcode=sale_barcode)


        self.saleid.setText(str(self.sale.barcode))
        self.customername.setText(self.sale.customer_name)
        self.customernumber.setText(self.sale.customer_number)
        self.date.setText(self.sale.date.strftime("%d-%m-%Y %H:%M:%S"))


        self.totalamount.setText(str(self.sale.total))

        self.loadData()


    def setHeaders(self):
        self.saleitemtable.setColumnCount(4)
        self.saleitemtable.setHorizontalHeaderLabels([ 'Product Name', 'Quantity', 'Price', 'Sub Total'])
        #set appropriate column width relative to talbe width
        self.saleitemtable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.saleitemtable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.saleitemtable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.saleitemtable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)



    def loadData(self):
        #clear table
        self.saleitemtable.clearContents()
        self.setHeaders()
        self.saleitemtable.setRowCount(0)

        for item in self.saleitems:
            self.saleitemtable.insertRow(self.saleitemtable.rowCount())
            self.saleitemtable.setItem(self.saleitemtable.rowCount()-1, 0, QtWidgets.QTableWidgetItem(DBgetproductname(item.product_id)))
            self.saleitemtable.setItem(self.saleitemtable.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(item.quantity)))
            self.saleitemtable.setItem(self.saleitemtable.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(item.price)))
            self.saleitemtable.setItem(self.saleitemtable.rowCount()-1, 3, QtWidgets.QTableWidgetItem(str(item.quantity*item.price)))



   

    