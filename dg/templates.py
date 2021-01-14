from PyQt5 import uic  # noqa
from PyQt5.QtCore import (
    pyqtSignal,
    QSize
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QListWidget,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QListWidgetItem
)

from dg import (
    UI_DIR,
    TEMPLATES_DIR,
    ICONS_DIR
)


class TemplatesWindow(QDialog):
    """
    Templates Window
    """
    on_save = pyqtSignal(str)
    list_widget: QListWidget
    button_box: QDialogButtonBox

    def __init__(self, parent):
        """Initialise"""
        super().__init__(parent=parent)
        ui_path = UI_DIR / 'templates.ui'
        uic.loadUi(str(ui_path), self)
        self.setStyleSheet("""
        QListWidget::item:selected {color: white; background-color: #0080FF; }
        QListWidget::item {padding: 10;}
        """)

        self.btn_ok = self.button_box.button(QDialogButtonBox.Ok)
        self.btn_ok.setIcon(QIcon(str(ICONS_DIR.joinpath('ok.png'))))
        self.btn_ok.setIconSize(QSize(16, 16))
        self.btn_ok.clicked.connect(lambda: self.on_ok_clicked())

        self.btn_cancel = self.button_box.button(QDialogButtonBox.Cancel)
        self.btn_cancel.setIcon(QIcon(str(ICONS_DIR.joinpath('cancel.png'))))
        self.btn_cancel.setIconSize(QSize(16, 16))
        self.btn_cancel.clicked.connect(lambda: self.on_cancel_clicked())

        self.btn_delete = self.button_box.button(QDialogButtonBox.Reset)
        self.btn_delete.setText('Delete')
        self.btn_delete.setEnabled(False)
        self.btn_delete.setIcon(QIcon(str(ICONS_DIR.joinpath('delete.png'))))
        self.btn_delete.setIconSize(QSize(16, 16))
        self.btn_delete.clicked.connect(lambda: self.on_delete_clicked())

        self.list_widget.doubleClicked.connect(lambda: self.on_ok_clicked())
        self.list_widget.itemClicked.connect(lambda _: self.on_list_item_clicked())

        for each in TEMPLATES_DIR.iterdir():
            if each.name.endswith('.docx'):
                item = QListWidgetItem(str(each.name))
                icon = QIcon(str(ICONS_DIR.joinpath('templates.png')))
                item.setIcon(icon)
                self.list_widget.addItem(item)

    def on_list_item_clicked(self):
        """List item clicked"""
        self.btn_delete.setEnabled(True)

    def on_ok_clicked(self):
        """Ok triggered"""
        items = self.list_widget.selectedItems()
        for item in items:
            selected = item.text()
            self.on_save.emit(selected)
            self.close()

    def on_cancel_clicked(self):
        """Cancel trigger"""
        self.close()

    def on_delete_clicked(self):
        """Delete triggered"""
        item = self.list_widget.currentItem()
        answer = QMessageBox.question(self, f'Delete {item.text()}?',
                                      f'Do you really want to delete template permanently?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            self.list_widget.takeItem(self.list_widget.currentRow())
            file = TEMPLATES_DIR.joinpath(item.text())
            file.unlink(missing_ok=True)
