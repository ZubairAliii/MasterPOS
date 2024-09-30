#product page

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from database import *
from PAGES.addproduct import AddProductDialog
from PAGES.updateproduct import UpdateProductDialog

class ProductWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ProductWidget, self).__init__(parent)
        uic.loadUi('UI/ProductWidget.ui', self)
        
        self.loadData()
       
        self.addProductBtn.clicked.connect(self.showAddProductDialog)
        self.updateProductBtn.clicked.connect(self.showUpdateProductDialog)
        self.deleteProductBtn.clicked.connect(self.deleteProduct)

    def setHeaders(self):
        self.productsTable.setColumnCount(7)
        self.productsTable.setHorizontalHeaderLabels([ 'Name', 'Description', 'Category', 'Barcode', 'Purchase Price', 'Selling Price', 'Quantity'])
        #set appropriate column width relative to talbe width
        self.productsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        


    def loadData(self):
        #clear table
        self.productsTable.clearContents()
        self.setHeaders()
        self.productsTable.setRowCount(0)
        self.products = DBgetproducts()
        for product in self.products:
            self.productsTable.insertRow(self.productsTable.rowCount())
            self.productsTable.setItem(self.productsTable.rowCount()-1, 0, QtWidgets.QTableWidgetItem(product.name))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 1, QtWidgets.QTableWidgetItem(product.description))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 2, QtWidgets.QTableWidgetItem(DBgetcategoryname(product.category_id)))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 3, QtWidgets.QTableWidgetItem(product.barcode))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 4, QtWidgets.QTableWidgetItem(str(product.purchase_price)))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 5, QtWidgets.QTableWidgetItem(str(product.selling_price)))
            self.productsTable.setItem(self.productsTable.rowCount()-1, 6, QtWidgets.QTableWidgetItem(str(product.quantity)))

    def showAddProductDialog(self):
        self.addProductDialog = AddProductDialog(self)
        #if product is added
        if self.addProductDialog.exec_():
            self.loadData()

    def showUpdateProductDialog(self):
        #get selected product
        selectedRow = self.productsTable.currentRow()
        product = self.products[selectedRow]
        self.updateProductDialog = UpdateProductDialog(self, product.id)
        if self.updateProductDialog.exec_():
            self.loadData()

    def deleteProduct(self):
        #get selected product
        selectedRow = self.productsTable.currentRow()
        if selectedRow == -1:
            return
        product = self.products[selectedRow]
        if DBdeleteproduct(product.id):
            self.loadData()