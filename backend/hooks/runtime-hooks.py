import sys
import os

def add_paths():
    if getattr(sys, 'frozen', False):
        sys.path.append(os.path.join(sys._MEIPASS, 'flask'))
        sys.path.append(os.path.join(sys._MEIPASS, 'werkzeug'))

add_paths()