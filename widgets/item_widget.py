
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from gen.ItemWidget import Ui_ItemWidget


class ItemWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        self.ui = Ui_ItemWidget()
        self.ui.setupUi(self)
        self.item = item
        self.fill_item()

    def fill_item(self):
        self.ui.label_title.setText(self.item["title"])
        self.ui.label_price.setText(str(self.item["price"]))
        self.ui.label_discount.setText(str(self.item["discount"]))
        self.ui.label_category.setText(self.item["category"])
        self.ui.label_brand.setText(self.item["brand"])


        if self.item["image"]:
            path = "image\\" + self.item["image"]
            pix = QPixmap(path)
        else:
            path = "../image/img.png"
            pix = QPixmap(path)
        self.ui.label_image.setPixmap(pix)

    def mousePressEvent(self, a0):
        main = self.window()
        main.select_widget(self)
