from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm

from reportlab.graphics.barcode import code93
from math import ceil
import csv



# draw the barcode
def drawBarcode( x, y, value, c):
	barcode_offset_x = 0*mm
	barcode_offset_y = 0*mm

	barcode=code93.Standard93(value, barHeight = 4*mm)
	barcode.drawOn(c, x+barcode_offset_x, y+barcode_offset_y)

	number_offset_x = 16*mm
	number_offset_y = -5*mm

	name_offset_x = 16*mm
	name_offset_y = -2*mm

	price_offset_x = 5*mm
	price_offset_y = -5*mm


	for item in inventory:
		if item["id"] == value:
			name = item["name"][:20]
			price = "$" + item["price_retail"] + "0"

	c.setFont("Times-Roman", 6)
	c.drawCentredString(x+name_offset_x, y+name_offset_y, name)
	c.setFont("Times-Roman", 8)
	c.drawString(x+number_offset_x, y+number_offset_y, "#" + value)
	c.drawString(x+price_offset_x, y+price_offset_y, price)

# generate list of item id's from po
def getItems():
	barcodes = []

	for item in po:
		for item2 in inventory:
			for x in range(int(item["ORDER QTY."])):
				if item2["name"] == item["ITEM"]:
					barcodes.append(item2["id"])

	return barcodes

# a poorly made function using global variables to layout the barcodes on the page
def layout_sheet():
	global sheet_index
	for label_y in range(sheet_y):
		for label_x in range(sheet_x):
			sheet_index = sheet_index + 1
			if sheet_index < len(labels):
				test_x = base_x+(label_x*label_offset_x)
				test_y = base_y+(label_y*label_offset_y)
				drawBarcode(test_x, test_y, labels[sheet_index], c)

inventory = list(csv.DictReader(open("inventory.csv")))
po = list(csv.DictReader(open("po.csv")))

# these values work for Avery Return Address Label Sheets
# base values determine starting position in upper left hand corner of a page
base_x = 12*mm
base_y = 265*mm

# sheet values detemine how many labels the sheet has on each side
sheet_x = 4
sheet_y = 20

# label offsets determine distance between individual labels
label_offset_x = 52*mm
label_offset_y = -13.25*mm

c = canvas.Canvas("barcodes.pdf", pagesize=letter)

labels = getItems()
pages =  int(ceil(len(labels) / float(sheet_x * sheet_y)))

sheet_index = 0

for x in range(pages):
	layout_sheet()
	c.showPage()

c.save()
