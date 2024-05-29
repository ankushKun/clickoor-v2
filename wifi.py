import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def get_available_wifis():
    avl = []
    lines = os.popen("sudo iwlist wlan0 scan").read().split("\n")
    for line in lines:
        line = line.rstrip()
        if line != "" and "ESSID" in line:
            name = line.split('"')[1]
            avl.append(name)
    return avl


def current_connection():
    lines = os.popen("nmcli -t -f NAME con show --active").read().split("\n")
    if len(lines) > 0:
        return lines[0]
    return None


class WifiWorker(QThread):
    wifi_list_updated = pyqtSignal(list)

    def run(self):
        available_wifis = get_available_wifis()
        self.wifi_list_updated.emit(available_wifis)


class ConnectWorker(QThread):
    connection_status = pyqtSignal(bool)

    def __init__(self, ssid, password):
        super().__init__()
        self.ssid = ssid
        self.password = password

    def run(self):
        r = os.system(
            f"sudo nmcli dev wifi connect {self.ssid} password {self.password}"
        )
        if r == 0:
            self.connection_status.emit(True)
        else:
            self.connection_status.emit(False)


class WifiScreen(QWidget):

    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)
        self.caps_lock = False
        self.availale_networks = []

        # ssid_selector = QComboBox()
        # ssid_selector.addItems(get_available_wifis())

        # connect_button = QPushButton("Connect")
        # connect_button.clicked.connect(self.connect_to_wifi)

        # layout = QVBoxLayout()
        # layout.addWidget(ssid_selector)
        # layout.addWidget(connect_button)
        # self.setLayout(layout)

        # WIFI SSID CONTAINER
        ssid_container = QWidget(self)
        ssid_container.setFixedSize(640, 50)
        ssid_container.move(0, 0)
        ssid_container.setStyleSheet("background-color:black;")
        ssid_container.setLayout(QVBoxLayout())

        ssid_label = QLabel("Select a wifi network:", ssid_container)
        ssid_label.setStyleSheet("color:white;")
        ssid_label.setFixedSize(200, 50)
        ssid_label.move(0, 0)

        self.ssid_selector = QComboBox(ssid_container)
        self.ssid_selector.addItems(get_available_wifis())
        self.ssid_selector.setFixedSize(200, 50)
        self.ssid_selector.move(200, 0)

        # PASSWORD CONTAINER

        pass_container = QWidget(self)
        pass_container.setFixedSize(640, 50)
        pass_container.move(0, 50)
        pass_container.setStyleSheet("background-color:black;")
        pass_container.setLayout(QVBoxLayout())

        pass_label = QLabel("Enter password:", pass_container)
        pass_label.setStyleSheet("color:white;")
        pass_label.setFixedSize(200, 50)
        pass_label.move(0, 0)

        self.pass_input = QLineEdit(pass_container)
        self.pass_input.setFixedSize(200, 50)
        self.pass_input.move(200, 0)

        # VIRTUAL KEYBOARD
        self.keyboard_container = QWidget(self)
        self.keyboard_container.setFixedSize(640, 300)
        self.keyboard_container.move(0, 100)
        self.keyboard_container.setStyleSheet("background-color:black;")
        self.keyboard_container.setLayout(QGridLayout())

        keyboard = [
            # ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "", "CAP", "SPC"],
            # ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"],
            # ["n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
            # ["%", "^", "&", "*", "(", ")", "-", "_", "+", "=", "[", "]", ""],
            # ["$", "@", ";", ":", "'", '"', "#", "!", "{", "}", "<", ">", "DEL"],
            # QUERTY FORMAT
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "DEL"],
            ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "+", "="],
            ["CAP", "a", "s", "d", "f", "g", "h", "j", "k", "l", "*", "SPC"],
            ["&&", "^", "z", "x", "c", "v", "b", "n", "m", "%", "_", "", ""],
            ["", "$", "@", ";", ":", "'", '"', "#", "!", "<", ">"],
        ]
        self.keyboard = keyboard

        for i in range(len(keyboard)):
            for j in range(len(keyboard[i])):
                if keyboard[i][j] == "":
                    # add empty space
                    # spacer = QLabel(self.keyboard_container)
                    # spacer.setFixedSize(1, 1)
                    # spacer.move(-200, -200)
                    # self.keyboard_container.layout().addWidget(spacer, i, j)
                    continue
                key = QPushButton(keyboard[i][j], self.keyboard_container)
                key.setStyleSheet("font-size:16px;")
                self.keyboard_container.layout().addWidget(key, i, j)
                key.setStyleSheet("background-color:black;font-weight:bold;")
                key.setFixedSize(48, 48)
                key.move(j * 44, i * 40)
                key.clicked.connect(lambda _, key=key: self.key_pressed(key.text()))

        # CONNECT BUTTON
        connect_button = QPushButton("Connect", self)
        connect_button.setFixedSize(100, 50)
        connect_button.move(430, 0)
        connect_button.clicked.connect(self.connect_to_wifi)

        # REFRESH BTN
        refresh_button = QPushButton("Refresh", self)
        refresh_button.setFixedSize(100, 50)
        refresh_button.move(535, 0)
        refresh_button.clicked.connect(self.refresh)

        # STATUS
        self.status_label = QLabel(f"Connected to: {current_connection()}", self)
        self.status_label.setFixedSize(235, 50)
        self.status_label.move(405, 50)

    def refresh(self):
        self.worker = WifiWorker()
        self.worker.wifi_list_updated.connect(self.update_wifi_list)
        self.status_label.setText("Refreshing...")
        self.worker.start()

    def update_wifi_list(self, wifi_list):
        print(wifi_list)
        self.ssid_selector.clear()
        self.ssid_selector.addItems(wifi_list)
        self.status_label.setText("Refreshed")

    def key_pressed(self, key):
        print(key)
        if len(key) == 0:
            return
        if len(key) > 1:
            if key == "&&":
                self.pass_input.setText(self.pass_input.text() + "&")
            if key == "SPC":
                self.pass_input.setText(self.pass_input.text() + " ")
            elif key == "CAP":
                self.caps_lock = not self.caps_lock
                # for i in range(1, 3):
                #     for j in range(1, 13):
                for i in range(len(self.keyboard)):
                    for j in range(len(self.keyboard[i])):
                        key = (
                            self.keyboard_container.layout()
                            .itemAt(i * len(self.keyboard[i]) + j)
                            .widget()
                        )
                        if len(key.text()) == 1:
                            key.setText(
                                key.text().upper()
                                if self.caps_lock
                                else key.text().lower()
                            )
            elif key == "DEL":
                self.pass_input.setText(self.pass_input.text()[:-1])
        else:
            self.pass_input.setText(self.pass_input.text() + key)
        self.pass_input.setFocus()

    def connect_to_wifi(self):
        if self.ssid_selector.currentText() == "":
            self.status_label.setText("Please select a wifi network")
            return
        if self.pass_input.text() == "":
            self.status_label.setText("Please enter a password")
            return

        self.worker = ConnectWorker(
            self.ssid_selector.currentText(), self.pass_input.text()
        )
        self.worker.connection_status.connect(self.connection_status)
        self.status_label.setText("Connecting...")
        self.worker.start()

    def connection_status(self, status):
        if status:
            self.status_label.setText("Connected to wifi")
        else:
            self.status_label.setText("Failed to connect")

        # print("Connecting to wifi")

        # def connect_in_another_threaad():
        #     r = os.system(
        #         f"nmcli dev wifi connect {self.ssid_selector.currentText()} password {self.pass_input.text()}"
        #     )
        #     if r == 0:
        #         self.status_label.setText("Connected to wifi")
        #     else:
        #         self.status_label.setText("Failed to connect")

        # thread = QThread()
