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


image_res_options = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

video_res_options = {
    "720p": (1280, 720),
    "1080p": (1920, 1080),
}


class SettingsScreen(QWidget):
    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)

        settings_container = QWidget(self)
        settings_container.setFixedSize(640, 400)
        settings_container.move(0, 0)
        settings_container.setStyleSheet("background-color:black;")
        settings_container.setLayout(QVBoxLayout())

        # img config
        img_container = QWidget(settings_container)
        img_container.setFixedSize(640, 50)
        img_container.move(0, 0)
        img_container.setStyleSheet("background-color:black;")
        img_container.setLayout(QHBoxLayout())

        img_res_label = QLabel("Image Resolution:", img_container)
        img_res_label.setStyleSheet("color:white;")
        img_res_label.setFixedSize(200, 50)
        img_res_label.move(0, 0)

        self.img_res_combo = QComboBox(img_container)
        self.img_res_combo.addItems(image_res_options.keys())
        self.img_res_combo.setFixedSize(200, 50)
        self.img_res_combo.move(200, 0)
        self.img_res_combo.currentIndexChanged.connect(self.image_res_changed)

        # Video config
        vid_container = QWidget(settings_container)
        vid_container.setFixedSize(640, 50)
        vid_container.move(0, 50)
        vid_container.setStyleSheet("background-color:black;")
        vid_container.setLayout(QHBoxLayout())

        vid_res_label = QLabel("Video Resolution:", vid_container)
        vid_res_label.setStyleSheet("color:white;")
        vid_res_label.setFixedSize(200, 50)
        vid_res_label.move(0, 0)

        self.vid_res_combo = QComboBox(vid_container)
        self.vid_res_combo.addItems(video_res_options.keys())
        self.vid_res_combo.setFixedSize(200, 50)
        self.vid_res_combo.move(200, 0)
        self.vid_res_combo.currentIndexChanged.connect(self.video_res_changed)

        # Auto upload images
        self.auto_upload_images = QCheckBox(settings_container)
        self.auto_upload_images.setChecked(SettingsOptions.auto_upload_images)
        self.auto_upload_images.setFixedSize(200, 50)
        self.auto_upload_images.move(200, 100)
        self.auto_upload_images.setText("Auto Upload Images")
        self.auto_upload_images.stateChanged.connect(self.auto_upload_images_changed)

        # Auto upload videos
        self.auto_upload_videos = QCheckBox(settings_container)
        self.auto_upload_videos.setChecked(SettingsOptions.auto_upload_videos)
        self.auto_upload_videos.setFixedSize(200, 50)
        self.auto_upload_videos.move(200, 150)
        self.auto_upload_videos.setText("Auto Upload Videos")
        self.auto_upload_videos.stateChanged.connect(self.auto_upload_videos_changed)

        # put all of these in the center and one below another
        layout = QVBoxLayout()
        layout.addWidget(img_container)
        layout.addWidget(vid_container)
        layout.addWidget(self.auto_upload_images)
        layout.addWidget(self.auto_upload_videos)
        self.setLayout(layout)

    def auto_upload_images_changed(self):
        SettingsOptions.auto_upload_images = self.auto_upload_images.isChecked()
        SettingsOptions.save()

    def auto_upload_videos_changed(self):
        SettingsOptions.auto_upload_videos = self.auto_upload_videos.isChecked()
        SettingsOptions.save()

    def image_res_changed(self):
        SettingsOptions.image_res = image_res_options[self.img_res_combo.currentText()]
        SettingsOptions.save()

    def video_res_changed(self):
        SettingsOptions.video_res = video_res_options[self.vid_res_combo.currentText()]
        SettingsOptions.save()
