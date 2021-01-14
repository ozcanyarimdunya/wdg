import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from dg import ICONS_DIR
from dg.home import HomeWindow

try:
    from PyQt5.QtWinExtras import QtWin  # noqa

    app_id = 'semiworld.org.tools.dg'
    QtWin.setCurrentProcessExplicitAppUserModelID(app_id)  # noqa
except ImportError:
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    icon = ICONS_DIR / 'icon.png'
    app.setWindowIcon(QIcon(str(icon)))
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())
