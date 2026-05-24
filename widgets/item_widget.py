
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
        self.ui.label_title.setText(f'Название: {self.item["title"]}')
        self.ui.label_discount.setText(f'Скидка: {self.item["discount"]} %')
        self.ui.label_category.setText(f'Категория: {self.item["category"]}')
        self.ui.label_brand.setText(f'Бренд: {self.item["brand"]}')
        self.ui.label_description.setText(f'Описание: {self.item["description"]}')
        if self.item["discount"] >= 15:
            price = self.item["price"]
            old_price = price / (1 - self.item["discount"] / 100)
            self.ui.label_price.setText(
                f'Старая цена: <s>{round(old_price,2)} рублей </s> <br>'
                f'<font color="red">Новая цена {price} </font>'
            )
        else:
            self.ui.label_price.setText(f'Цена: {self.item["price"]} рублей')

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
