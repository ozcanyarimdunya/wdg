from pathlib import Path

from PyQt5 import uic  # noqa
from PyQt5.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QStatusBar,
    QMenu,
    QAction,
    QToolBar,
    QMessageBox,
    QFileDialog,
)

from dg import (
    UI_DIR,
    TEMPLATES_DIR,
    __version__,
    __app__,
    __website__,
    __author__
)
from dg.generator import GeneratorWindow
from dg.task import TaskExtractVariables, TaskUploadTemplates
from dg.templates import TemplatesWindow


class HomeWindow(QMainWindow):
    """
    Home Window
    """
    tab_widget: QTabWidget
    statusbar: QStatusBar
    toolbar: QToolBar
    menu_file: QMenu
    menu_window: QMenu
    menu_help: QMenu
    action_templates: QAction
    action_upload: QAction
    action_quit: QAction
    action_generate: QAction
    action_discard: QAction
    action_close_all: QAction
    action_about: QAction

    def __init__(self):
        """Initialise"""
        super().__init__()
        self.setup_ui()
        self.setup_actions()
        self.setup_toolbar()
        self.show_initial_message()

    def setup_ui(self):
        """Setup ui"""
        ui_path = UI_DIR / 'home.ui'
        uic.loadUi(str(ui_path), self)
        self.setStyleSheet("""
        QDockWidget, QMenuBar { background-color: transparent; } 
        QListWidget::item { border-bottom: 1 solid lightgray; }
        QListWidget::item:selected { background-color: white; }
        QListWidget, QLineEdit#txt_search { border: 1 solid lightgray; }
        QPlainTextEdit, QLineEdit { border: 1 solid #A7AAA5; padding: 5; }
        QScrollArea { border: 0 solid; }
        QWidget#scrollWidget { background-color: white; }
        """)

    def setup_actions(self):
        """Setup actions"""
        self.action_about.triggered.connect(lambda: self.on_about_triggered())
        self.action_quit.triggered.connect(lambda: self.on_quit_triggered())
        self.action_templates.triggered.connect(lambda: self.on_templates_triggered())
        self.action_upload.triggered.connect(lambda: self.on_upload_triggered())
        self.action_generate.triggered.connect(lambda: self.on_generate_triggered())
        self.action_discard.triggered.connect(lambda: self.on_discard_triggered())
        self.action_close_all.triggered.connect(lambda: self.on_close_all_triggered())
        self.closeEvent = lambda event: self.on_quit_triggered()  # noqa

    def setup_toolbar(self):
        """Setup toolbar"""
        self.tab_widget.tabCloseRequested.connect(lambda index: self.on_tab_closed(index))
        self.tab_widget.currentChanged.connect(lambda index: self.on_tab_changed(index))
        self.toolbar.addActions([self.action_templates, self.action_upload])
        self.toolbar.addSeparator()

    def show_initial_message(self):
        """Show statusbar message"""
        self.statusbar.showMessage('Click on templates button, select template and start generating!', 5000)

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
            self.show_initial_message()

    def on_quit_triggered(self):
        """On quit action triggered"""
        active_windows = self.tab_widget.count()
        if active_windows == 0:
            self.close()
            return

        answer = QMessageBox.question(self, 'Quit?',
                                      f'There are {active_windows} active window(s), do you really want to quit?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if answer == QMessageBox.Yes:
            self.close()

    def on_templates_triggered(self):
        """On templates action triggered"""
        window = TemplatesWindow(self)
        window.show()
        window.on_save.connect(lambda name: self.on_templates_selected(name))

    def on_upload_triggered(self):
        """On upload action triggered"""
        directory = str(Path.home().joinpath('Desktop'))
        options = QFileDialog.Options()
        filenames, _ = QFileDialog.getOpenFileNames(self, "Upload template", directory,
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
        QMessageBox.information(self, 'Success', f'<b>{uploaded_files}</b> uploaded successfully!')
        self.on_templates_triggered()

    def on_upload_templates_fail(self, error):
        """On upload templates task fail"""
        QMessageBox.information(self, 'Error', f'Error on upload file! <br>Error: {error}')

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
        self.tab_widget.addTab(window, name)
        self.tab_widget.setCurrentWidget(window)

    def on_extract_variables_fail(self, error):
        """On extract variables task fail"""
        QMessageBox.warning(self, 'Error', f'An error occurred when parsing template. <br/>Error: {error}')

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
        self.show_initial_message()

    def on_about_triggered(self):
        """On about action triggered"""
        QMessageBox.about(self, __app__,
                          f'<br>Created <b>@2021</b> by <a href="{__website__}">{__author__}</a> with 💖💖💖 '
                          f'<br><br>Version: <b>{__version__}</b>')
