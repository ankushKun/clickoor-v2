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
    display_orientation = "normal"
    camera_orientation = "normal"
    derivation = "None"
    commercial_use = "None"

    def load():
        if os.path.exists(SettingsOptions.settings_path):
            s_local = json.load(open(SettingsOptions.settings_path, "r"))
            SettingsOptions.preview_res = s_local["preview_res"]
            SettingsOptions.image_res = s_local["image_res"]
            SettingsOptions.video_res = s_local["video_res"]
            SettingsOptions.auto_upload_images = s_local["auto_upload_images"]
            SettingsOptions.auto_upload_videos = s_local["auto_upload_videos"]
            SettingsOptions.display_orientation = s_local["display_orientation"]
            SettingsOptions.camera_orientation = s_local["camera_orientation"]
            SettingsOptions.derivation = s_local["derivation"]
            SettingsOptions.commercial_use = s_local["commercial_use"]
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
            "display_orientation": SettingsOptions.display_orientation,
            "camera_orientation": SettingsOptions.camera_orientation,
            "derivation": SettingsOptions.derivation,
            "commercial_use": SettingsOptions.commercial_use
        }
        json.dump(s_new, open(SettingsOptions.settings_path, "w"))

derivation_options = ["Allowed-With-Credit","Allowed-With-Indication", "Allowed-With-License-Passthrough", "None"]
commercial_options = ["Allowed", "Allowed-With-Credit", "None"]

display_orientation_options = ["normal", "flipped"]
camera_orientation_options = ["normal", "flipped"]

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
        

        auto_upload_container = QWidget(settings_container)
        auto_upload_container.setFixedSize(640,50)
        auto_upload_container.setLayout(QHBoxLayout())


        # Auto upload images
        self.auto_upload_images = QCheckBox(auto_upload_container)
        self.auto_upload_images.setChecked(SettingsOptions.auto_upload_images)
        self.auto_upload_images.setFixedSize(200, 50)
        self.auto_upload_images.move(0,0)
        self.auto_upload_images.setText("Auto Upload Images")
        self.auto_upload_images.stateChanged.connect(self.auto_upload_images_changed)

        # Auto upload videos
        self.auto_upload_videos = QCheckBox(auto_upload_container)
        self.auto_upload_videos.setChecked(SettingsOptions.auto_upload_videos)
        self.auto_upload_videos.setFixedSize(200, 50)
        self.auto_upload_videos.move(200, 0)
        self.auto_upload_videos.setText("Auto Upload Videos")
        self.auto_upload_videos.stateChanged.connect(self.auto_upload_videos_changed)

        

        # Camera orientation
        cam_ori_container = QWidget(settings_container)
        cam_ori_container.setFixedSize(640, 50)
        cam_ori_container.setLayout(QHBoxLayout())
        cam_ori_container.move(0,200)


        cam_ori_label = QLabel("Camera orientation: ", cam_ori_container)
        cam_ori_label.setFixedSize(200,50)
        cam_ori_label.move(0,0)

        self.cam_ori_combo = QComboBox(cam_ori_container)
        self.cam_ori_combo.addItems(camera_orientation_options)
        self.cam_ori_combo.setFixedSize(200,50)
        self.cam_ori_combo.move(200,0)
        self.cam_ori_combo.currentIndexChanged.connect(self.camera_orientation_changed)

        # Camera orientation
        dis_ori_container = QWidget(settings_container)
        dis_ori_container.setFixedSize(640, 50)
        dis_ori_container.setLayout(QHBoxLayout())
        dis_ori_container.move(0,250)

        dis_ori_label = QLabel("Display orientation: ", dis_ori_container)
        dis_ori_label.setFixedSize(200,50)
        dis_ori_label.move(0,0)

        self.dis_ori_combo = QComboBox(dis_ori_container)
        self.dis_ori_combo.addItems(display_orientation_options)
        self.dis_ori_combo.setFixedSize(200,50)
        self.dis_ori_combo.move(200,0)
        self.dis_ori_combo.currentIndexChanged.connect(self.display_orientation_changed)

        # UDL Derivation
        deriv_container = QWidget(settings_container)
        deriv_container.setFixedSize(640,50)
        deriv_container.setLayout(QHBoxLayout())
        deriv_container.move(0,300)

        deriv_label = QLabel("UDL Derivation: ", deriv_container)
        deriv_label.setFixedSize(200,50)
        deriv_label.move(0,0)

        self.deriv_combo = QComboBox(deriv_container)
        self.deriv_combo.addItems(derivation_options)
        self.deriv_combo.setFixedSize(200,50)
        self.deriv_combo.move(200,0)
        self.deriv_combo.currentIndexChanged.connect(self.derivation_changed)

        # UDL Derivation
        commer_container = QWidget(settings_container)
        commer_container.setFixedSize(640,50)
        commer_container.setLayout(QHBoxLayout())
        commer_container.move(0,300)

        commer_label = QLabel("UDL Commercial Use: ", commer_container)
        commer_label.setFixedSize(200,50)
        commer_label.move(0,0)

        self.commer_combo = QComboBox(commer_container)
        self.commer_combo.addItems(commercial_options)
        self.commer_combo.setFixedSize(200,50)
        self.commer_combo.move(200,0)
        self.commer_combo.currentIndexChanged.connect(self.commercial_changed)


        # restart button top right corner
        restart_button = QPushButton(settings_container)
        restart_button.setFixedSize(70, 50)
        restart_button.move(570, 50)
        restart_button.setText("Restart")
        restart_button.clicked.connect(lambda: os.system("sudo reboot"))

        # put all of these in the center and one below another
        layout = QVBoxLayout()
        layout.addWidget(img_container)
        layout.addWidget(vid_container)
        # layout.addWidget(self.auto_upload_images)
        # layout.addWidget(self.auto_upload_videos)
        layout.addWidget(auto_upload_container)
        layout.addWidget(cam_ori_container)
        layout.addWidget(dis_ori_container)
        layout.addWidget(deriv_container)
        layout.addWidget(commer_container)
        layout.addWidget(restart_button)
        self.setLayout(layout)

        # load saved settings
        SettingsOptions.load()
        # set the current values
        self.img_res_combo.setCurrentIndex(
            list(image_res_options.values()).index(tuple(SettingsOptions.image_res))
        )
        self.vid_res_combo.setCurrentIndex(
            list(video_res_options.values()).index(tuple(SettingsOptions.video_res))
        )
        self.auto_upload_images.setChecked(SettingsOptions.auto_upload_images)
        self.auto_upload_videos.setChecked(SettingsOptions.auto_upload_videos)
        self.cam_ori_combo.setCurrentIndex(
            camera_orientation_options.index(SettingsOptions.camera_orientation)
        )
        self.dis_ori_combo.setCurrentIndex(
            display_orientation_options.index(SettingsOptions.display_orientation)
        )

    def derivation_changed(self):
        SettingsOptions.derivation = self.deriv_combo.currentText()
        SettingsOptions.save()

    def commercial_changed(self):
        SettingsOptions.commercial_use = self.commer_combo.currentText()
        SettingsOptions.save()

    def display_orientation_changed(self):
        SettingsOptions.display_orientation = self.dis_ori_combo.currentText()
        SettingsOptions.save()

    def camera_orientation_changed(self):
        SettingsOptions.camera_orientation = self.cam_ori_combo.currentText()
        SettingsOptions.save()

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
