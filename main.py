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

        os.system("xrandr -o left")

        tabs = QTabWidget(self)
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.setFixedSize(640, 480)
        tabs.setIconSize(QSize(45, 45))
        tabs.showFullScreen()
        tabs.setStyleSheet("background-color:black;font-size:11pt;")

        self.tabs_list = [
            CameraScreen("Camera", "assets/shutter.png"),
            GalleryScreen("Gallery", "assets/gallery.png"),
            WifiScreen("Wifi", "assets/wifi.png"),
            WalletScreen("AR Wallet", "assets/wallet.png"),
            SettingsScreen("Settings", "assets/settings.png"),
        ]

        for tab in self.tabs_list:
            tabs.addTab(tab, tab.icon, tab.name)

        tabs.currentChanged.connect(self.tab_changed)

    def tab_changed(self, i):
        tab = self.tabs_list[i]
        if tab.name == "Camera":
            tab.camera.start()
        else:
            # make sure the first widget is always the camera one
            self.tabs_list[0].camera.stop()

        if tab.name == "Gallery":
            tab.active_screen = True
            tab.goto_start()
        else:
            # tab.active_screen = False
            self.tabs_list[1].active_screen = False

        if tab.name == "AR Wallet":
            tab.load_wallet()
            tab.start_server()
        else:
            self.tabs_list[3].stop_server()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainScreen()
    window.show()
    app.exec()
