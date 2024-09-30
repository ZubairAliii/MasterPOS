from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QWidget
from PyQt5 import uic
from database import *
from PyQt5.QtCore import pyqtSignal
from .receipt import generate_receipt
from datetime import datetime 



class PosWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PosWidget, self).__init__(parent)
        uic.loadUi('UI/POSWidget.ui', self)

        self.selectedCategory = None
        self.loadCategories()
        self.loadProducts(self.selectedCategory.id)

        self.checked = False
        
        # Dictionary to keep track of added products (product_id -> ListViewWidget)
        self.cartsProductWidgets = [{}]
        self.cartsProducts=[{}]
        # Total price label (assumed already exists in the UI file)
        self.totalPriceLabel = self.findChild(QtWidgets.QLabel, "totalprice")

        # Variable to keep track of the total price
        self.totalPrice = 0.0

        # self.checkoutButton = self.findChild(QtWidgets.QPushButton, "checkout")
        # self.printcheckout.clicked.connect(self.printrecipt)
        #Print Receipt Button
        self.checkout.clicked.connect(self.openCheckOutDialog)

        self.clear.clicked.connect(self.clearCart)
        self.saleTabWidget.currentChanged.connect(self.onchangeSale)
        self.lastPage = 0
        self.updateTotalPrice()
        
    def onchangeSale(self):
        if self.saleTabWidget.currentIndex() > self.lastPage:
            #add tab to tab widget
            print(self.lastPage)
            tab = QtWidgets.QWidget()
            tab.setLayout(QVBoxLayout())
            scroll = QtWidgets.QScrollArea()
            scollarea  = QtWidgets.QWidget()

            scollarea.setLayout(QVBoxLayout())
            scroll.setWidgetResizable(True)
            scroll.setWidget(scollarea)
            frame = QtWidgets.QFrame()
            #set frame name
            frame.setObjectName("tab"+str(self.lastPage+2))
            frame.setLayout(QVBoxLayout())
            scollarea.layout().addWidget(frame)
            spacer  = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            scollarea.layout().addItem(spacer)

            tab.layout().addWidget(scroll)

            self.saleTabWidget.addTab(tab,"+")
            print(self.lastPage)
            #change the name of second last tab
            self.saleTabWidget.setTabText(self.lastPage+1,"Sale "+str(self.lastPage+2))
            print(self.lastPage)
            self.cartsProductWidgets.append({})
            self.cartsProducts.append({})
            

            self.lastPage += 1
        self.updateTotalPrice()

    def loadProducts(self, category_id):
        # Clear the product grid before loading new products
        
        for i in reversed(range(self.productsGrid.layout().count())):
            self.productsGrid.layout().itemAt(i).widget().setParent(None)
        
        products = DBgetproductsbycategory(category_id)
        
        # Load products in the grid, with a max of 5 columns
        for i in range(0, len(products), 5):
            for j in range(5):
                if i + j < len(products):
                    product_widget = ProductWidget(products[i+j])
                    product_widget.onClick.connect(self.addItemToScrollArea)
                    self.productsGrid.layout().addWidget(product_widget, i // 5, j)

    def loadCategories(self):
        categories = DBgetcategories()
        self.selectedCategory = categories[0]
        self.categoriesWidgets = []
        
        # Load categories into the grid, with a max of 4 columns
        for i in range(0, len(categories), 4):
            for j in range(4):
                if i + j < len(categories):
                    cat = CategoryWidget(categories[i + j])
                    cat.onSelect.connect(self.loadProducts)
                    cat.onSelect.connect(self.refreshCategories)
                    self.categoriesWidgets.append(cat)
                    if i == 0 and j == 0:
                        cat.setState(True)

                    self.categoriesGrid.layout().addWidget(cat, i // 4, j)

    def refreshCategories(self, selectedCategory_id):
        for cat in self.categoriesWidgets:
            if cat.category.id == selectedCategory_id:
                cat.setState(True)
            else:
                cat.setState(False)

    # Add ListViewWidget to the scroll area dynamically or update the quantity if already in the list
    def addItemToScrollArea(self, product):
        #get current tab of cart
        tab = self.saleTabWidget.currentWidget()
        #find a frame that name starts with "tab"
        currentScrollArea = tab.findChild(QtWidgets.QFrame)
        currentFrame = currentScrollArea.findChild(QtWidgets.QFrame)

        index=  self.saleTabWidget.currentIndex()
        
        print(currentFrame)
        


        if product.id in self.cartsProductWidgets[index]:
            # If the product is already in the list, increase the quantity
            listViewWidget =  self.cartsProductWidgets[index][product.id]
            listViewWidget.increaseQuantity()
        else:
            # If the product is not in the list, create a new ListViewWidget and add it
            listViewWidget = ListViewWidget(product)
            listViewWidget.onQuantityChanged.connect(self.updateTotalPrice)  # Connect signal to update total price
            listViewWidget.onQuantityChanged.connect(self.updateQuantity)
            listViewWidget.onItemRemoved.connect(self.removeItemFromScrollArea)  # Connect signal to remove item from scroll area
            currentFrame.layout().addWidget(listViewWidget)
            self.cartsProductWidgets[index][product.id] = listViewWidget  # Keep track of added products
            self.cartsProducts[index][product.id] = [product,1]

        # Scroll to the bottom after adding or updating items
        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

        # Update the total price after adding or updating items
        self.updateTotalPrice()
    def updateQuantity(self,quantity,product_id):
        index = self.saleTabWidget.currentIndex()
        # Update the quantity of the product in the cart
        self.cartsProducts[index][product_id][1] = quantity

    def updateTotalPrice(self):
        index = self.saleTabWidget.currentIndex()
        print(index)
        # Recalculate the total price based on all items in the cart
        self.totalPrice = sum(widget.product.selling_price * widget.quantity.value() for widget in self.cartsProductWidgets[index].values())
        # Update the total price label
        self.totalPriceLabel.setText("{:.2f}".format(self.totalPrice))

    def removeItemFromScrollArea(self, product_id):
        index = self.saleTabWidget.currentIndex()
        # Remove the item from the scroll area
        self.billProductList.layout().removeWidget(self.cartsProductWidgets[index][product_id])

        # Remove the item from the dictionary
        self.cartsProductWidgets[index].pop(product_id)
        self.cartsProducts[index].pop(product_id)
        self.updateTotalPrice()


    # def printrecipt(self):
    #     # Generate a receipt slip with product details and total price
      

    #     for widget in self.cartProductWidgets.values():
    #         total_price = 0
    #         product_name = widget.product.name
    #         quantity = widget.quantity.value()
    #         unit_price = widget.product.selling_price
    #         item_total = quantity * unit_price
    #         total_price += item_total
    #         self.list_of_product[product_name] = [unit_price,quantity,total_price]
    #         self.checked = True

    #     # Show receipt in a message box (or save to file)
    #     generate_receipt(self.list_of_product)


    def openCheckOutDialog(self):
       #Open CheckOutDialog window
       self.checkoutDialog = checkoutDialog(self,self.totalPrice)
       self.checkoutDialog.onSaveBtn.connect(self.SaveSale)
       self.checkoutDialog.onPrintBtn.connect(self.printandcheckout)
       self.checkoutDialog.exec_()

    def clearCart(self):
        #clear scroll area
        # for i in reversed(range(self.billProductList.layout().count())):
        #     # self.billProductList.layout().itemAt(i).widget().setParent(None)
        #     self.billProductList.layout().removeWidget(self.billProductList.layout().itemAt(i).widget())
        index =  self.saleTabWidget.currentIndex()
        for widget in self.cartsProductWidgets[index].values():
            widget.setParent(None)
        self.cartsProductWidgets[index] = {}
        #self.
        #self.totalPrice = 0
        self.updateTotalPrice()
        #number of tabs
        if self.saleTabWidget.count() > 2:
            self.saleTabWidget.removeTab(self.saleTabWidget.currentIndex())
            self.saleTabWidget.setCurrentIndex(self.saleTabWidget.count()-2)
            self.lastPage -=1
            self.refreshTabNames()
    def refreshTabNames(self):
        for i in range(self.saleTabWidget.count()-1):
            self.saleTabWidget.setTabText(i, f"Page {i+1}")


    def SaveSale(self,customer_name,customer_number,clear=True):
        index =  self.saleTabWidget.currentIndex()
        barcode = int(datetime.now().timestamp())
        DBaddsale(date=datetime.now(), total=self.totalPrice, barcode=int(datetime.now().timestamp()), customer_name=customer_name, customer_number=customer_number, user_id=1, products=self.cartsProducts[index])
        if clear:
            self.clearCart()
        return barcode
    def printandcheckout(self,customer_name,customer_number):
        index =  self.saleTabWidget.currentIndex()
        barcode = self.SaveSale(customer_name,customer_number,False)
        generate_receipt(self.cartsProducts[index],customer_name,customer_number,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),barcode)
        self.clearCart()

class checkoutDialog(QtWidgets.QDialog):
    onSaveBtn = pyqtSignal(str,str)
    onPrintBtn = pyqtSignal(str,str)

    def __init__(self, parent=None,total_price=0):
        super(checkoutDialog, self).__init__(parent)
        uic.loadUi('UI/CheckOutDialog.ui', self)
        self.total_price = total_price
        self.totalamount.setText("{:.2f}".format(self.total_price))
        
        self.cashrecieved.textChanged.connect(self.calculateChange)

        self.checkout.clicked.connect(self.checkOut)
        self.printandcheckoutbtn.clicked.connect(self.printandcheckout)
        # self.returnamount.setText("{:.2f}".format(self.total_price))

    def checkOut(self):
     
        self.onSaveBtn.emit(self.customername.text(),self.customernumber.text())
        self.close()

    def printandcheckout(self):
        self.onPrintBtn.emit(self.customername.text(),self.customernumber.text())
        self.close()

    def calculateChange(self):
        if self.cashrecieved.text() == "":
            self.returnamount.setText("0.00")
        else:
            cashrecieved = float(self.cashrecieved.text())
            returnamount = cashrecieved - self.total_price
            self.returnamount.setText("{:.2f}".format(returnamount))



 

class ProductWidget(QtWidgets.QWidget):
    onClick = pyqtSignal(object)  # Custom signal to emit the product when clicked

    def __init__(self, product, parent=None):
        super(ProductWidget, self).__init__(parent)
        uic.loadUi('UI/POSProductWidget.ui', self)
        self.product = product

        # Name and price
        self.productName.setText(product.name)
        self.productPrice.setText("{}".format(product.selling_price))

        # Set background color and border radius
        self.productFrame.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 10px;")

        # Height constraint
        self.productFrame.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # Width constraint
        self.productFrame.setFixedWidth(100)

        # Connect the click event
        self.productFrame.mousePressEvent = self.emitProduct

    def emitProduct(self, event):
        # Emit the signal with the product data when clicked
        self.onClick.emit(self.product)


class CategoryWidget(QtWidgets.QWidget):
    onSelect = pyqtSignal(int)

    def __init__(self, category, parent=None):
        super(CategoryWidget, self).__init__(parent)
        # State colors: blue for active, white for inactive
        self.ACTIVE = "background-color: rgb(69, 145, 237); color: rgb(255, 255, 255); border: 1px solid rgb(0, 0, 0); border-radius: 10px;"
        self.INACTIVE = "background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 1px solid rgb(0, 0, 0); border-radius: 10px;"

        self.category = category
        self.categoryName = QtWidgets.QLabel(self)

        # Set label properties
        self.categoryName.setFrameShape(QtWidgets.QFrame.Box)
        self.categoryName.setLineWidth(1)
        self.categoryName.setAlignment(QtCore.Qt.AlignCenter)
        self.categoryName.setContentsMargins(5, 8, 5, 8)
        self.categoryName.setText(category.name)

        # Connect the click event
        self.categoryName.mousePressEvent = self.selectCategory

        # Set layout
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(self.categoryName)
        self.setState(False)

    def setState(self, state):
        if state:
            self.categoryName.setStyleSheet(self.ACTIVE)
        else:
            self.categoryName.setStyleSheet(self.INACTIVE)

    def selectCategory(self, event):
        self.onSelect.emit(self.category.id)


class ListViewWidget(QtWidgets.QWidget):
    onQuantityChanged = pyqtSignal(int,int)  # Signal emitted when quantity is changed
    onItemRemoved = pyqtSignal(int)

    def __init__(self, product, parent=None):
        super(ListViewWidget, self).__init__(parent)
        uic.loadUi('UI/ListViewProductWidget.ui', self)
        
        # Set product name and price
        self.product = product
        self.ProductName.setText(product.name)
        self.ProductPrice.setText(str(product.selling_price))
        self.ProductSubTotal.setText(str(product.selling_price))
        self.quantity.setValue(1)  # Default quantity is 1

        # Update price according to quantity
        self.quantity.valueChanged.connect(self.updatePrice)
        self.crossbtn.clicked.connect(self.removeItem)


    def updatePrice(self):
        # Set product price based on quantity
        total_price = self.product.selling_price * self.quantity.value()
        self.ProductSubTotal.setText("{:.2f}".format(total_price))

        # Emit the signal to notify about the quantity change
        self.onQuantityChanged.emit(self.quantity.value(),self.product.id)

    def increaseQuantity(self):
        # Increase the quantity by 1
        current_quantity = self.quantity.value()
        self.quantity.setValue(current_quantity + 1)


    def removeItem(self):
        # Remove the item from the list
        self.onItemRemoved.emit(self.product.id)
