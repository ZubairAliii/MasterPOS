# POS of recipt using REPORTLAB


#2.2 inch thermal printer
from reportlab.pdfgen import canvas
#PAGE OF 2.2 inch width and max height
from reportlab.lib.units import inch
import math
# import barcode from reportlab
import barcode
from barcode.writer import ImageWriter

from reportlab.graphics.barcode.common import *
from reportlab.graphics.barcode.code39 import *
from reportlab.graphics.barcode.code93 import *
from reportlab.graphics.barcode.code128 import *
from reportlab.graphics.barcode.usps import *
from reportlab.graphics.barcode.usps4s import USPS_4State
from reportlab.lib.units import mm, inch, cm, pica

from reportlab.graphics.barcode import getCodes, getCodeNames, createBarcodeDrawing, createBarcodeImageInMemory
from reportlab.pdfgen import canvas


def generate_barcode(data, barcode_format, options=None):
    # Get the barcode class corresponding to the specified format     
    barcode_class = barcode.get_barcode_class(barcode_format)
    # Create a barcode image using the provided data and format
    barcode_image = barcode_class(data, writer=ImageWriter())
    # Save the barcode image to a file named "barcode" with the specified options
    barcode_image.save("barcode", options=options)

def generate_receipt(products, customer_name, customer_number,date,barcode, filename="pos.pdf"):
    WIDTH = 2.2 * inch
    CENTER = WIDTH / 2

    c = canvas.Canvas(filename, pagesize=(WIDTH, 10 * inch))
    Y = 10 * inch

    # Header
    c.setFont("Helvetica-Bold", 12)
    Y -= 0.5 * inch
    c.drawCentredString(CENTER, Y, "SHOP NAME")
    c.setFont("Helvetica-Bold", 10)
    Y -= 0.2 * inch
    c.drawCentredString(CENTER, Y, "ADDRESS")
    c.setFont("Helvetica-Bold", 8)
    Y -= 0.2 * inch
    c.drawCentredString(CENTER, Y, "CONTACT")
    c.setFont("Helvetica", 6)
    Y -= 0.2 * inch
    c.drawCentredString(CENTER, Y, "DATE")

    # Customer Details
    LEFT_PADDING = 0.09 * inch
    Y -= 0.4 * inch
    c.drawString(LEFT_PADDING, Y, "Customer Name: "+customer_name)
    Y -= 0.1 * inch
    c.drawString(LEFT_PADDING, Y, "Customer Number: "+customer_number)

    # Draw Line
    Y -= 0.05 * inch
    c.line(0, Y, 2.3 * inch, Y)

    # Draw Product Table Header
    COLUMN_WIDTH = (WIDTH - 2 * LEFT_PADDING) / 5
    Y -= 0.1 * inch
    c.setFont("Helvetica-Bold", 6)
    c.drawString(LEFT_PADDING, Y, "NAME")
    c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3, Y, "PRICE")
    c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3.9, Y, "QTY")
    c.drawString(LEFT_PADDING + COLUMN_WIDTH * 4.5, Y, "TOTAL")

    # Draw Line
    Y -= 0.05 * inch
    c.line(0, Y, 2.3 * inch, Y)

    # Add Products to the Receipt
    c.setFont("Helvetica", 7)
    total = 0
    qnty = 0
    for product_id in products:
        product = products[product_id][0]
        #unit_price, quantity, item_total = details
        product_name = product.name
        unit_price = product.selling_price
        quantity = products[product_id][1]
        item_total = unit_price * quantity
        Y -= 0.1 * inch
        c.drawString(LEFT_PADDING, Y, product_name)
        c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3, Y, f"{unit_price:.1f}")
        c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3.9, Y, str(quantity))
        c.drawString(LEFT_PADDING + COLUMN_WIDTH * 4.5, Y, f"{item_total:.1f}")
        total += item_total
        qnty+=quantity
        # Draw dotted line
        Y -= 0.02 * inch
        c.setDash(1, 1)
        c.line(0, Y, 2.3 * inch, Y)


    # TOTAL
    c.setFont("Helvetica-Bold", 6)
    Y -= 0.1 * inch
    c.drawString(LEFT_PADDING, Y, "ITEMS:")
    c.setFont("Helvetica", 6)
    c.drawString(LEFT_PADDING * 5, Y, str(len(products)))

    c.setFont("Helvetica-Bold", 6)
    Y -= 0.1 * inch
    c.drawString(LEFT_PADDING, Y, "Quantity:")
    c.setFont("Helvetica", 6)
    c.drawString(LEFT_PADDING * 6, Y, str(qnty))


    c.setFont("Helvetica-Bold", 6)
    c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3, Y, "TOTAL:")
    c.setFont("Helvetica", 6)
    c.drawString(LEFT_PADDING + COLUMN_WIDTH * 3.9, Y, f"{total:.1f}")
    
    # c.setStrokeColor("#000000")
    # #Draw Barcode using reportlab
    # c.setFont("Helvetica", 6)
    # print(LEFT_PADDING, Y - 0.1 * inch)
    # barcode = Code128(str("3434234"),
    #                       barHeight=0.5 * inch,
    #                       barWidth=WIDTH - 2 * LEFT_PADDING,
    #                       humanReadable=True)
    # barcode.drawOn(c, LEFT_PADDING, Y - 0.1 * inch)
    generate_barcode(str(barcode), "code128", options={"foreground":"black", 
                                                 "write_text":False,
                                                  "module_width":0.4, 
                                                  "module_height":1,})

    #add image to pdf
    c.drawImage("barcode.png", LEFT_PADDING, Y - 0.6 * inch, WIDTH - 2 * LEFT_PADDING, 0.5 * inch)
    # Draw Line
    c.save()