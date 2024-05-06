import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# sudo apt-get install python3-pyqt5.qtsvg
# pip3 install pyqtdarktheme --break-system-packages
import qdarktheme

# import screens here
from camera import CameraScreen
from settings import SettingsScreen
from wallet import WalletScreen
from wifi import WifiScreen
from gallery import GalleryScreen


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Clickoor")
        self.setFixedSize(640, 480)
        self.showFullScreen()

        tabs = QTabWidget(self)
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setFixedSize(640, 480)
        tabs.setIconSize(QSize(45, 45))
        tabs.showFullScreen()
        tabs.setStyleSheet("background-color:black;font-size:11pt;")

        # add screens here
        tabs.addTab(CameraScreen(), QIcon("assets/shutter.png"), "Camera")
        tabs.addTab(GalleryScreen(), QIcon("assets/gallery.png"), "Gallery")
        tabs.addTab(WifiScreen(), QIcon("assets/wifi.png"), "Wifi")
        tabs.addTab(WalletScreen(), QIcon("assets/wallet.png"), "AR Wallet")
        tabs.addTab(SettingsScreen(), QIcon("assets/settings.png"), "Settings")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainScreen()
    window.show()
    # window.setStyleSheet("background-color:black;")
    app.exec()
