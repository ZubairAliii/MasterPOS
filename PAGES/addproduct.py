#Add Product Page

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from database import *

class AddProductDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(AddProductDialog, self).__init__(parent)
        uic.loadUi('UI/AddProductDialog.ui', self)
        self.addProductBtn.clicked.connect(self.addProduct)
        self.loadCategories()
    
    def loadCategories(self):
        categories = DBgetcategories()
        for category in categories:
            self.productCategory.addItem(category.name)


    def addProduct(self):
        name = self.productName.text()
        description = self.productDescription.toPlainText()
        barcode = self.productBarcode.text()
        purchase_price = self.productPurchasePrice.text()
        selling_price = self.productSellingPrice.text()
        quantity = self.productQuantity.text()
        category = DBgetcategoryid(self.productCategory.currentText())
        if DBaddproduct(name, description, barcode, purchase_price, selling_price, quantity, category):
            self.accept()
        