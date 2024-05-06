import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class GalleryScreen(QWidget):
    def __init__(self):
        super().__init__()

        QLabel("Gallery", self)
