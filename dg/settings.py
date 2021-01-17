from PyQt5 import uic  # noqa
from PyQt5.QtCore import (
    pyqtSignal,
    QSettings, Qt
)
from PyQt5.QtWidgets import (
    QDialog,
    QRadioButton,
    qApp
)

from dg import (
    UI_DIR,
    SETTINGS_FILE
)
from dg.contrib import get_style


class SettingsWindow(QDialog):
    """
    Settings Window
    """
    on_save = pyqtSignal()
    rd_theme_normal: QRadioButton
    rd_theme_dark: QRadioButton

    def __init__(self, parent):
        """Initialise"""
        super().__init__(parent=parent)
        self.setup_ui()

    def setup_ui(self):
        """Setup ui"""
        ui_path = UI_DIR / 'settings.ui'
        uic.loadUi(str(ui_path), self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.settings = QSettings(str(SETTINGS_FILE), QSettings.IniFormat)  # noqa
        theme = self.settings.value('theme')
        if theme == 'dark':
            self.rd_theme_dark.setChecked(True)
        else:
            self.rd_theme_normal.setChecked(True)

        self.rd_theme_dark.clicked.connect(lambda x: self.on_theme_selection('dark'))
        self.rd_theme_normal.clicked.connect(lambda x: self.on_theme_selection('normal'))

    def on_theme_selection(self, theme):
        """On theme selected"""
        self.settings.setValue('theme', theme)
        self.settings.sync()
        qApp.setStyleSheet(get_style())
