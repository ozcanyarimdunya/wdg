import pathlib

__version__ = '1.0.0'
__author__ = 'Özcan YARIMDÜNYA'
__website__ = 'http://semiworld.org'
__app__ = 'Word Document Generator'

BASE_DIR = pathlib.Path(__file__).parent.parent
DOCUMENT_DIR = pathlib.Path.home() / 'Documents' / __app__
ASSETS_DIR = BASE_DIR / 'assets'
TEMPLATES_DIR = DOCUMENT_DIR / 'templates'
LOG_DIR = DOCUMENT_DIR / 'logs'
ICONS_DIR = ASSETS_DIR / 'icons'
UI_DIR = ASSETS_DIR / 'ui'


def initialise_sample():
    """Initialise a sample"""
    try:
        sample = ASSETS_DIR / 'templates' / 'Sample.docx'
        local_sample = TEMPLATES_DIR.joinpath('Sample.docx')
        sample.link_to(local_sample)
    except Exception as ex:
        print(ex)


if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
    initialise_sample()

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
