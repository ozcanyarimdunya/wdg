import os
import pathlib

__version__ = '0.1.0'
__author__ = '@ozcanyarimdunya'

BASE_DIR = pathlib.Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
TEMPLATES_DIR = ASSETS_DIR / 'templates'
ICONS_DIR = ASSETS_DIR / 'icons'
UI_DIR = ASSETS_DIR / 'ui'
if not TEMPLATES_DIR.exists():
    os.mkdir(TEMPLATES_DIR)

if not ICONS_DIR.exists():
    os.mkdir(ICONS_DIR)

if not UI_DIR.exists():
    raise Exception('Cannot start without ui files')
