from pathlib import Path

from PyQt5 import uic  # noqa
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QStatusBar,
    QMenu,
    QAction,
    QToolBar,
    QMessageBox,
    QFileDialog,
    QDockWidget,
    QListWidget,
    QWidget,
    QListWidgetItem
)

from dg import (
    SETTINGS_FILE,
    TEMPLATES_DIR,
    __version__,
    __app_name__,
    __website__,
    __author__
)
from dg.generator import GeneratorWindow
from dg.mixins import ResourceMixin
from dg.settings import SettingsWindow
from dg.task import TaskExtractVariables, TaskUploadTemplates


class HomeWindow(QMainWindow, ResourceMixin):
    """
    Home Window
    """
    tab_widget: QTabWidget
    statusbar: QStatusBar
    toolbar: QToolBar
    menu_file: QMenu
    menu_window: QMenu
    menu_help: QMenu
    action_upload: QAction
    action_settings: QAction
    action_quit: QAction
    action_generate: QAction
    action_discard: QAction
    action_close_all: QAction
    action_about: QAction
    dock_widget: QDockWidget
    list_widget: QListWidget

    def __init__(self):
        """Initialise"""
        super().__init__()
        self.setup_ui()
        self.load_templates()
        self.show_template_message()
        self.settings = QSettings(str(SETTINGS_FILE), QSettings.IniFormat)

    def setup_ui(self):
        """Setup ui"""
        uic.loadUi(self.get_ui_path('home'), self)
        self.action_about.triggered.connect(lambda: self.on_about_triggered())
        self.action_quit.triggered.connect(lambda: self.close())  # noqa
        self.action_settings.triggered.connect(lambda: self.on_settings_triggered())
        self.action_upload.triggered.connect(lambda: self.on_upload_triggered())
        self.action_generate.triggered.connect(lambda: self.on_generate_triggered())
        self.action_discard.triggered.connect(lambda: self.on_discard_triggered())
        self.action_close_all.triggered.connect(lambda: self.on_close_all_triggered())
        self.dock_widget.setTitleBarWidget(QWidget())
        self.list_widget.installEventFilter(self)
        self.list_widget.itemDoubleClicked.connect(lambda item: self.on_templates_selected(item.text()))
        self.list_widget.contextMenuEvent = lambda event: self.on_list_widget_context(event)
        self.list_widget.enterEvent = lambda e: self.show_template_message()
        self.tab_widget.currentChanged.connect(lambda index: self.on_tab_changed(index))
        self.tab_widget.tabCloseRequested.connect(lambda index: self.on_tab_closed(index))
        self.toolbar.enterEvent = lambda e: self.show_toolbar_message()
        self.toolbar.contextMenuEvent = lambda e: None
        self.toolbar.addAction(self.action_upload)
        self.toolbar.addSeparator()
        self.list_widget.setToolTip('Double click on a template and start generating!')
        self.action_upload.setToolTip('Upload a template or select an existing template below!')
        self.action_upload.hovered.connect(lambda *args: self.show_toolbar_message())
        self.action_generate.setToolTip('Generate current active tab')
        self.action_generate.hovered.connect(lambda *args: self.show_form_message())
        self.action_discard.setToolTip('Discard current active tab')

    def show_message(self, message):
        """Set statusbar message"""
        self.statusbar.showMessage(message)

    def show_template_message(self):
        """Show template message"""
        self.show_message('Double click on templates and start generating!')

    def show_toolbar_message(self):
        """Show toolbar message"""
        self.show_message('Upload a template or select an existing template below!')

    def show_form_message(self):
        """Show form message"""
        self.show_message("Fill the forms and click Generate")

    def load_templates(self):
        """Load templates"""
        self.list_widget.clear()
        for each in TEMPLATES_DIR.iterdir():
            if each.name.endswith('.docx'):
                item = QListWidgetItem(str(each.name))
                item.setIcon(self.get_as_icon('templates'))
                self.list_widget.addItem(item)

    def on_list_widget_context(self, event: QContextMenuEvent):
        """On list widget right clicked"""
        menu = QMenu(parent=self)
        item = self.list_widget.itemAt(event.pos())
        if not item:
            return

        action_run = QAction(self.get_as_icon('use'), 'Use This Template', self)
        action_run.triggered.connect(lambda: self.on_templates_selected(item.text()))
        menu.addAction(action_run)

        action_delete = QAction(self.get_as_icon('delete'), 'Delete Template', self)
        action_delete.triggered.connect(lambda: self.on_delete_template_clicked(item))
        menu.addAction(action_delete)
        menu.exec_(event.globalPos())

    def on_delete_template_clicked(self, item):
        """Delete template triggered"""
        answer = QMessageBox.question(self, f'Delete {item.text()}?',
                                      f'Do you really want to delete template permanently?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            file = TEMPLATES_DIR.joinpath(item.text())
            file.unlink(missing_ok=True)
            self.load_templates()

    def on_tab_changed(self, index):
        """On tab changed"""
        has_tab = index >= 0
        self.action_close_all.setEnabled(has_tab)
        self.action_generate.setEnabled(has_tab)
        self.action_discard.setEnabled(has_tab)

        if has_tab:
            self.toolbar.addAction(self.action_generate)
            self.toolbar.addAction(self.action_discard)
        else:
            self.toolbar.removeAction(self.action_generate)
            self.toolbar.removeAction(self.action_discard)

    def on_tab_closed(self, index):
        """On tab closed"""
        self.tab_widget.removeTab(index)
        if self.tab_widget.count() == 0:
            self.show_template_message()

    def closeEvent(self, event):
        if self.on_quit_triggered():
            return super().closeEvent(event)
        event.ignore()

    def on_quit_triggered(self):
        """On quit action triggered"""
        active_windows = self.tab_widget.count()
        if active_windows == 0:
            return True

        answer = QMessageBox.question(self, 'Quit?',
                                      f'There are {active_windows} active window(s), do you really want to quit?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        return answer == QMessageBox.Yes

    def on_settings_triggered(self):
        """On settings action triggered"""
        window = SettingsWindow(self)
        window.show()

    def on_upload_triggered(self):
        """On upload action triggered"""
        directory = str(Path.home().joinpath('Desktop'))
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Upload templates", directory,
                                                    "Docx Files (*.docx)", options=options)

        if not filenames:
            return

        self.task_upload = TaskUploadTemplates(parent=self, filenames=filenames)  # noqa
        self.task_upload.start()
        self.task_upload.on_upload_start.connect(lambda: self.setEnabled(False))
        self.task_upload.on_upload_finish.connect(lambda: self.setEnabled(True))
        self.task_upload.on_upload_success.connect(lambda files: self.on_upload_templates_success(files))
        self.task_upload.on_upload_fail.connect(lambda error: self.on_upload_templates_fail(error))

    def on_upload_templates_success(self, files):
        """On upload templates task success"""
        uploaded_files = '<br>'.join(files)
        QMessageBox.information(self, 'Success',
                                f'<b>{uploaded_files}</b> uploaded successfully!'
                                f'<br>'
                                f'Now double click on template and start generating!')
        self.load_templates()

    def on_upload_templates_fail(self, error):
        """On upload templates task fail"""
        QMessageBox.warning(self, 'Error', f'Error on upload file! <br>Error: {error}')

    def on_templates_selected(self, name):
        """On template selected"""
        filename = TEMPLATES_DIR.joinpath(name)
        if not filename.exists():
            QMessageBox.information(self, 'Error', f'{filename} not found!')
            return

        self.task_extract = TaskExtractVariables(parent=self, filename=filename)  # noqa
        self.task_extract.start()
        self.task_extract.on_extract_start.connect(lambda: self.setEnabled(False))
        self.task_extract.on_extract_finish.connect(lambda: self.setEnabled(True))
        self.task_extract.on_extract_success.connect(lambda v: self.on_extract_variables_success(v, name))
        self.task_extract.on_extract_fail.connect(lambda error: self.on_extract_variables_fail(error))

    def on_extract_variables_success(self, variables, name):
        """On extract variables task success"""
        window = GeneratorWindow(variables=variables, name=name)
        window.enterEvent = lambda e: self.show_form_message()
        self.tab_widget.addTab(window, name)
        self.tab_widget.setTabIcon(self.tab_widget.currentIndex(), self.get_as_icon('templates'))
        self.tab_widget.setTabIcon(self.tab_widget.currentIndex() + 1, self.get_as_icon('templates'))
        self.tab_widget.setCurrentWidget(window)

    def on_extract_variables_fail(self, error):
        """On extract variables task fail"""
        QMessageBox.warning(self, 'Error', f'An error occurred when parsing template. <br/>Error: {error}'
                                           '<hr>'
                                           '<br>Probable errors:'
                                           '<br><b>-></b> It could be non-english character'
                                           '<br><b>-></b> It could have empty space'
                                           '<br><b>-></b> One of {{ or }} may be missing'
                                           '<hr>'
                                           '<br><b>-></b> field definition should be like: <b>{{field}}</b>')

    def on_generate_triggered(self):
        """On generate action triggered"""
        window: GeneratorWindow = self.tab_widget.currentWidget()
        window.generate()

    def on_discard_triggered(self):
        """On discard action triggered"""
        self.tab_widget.removeTab(self.tab_widget.currentIndex())

    def on_close_all_triggered(self):
        """On close all action triggered"""
        self.tab_widget.clear()
        self.show_template_message()

    def on_about_triggered(self):
        """On about action triggered"""
        about = QMessageBox(self)
        about.setWindowTitle(f'{__app_name__} {__version__}')

        about.setText(
            f'<br>'
            f'<hr>'
            f'<center>'
            f'Created <b>@2021</b> '
            f'<br>'
            f'by <a href="{__website__}">{__author__}</a> '
            f'<br>'
            f'with 💖💖💖'
            f'</center>'
            f'<hr>'
        )
        about.setIconPixmap(self.get_as_pixmap('pp'))
        about.show()
