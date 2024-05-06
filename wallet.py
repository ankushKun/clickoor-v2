import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class WalletScreen(QWidget):

    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)

        QLabel("Wallet", self)
