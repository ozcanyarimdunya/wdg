import re
from pathlib import Path

from PyQt5 import uic  # noqa
from PyQt5.QtCore import (
    pyqtSignal,
    QSize
)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QFormLayout,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QFileDialog,
)

from dg import (
    UI_DIR,
    ICONS_DIR,
    TEMPLATES_DIR
)
from dg.task import TaskGenerateDocument


class GeneratorWindow(QWidget):
    """
    Dynamic Generated Window
    """
    on_cancel = pyqtSignal()
    values = {}
    layout: QFormLayout
    button_box: QDialogButtonBox

    def __init__(self, variables, name):
        """Initialise"""
        super().__init__()
        self.variables = variables
        self.name = name
        self.setup_ui()
        self.setup_buttonbox()
        self.create_form_box()

    def setup_ui(self):
        """Setup ui"""
        ui_path = UI_DIR / 'generator.ui'
        uic.loadUi(str(ui_path), self)

    def setup_buttonbox(self):
        """Setup buttonbox"""
        btn_ok = self.button_box.button(QDialogButtonBox.Ok)
        btn_ok.setIcon(QIcon(str(ICONS_DIR.joinpath('ok.png'))))
        btn_ok.setIconSize(QSize(16, 16))
        btn_ok.clicked.connect(lambda: self.on_accepted())
        btn_cancel = self.button_box.button(QDialogButtonBox.Cancel)
        btn_cancel.setIcon(QIcon(str(ICONS_DIR.joinpath('cancel.png'))))
        btn_cancel.setIconSize(QSize(16, 16))
        btn_cancel.clicked.connect(lambda: self.on_rejected())

    @staticmethod
    def normalize(string):
        """Normalize given string"""
        return re.sub(r'[\W_]+', ' ', string).title()

    def create_form_box(self):
        """Dynamic form create"""
        for each in self.variables:
            widget = QLineEdit()
            widget.setObjectName(each)
            label = QLabel(each.title())  # noqa
            self.layout.addRow(label, widget)

    def set_values(self):
        """Set values dynamically"""
        self.values = {}
        for i in range(1, len(self.variables) * 2, 2):
            widget = self.layout.itemAt(i).widget()
            self.values[widget.objectName()] = widget.text()

    def render_template(self):
        """Render word document from template"""
        template = TEMPLATES_DIR.joinpath(self.name)
        if not template.exists():
            QMessageBox.information(self, 'Error', f'{template.name} document not found!')
            return

        directory = str(Path.home().joinpath('Desktop').joinpath(template.name))

        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, 'Save generated document', directory,
                                                  'Docx Files (*.docx)', options=options)
        if not filename:
            return

        if not str(filename).endswith('.docx'):
            filename = f'{filename}.docx'

        self.task_generate = TaskGenerateDocument(  # noqa
            parent=self,
            template=str(template),
            context=self.values,
            filename=filename
        )
        self.task_generate.start()
        self.task_generate.on_generate_start.connect(lambda: self.setEnabled(False))
        self.task_generate.on_generate_finish.connect(lambda: self.setEnabled(True))
        self.task_generate.on_generate_success.connect(lambda file: self.on_generate_document_success(file))
        self.task_generate.on_generate_fail.connect(lambda error: self.on_generate_document_fail(error))

    def on_generate_document_start(self):
        """On generate document task start"""
        self.setEnabled(False)

    def on_generate_document_finish(self):
        """On generate document task finish"""
        self.setEnabled(True)

    def on_generate_document_success(self, filename):
        """On generate document task success"""
        parent = str(Path(filename).parent)
        file = str(Path(filename).name)
        QMessageBox.information(self, 'Success',
                                f'Document <a href="file:///{parent}">{file}</a> generated successfully!')

    def on_generate_document_fail(self, error):
        """On generate document task fail"""
        QMessageBox.warning(self, 'Error', f'An error occurred when generating document. <br/>Error: {error}')

    def on_accepted(self):
        """Accepted signal"""
        try:
            self.set_values()
            self.render_template()
        except Exception as ex:
            QMessageBox.warning(self, 'Error', f'An error occurred: {str(ex)}')

    def on_rejected(self):
        """Rejected signal"""
        self.on_cancel.emit()
