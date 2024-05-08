import sys, os, json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class SettingsOptions:
    settings_path = "settings.json"
    preview_res = (1920, 1080)
    image_res = (1920, 1080)
    video_res = (1280, 720)
    auto_upload_images = True
    auto_upload_videos = False

    def load():
        if os.path.exists(SettingsOptions.settings_path):
            s_local = json.load(open(SettingsOptions.settings_path, "r"))
            SettingsOptions.preview_res = s_local["preview_res"]
            SettingsOptions.image_res = s_local["image_res"]
            SettingsOptions.video_res = s_local["video_res"]
            SettingsOptions.auto_upload_images = s_local["auto_upload_images"]
            SettingsOptions.auto_upload_videos = s_local["auto_upload_videos"]
        else:
            print(
                f"{SettingsOptions.settings_path} not found, creating one with defaults"
            )
            SettingsOptions.save()

    def save():
        s_new = {
            "preview_res": SettingsOptions.preview_res,
            "image_res": SettingsOptions.image_res,
            "video_res": SettingsOptions.video_res,
            "auto_upload_images": SettingsOptions.auto_upload_images,
            "auto_upload_videos": SettingsOptions.auto_upload_videos,
        }
        json.dump(s_new, open(SettingsOptions.settings_path, "w"))


class SettingsScreen(QWidget):
    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)

        self.image_res_selector = QComboBox(self)
        self.image_res_selector.addItem("1080p")
        self.image_res_selector.addItem("720p")
        self.image_res_selector.currentTextChanged.connect(self.image_res_changed)
        self.image_res_selector.setFixedSize(QSize(200, 100))

        #i = QListWidgetItem()
        #i.setText("OK")
        #l = QListWidget(self)
        #l.addItem(i)
        #l.addItem(i)

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #vlayout.addWidget(i)
        vlayout.addWidget(self.image_res_selector)

        self.setLayout(vlayout)

    def image_res_changed(self, res):
        print(res)
