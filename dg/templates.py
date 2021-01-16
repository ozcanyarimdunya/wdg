from PyQt5 import uic  # noqa
from PyQt5.QtCore import (
    pyqtSignal,
    QSize, Qt
)
from PyQt5.QtGui import QIcon, QKeyEvent
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
        self.setup_ui()
        self.setup_buttonbox()
        self.setup_events()
        self.load_templates()

    def setup_ui(self):
        """Setup ui"""
        ui_path = UI_DIR / 'templates.ui'
        uic.loadUi(str(ui_path), self)
        self.setStyleSheet("""
        QListWidget::item:selected {color: white; background-color: #0080FF; }
        QListWidget::item {padding: 10;}
        """)

    def setup_buttonbox(self):
        """Setup buttonbox"""
        btn_ok = self.button_box.button(QDialogButtonBox.Ok)
        btn_ok.setIcon(QIcon(str(ICONS_DIR.joinpath('ok.png'))))
        btn_ok.setIconSize(QSize(16, 16))
        btn_ok.clicked.connect(lambda: self.on_ok_clicked())
        btn_cancel = self.button_box.button(QDialogButtonBox.Cancel)
        btn_cancel.setIcon(QIcon(str(ICONS_DIR.joinpath('cancel.png'))))
        btn_cancel.setIconSize(QSize(16, 16))
        btn_cancel.clicked.connect(lambda: self.on_cancel_clicked())
        btn_delete = self.button_box.button(QDialogButtonBox.Reset)
        btn_delete.setText('Delete')
        btn_delete.setEnabled(False)
        btn_delete.setIcon(QIcon(str(ICONS_DIR.joinpath('delete.png'))))
        btn_delete.setIconSize(QSize(16, 16))
        btn_delete.clicked.connect(lambda: self.on_delete_clicked())

    def setup_events(self):
        """Setup events"""
        self.list_widget.doubleClicked.connect(lambda: self.on_ok_clicked())
        self.list_widget.itemClicked.connect(lambda item: self.on_list_item_clicked())
        self.list_widget.keyPressEvent = lambda event: self.on_delete_key_pressed(event)

    def load_templates(self):
        """Load templates"""
        self.list_widget.clear()
        for each in TEMPLATES_DIR.iterdir():
            if each.name.endswith('.docx'):
                item = QListWidgetItem(str(each.name))
                icon = QIcon(str(ICONS_DIR.joinpath('templates.png')))
                item.setIcon(icon)
                self.list_widget.addItem(item)

    def on_delete_key_pressed(self, event: QKeyEvent):
        """On delete key pressed"""
        if event.key() == Qt.Key_Delete:
            if self.list_widget.selectedItems():
                self.on_delete_clicked()

    def on_list_item_clicked(self):
        """List item clicked"""
        self.button_box.button(QDialogButtonBox.Reset).setEnabled(True)

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
            file = TEMPLATES_DIR.joinpath(item.text())
            file.unlink(missing_ok=True)
            self.load_templates()
