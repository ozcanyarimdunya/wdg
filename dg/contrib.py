from pathlib import Path

import textract
from docxtpl import DocxTemplate
from jinja2 import (
    BaseLoader,
    Environment,
    meta
)


def get_variables(filename):
    """Extract text from template file and get jinja variables"""
    extracted = textract.process(filename)
    env = Environment(loader=BaseLoader())
    content = env.parse(extracted)
    variables = meta.find_undeclared_variables(content)
    return variables


def get_unique_filename(filename: Path):
    """Get a unique filename"""
    if filename.exists():
        directory = filename.parent
        file = f'{filename.stem}(1){filename.suffix}'
        filename = Path(directory).joinpath(file)
        return get_unique_filename(filename)
    return filename


def generate_document(template, context, filename):
    """Generate word document from template"""
    doc = DocxTemplate(template)
    doc.render(context=context)
    doc.save(filename)
