from PyQt6.QtWidgets import QWidget, QLayout, QMessageBox

from db import dao
from gen.main_window import Ui_MainForm
from widgets.ProductDialog import ProductDialog
from widgets.item_widget import ItemWidget


def clear_layout(layout: QLayout):
    while layout.count():
        w = layout.takeAt(0).widget()
        if w:
            w.deleteLater()


class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)

        self.auth = None
        self.user = user

        self.fill_name()
        self.visibles()
        self.selected_widget = None
        self.add_widgets()
        self.conn()
        self.fill_combobox_sort()
        self.fill_combobox_categories()

    def conn(self):
        self.ui.pushButton_add.clicked.connect(self.add_new_product)
        self.ui.pushButton_edit.clicked.connect(self.edit_product)
        self.ui.pushButton_del.clicked.connect(self.delete_product)

        self.ui.pushButton_logout.clicked.connect(self.logout)

        self.ui.lineEdit_search.textChanged.connect(self.add_widgets)
        self.ui.comboBox_postav.currentIndexChanged.connect(self.add_widgets)
        self.ui.comboBox_sort.currentIndexChanged.connect(self.add_widgets)

    def delete_product(self):
        if self.selected_widget:
            dao.delete_product(self.selected_widget.item["id"])
            self.add_widgets()
            print("продукт удален")
        else:
            QMessageBox.warning(self,"выбери товар","выбери товар")

    def add_new_product(self):
        ProductDialog().exec()
        self.add_widgets()

    def edit_product(self):
        if self.selected_widget:
            item = self.selected_widget.item
            ProductDialog(item).exec()
            self.add_widgets()

        else:
            QMessageBox.warning(self,"выбери товар","выбери товар")


    def fill_combobox_sort(self):
        self.ui.comboBox_sort.addItem("Без сортировки")
        self.ui.comboBox_sort.addItem("По возрастанию цены")
        self.ui.comboBox_sort.addItem("По убыванию цены")

    def fill_combobox_categories(self):
        items = dao.get_all_categories()
        self.ui.comboBox_postav.addItem("Все")
        for item in items:
            self.ui.comboBox_postav.addItem(item["title"])

    def add_widgets(self):
        clear_layout(self.ui.verticalLayout_4)
        self.selected_widget = None

        category = self.ui.comboBox_postav.currentText()
        search = self.ui.lineEdit_search.text()
        sort = self.ui.comboBox_sort.currentText()

        items = dao.get_all_items(category,search,sort)
        for item in items:
            # print("item ===== ", item, "\n")
            self.ui.verticalLayout_4.addWidget(ItemWidget(item))

    def select_widget(self, widget):
        if self.selected_widget:
            self.selected_widget.setStyleSheet("")

        self.selected_widget = widget
        self.selected_widget.setStyleSheet("background: #8effb2;")

    def fill_name(self):
        self.ui.label_fio.setText(self.user["username"])

    def logout(self):
        from widgets.auth import AuthWindow
        self.auth = AuthWindow()
        self.auth.show()
        self.close()

    def visibles(self):
        user_role = self.user["role_id"]
        if user_role == 4:
            self.ui.tabWidget.setTabVisible(1,False)
            self.ui.pushButton_add.setVisible(False)
            self.ui.pushButton_del.setVisible(False)
            self.ui.pushButton_edit.setVisible(False)

            self.ui.lineEdit_search.setVisible(False)
            self.ui.comboBox_postav.setVisible(False)
            self.ui.comboBox_sort.setVisible(False)


