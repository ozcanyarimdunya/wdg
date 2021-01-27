from PyQt5 import uic  # noqa
from PyQt5.QtCore import (
    pyqtSignal,
    QSettings,
    Qt
)
from PyQt5.QtWidgets import (
    QDialog,
    QRadioButton,
    qApp
)

from dg import SETTINGS_FILE
from dg.contrib import get_style
from dg.mixins import ResourceMixin


class SettingsWindow(QDialog, ResourceMixin):
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
        uic.loadUi(self.get_ui_path('settings'), self)
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
