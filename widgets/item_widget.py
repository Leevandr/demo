
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
        self.ui.label_price.setText(f'{self.item["price"]} рублей')
        self.ui.label_discount.setText(f'{self.item["discount"]} % скидки')
        self.ui.label_category.setText(self.item["category"])
        self.ui.label_brand.setText(self.item["brand"])
        self.ui.label_description.setText(self.item["description"])


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
