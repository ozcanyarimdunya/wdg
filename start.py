try:
    from PyQt5.QtCore import QLockFile, QDir

    lockfile = QLockFile(QDir.tempPath() + '/wdg.lock')
    is_single = lockfile.tryLock(100)
except:
    is_single = True

import logging
import sys
from logging.handlers import RotatingFileHandler

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from dg import (
    ICONS_DIR,
    LOG_DIR
)
from dg.contrib import get_style
from dg.home import HomeWindow

log_file = LOG_DIR / 'app.log'
logging.basicConfig(  # noqa
    level=logging.INFO,
    format="[%(asctime)s]:%(levelname)s %(name)s :%(module)s/%(funcName)s,%(lineno)d: %(message)s",
    handlers=[
        RotatingFileHandler(str(log_file)),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()


def define_win_extras():
    """Windows only definition"""
    try:
        from PyQt5.QtWinExtras import QtWin  # noqa

        app_id = 'semiworld.org.tools.wdg'
        QtWin.setCurrentProcessExplicitAppUserModelID(app_id)  # noqa
    except ImportError:
        pass


def main():
    """Main function to run application"""
    try:
        logger.info("Starting application")
        app = QApplication(sys.argv)
        app.setStyleSheet(get_style())
        ico = ICONS_DIR / 'icons.ico'
        app.setWindowIcon(QIcon(str(ico)))
        window = HomeWindow()
        if not is_single:
            QMessageBox.warning(window, 'Error', 'Application is already running!')
            exit(0)

        window.show()
        sys.exit(app.exec_())
    except Exception as ex:
        logger.exception(ex)
    finally:
        logger.info("Exiting application")


if __name__ == '__main__':
    define_win_extras()
    main()
