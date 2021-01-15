from PyQt5.QtCore import QThread, pyqtSignal

from contrib import upload_files, generate_document


class TaskUploadTemplates(QThread):
    """Task Upload Templates"""
    on_upload_start = pyqtSignal()
    on_upload_finish = pyqtSignal()
    on_upload_success = pyqtSignal(list)
    on_upload_fail = pyqtSignal(str)

    def __init__(self, parent, filenames):
        """Initialise"""
        super().__init__(parent=parent)
        self.filenames = filenames

    def run(self) -> None:
        """Run task"""
        try:
            self.on_upload_start.emit()
            uploaded_files = upload_files(filenames=self.filenames)
            self.on_upload_success.emit(uploaded_files)
        except Exception as ex:
            self.on_upload_fail.emit(str(ex))
        finally:
            self.on_upload_finish.emit()


class TaskGenerateDocument(QThread):
    on_generate_start = pyqtSignal()
    on_generate_finish = pyqtSignal()
    on_generate_success = pyqtSignal(str)
    on_generate_fail = pyqtSignal(str)

    def __init__(self, parent, template, context, filename):
        """Initialise"""
        super().__init__(parent=parent)
        self.template = template
        self.context = context
        self.filename = filename

    def run(self) -> None:
        """Run task"""
        try:
            self.on_generate_start.emit()
            generate_document(template=self.template, context=self.context, filename=self.filename)
            self.on_generate_success.emit(self.filename)
        except Exception as ex:
            self.on_generate_fail.emit(str(ex))
        finally:
            self.on_generate_finish.emit()
