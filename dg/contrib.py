import shutil
from pathlib import Path

import textract
from docxtpl import DocxTemplate
from jinja2 import (
    BaseLoader,
    Environment,
    meta
)

from dg import TEMPLATES_DIR


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
