import shutil
from pathlib import Path

import qdarkstyle
import textract
from PyQt5.QtCore import QSettings
from docxtpl import DocxTemplate
from jinja2 import (
    BaseLoader,
    Environment,
    meta
)

from dg import (
    TEMPLATES_DIR,
    SETTINGS_FILE,
    STYLES_DIR
)


def extract_variables(filename):
    """Extract text from template file and get jinja variables"""
    extracted = textract.process(filename)
    env = Environment(loader=BaseLoader())
    content = env.parse(extracted)
    variables = meta.find_undeclared_variables(content)
    return variables


def get_unique_filename(filename: Path):
    """Get a unique filename"""
    if filename.exists():
        file = f'{filename.stem}(1){filename.suffix}'
        filename = Path(filename.parent).joinpath(file)
        return get_unique_filename(filename)
    return filename


def generate_document(template, context, filename):
    """Generate word document from template"""
    doc = DocxTemplate(template)
    doc.render(context=context)
    doc.save(filename)


def upload_files(filenames):
    """Upload files"""
    uploaded_files = []
    for filename in filenames:
        file = Path(filename).name
        destination = get_unique_filename(TEMPLATES_DIR.joinpath(file))
        shutil.copy(filename, str(destination))
        uploaded_files.append(destination.name)

    return uploaded_files


def get_style():
    """Get theme"""
    settings = QSettings(str(SETTINGS_FILE), QSettings.IniFormat)
    theme = settings.value('theme', 'normal')
    if theme == 'dark':
        stylesheet = qdarkstyle.load_stylesheet(qt_api='pyqt5')
        stylesheet += STYLES_DIR.joinpath('dark.qss').read_text()
        return stylesheet

    return STYLES_DIR.joinpath('normal.qss').read_text()
