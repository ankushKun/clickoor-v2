import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WifiScreen(QWidget):
    def __init__(self):
        super().__init__()

        QLabel("Wallet", self)
