import pathlib

__version__ = '1.0.6'
__author__ = 'Özcan YARIMDÜNYA'
__website__ = 'http://semiworld.org'
__app_name__ = 'Word Document Generator'

BASE_DIR = pathlib.Path(__file__).parent.parent
DOCUMENT_DIR = pathlib.Path.home() / 'Documents' / __app_name__
ASSETS_DIR = BASE_DIR / 'assets'
TEMPLATES_DIR = DOCUMENT_DIR / 'templates'
LOG_DIR = DOCUMENT_DIR / 'logs'
ICONS_DIR = ASSETS_DIR / 'icons'
UI_DIR = ASSETS_DIR / 'ui'
STYLES_DIR = ASSETS_DIR / 'styles'
SETTINGS_FILE = DOCUMENT_DIR / 'settings.ini'

if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
