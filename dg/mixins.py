from PyQt5.QtGui import QIcon, QPixmap

from dg import ICONS_DIR, UI_DIR


class ResourceMixin:
    """
    Resource Mixin for Windows
    """

    @staticmethod
    def get_icon_path(name, ext):
        """Get icon path"""
        return str(ICONS_DIR.joinpath(name + ext))

    def get_as_icon(self, name, ext='.png'):
        """Get as icon"""
        return QIcon(self.get_icon_path(name, ext))

    def get_as_pixmap(self, name, ext='.png'):
        """Get as pixmap"""
        return QPixmap(self.get_icon_path(name, ext))

    @staticmethod
    def get_ui_path(name, ext='.ui'):
        """Get ui file path"""
        return str(UI_DIR.joinpath(name + ext))
