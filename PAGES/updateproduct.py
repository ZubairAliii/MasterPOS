#Add Product Page

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import uic
from database import *

class UpdateProductDialog(QtWidgets.QDialog):

    def __init__(self, parent=None,product_id=None):
        self.product_id = product_id
        super(UpdateProductDialog, self).__init__(parent)
        uic.loadUi('UI/AddProductDialog.ui', self)
        self.addProductBtn.clicked.connect(self.updateProduct)
        self.addProductBtn.setText("Update")
        self.loadCategories()
        self.loadProduct()
    
    def loadProduct(self):
        #DBgetproduct
        product = DBgetproduct(id=self.product_id)
        self.productName.setText(product.name)
        self.productDescription.setPlainText(product.description)
        self.productBarcode.setText(product.barcode)
        self.productPurchasePrice.setValue(product.purchase_price)
        self.productSellingPrice.setValue(product.selling_price)
        self.productQuantity.setValue(product.quantity)
        self.productCategory.setCurrentText(DBgetcategoryname(product.category_id))

    def loadCategories(self):
        categories = DBgetcategories()
        for category in categories:
            self.productCategory.addItem(category.name)


    def updateProduct(self):
        name = self.productName.text()
        description = self.productDescription.toPlainText()
        barcode = self.productBarcode.text()
        purchase_price = self.productPurchasePrice.text()
        selling_price = self.productSellingPrice.text()
        quantity = self.productQuantity.text()
        category = DBgetcategoryid(self.productCategory.currentText())
        if DBupdateproduct(self.product_id, name, description, barcode, purchase_price, selling_price, quantity, category):
            self.accept()
        