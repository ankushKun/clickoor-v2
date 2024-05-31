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

from settings import SettingsOptions

import arweave

wallet_path = "wallet.json"


class WalletLoadWorker(QThread):
    wallet_loaded = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            wallet = arweave.Wallet(wallet_path)
            self.wallet_loaded.emit({"ok": True, "wallet": wallet})
        except Exception as e:
            print(e)
            self.wallet_loaded.emit({"ok": False, "wallet": None})


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        SettingsOptions.load()
        self.setWindowTitle("Clickoor")
        self.setFixedSize(640, 480)
        self.showFullScreen()

        if SettingsOptions.display_orientation == "flipped":
            os.system("xrandr -o right")
            os.system("wlr-randr --output DSI-1 --transform 270")
        else:
            os.system("xrandr -o left")
            os.system("wlr-randr --output DSI-1 --transform 90")

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

        self.load_wallet()

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
            tab.start_server()
        else:
            self.tabs_list[3].stop_server()

    def load_wallet(self):
        self.wallet_load_worker = WalletLoadWorker()
        self.wallet_load_worker.wallet_loaded.connect(self.wallet_loaded)
        self.wallet_load_worker.start()

    def wallet_loaded(self, d):
        if d["ok"]:
            self.wallet = d["wallet"]
            # self.status.setText("Wallet Loaded")
            self.tabs_list[0].set_wallet(self.wallet)  # camera
            self.tabs_list[1].set_wallet(self.wallet)  # gallery
            self.tabs_list[3].set_wallet(self.wallet)  # wallet
        else:
            self.wallet = None
            # self.status.setText("Wallet Load Failed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainScreen()
    window.show()
    app.exec()
