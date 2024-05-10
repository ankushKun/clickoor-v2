from curses import halfdelay
import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from picamera2.previews.qt import QGlPicamera2
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from libcamera import controls, Transform

from gpiozero import Button

from datetime import datetime
from calendar import timegm

# Picamera log level
# 0 - DEBUG
# 1 - INFO
# 2 - WARN
# 3 - ERROR
# 4 - FATAL
os.environ["LIBCAMERA_LOG_LEVELS"] = "2"

# 640,480 = 1.333
# 1920,1080 = 1.777
# 360


class CameraScreen(QWidget):

    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)
        self.camera = Picamera2()
        self.shutter = Button(5, bounce_time=0.15)
        self.shutter.when_pressed = self.shutter_clicked
        self.preview_config = self.camera.create_preview_configuration(
            main={"size": (1920, 1080)}, transform=Transform(vflip=True)
        )
        self.capture_config = self.camera.create_still_configuration(
            main={"size": (1920, 1080)},
            raw={"size": self.camera.sensor_resolution},
            transform=Transform(vflip=True),
        )
        self.video_config = self.camera.create_video_configuration(
            main={"size": (1280, 720)}, transform=Transform(vflip=True)
        )
        self.camera.configure(self.preview_config)
        self.camera.set_controls(
            {
                "AfMode": controls.AfModeEnum.Continuous,
                "AfSpeed": controls.AfSpeedEnum.Fast,
            }
        )

        preview_widget = QGlPicamera2(
            self.camera, self, keep_ar=True, width=640, height=360
        )
        preview_widget.done_signal.connect(self.captured)
        preview_widget.showFullScreen()
        preview_widget.setGeometry(0, 0, 640, 360)
        self.preview_widget = preview_widget

        # viewframe = QLabel(self)
        # viewframe.show()
        # pix = QPixmap("assets/frame.png")
        # pix.setMask(QBitmap("assets/frame.mask.png", "png"))
        # viewframe.setPixmap(pix)
        # viewframe.resize(640, 300)
        # QLabel.setStyleSheet(viewframe, "background-color: transparent;")
        # viewframe.showFullScreen()

        # stack = QStackedWidget(self)
        # stack.addWidget(viewframe)
        # stack.addWidget(self.preview_widget)

        mode_btn = QPushButton(self)
        mode_btn.setText("video")
        mode_btn.clicked.connect(self.switch_mode)
        # mode_btn.setFixedSize(50, 50)
        mode_btn.setFixedHeight(50)
        mode_btn.showFullScreen()
        mode_btn.setIcon(QIcon("./assets/record_stopped.png"))
        mode_btn.setIconSize(QSize(25, 25))
        mode_btn.setStyleSheet("background-color:transparent")
        mode_btn.setFlat(True)
        self.mode_btn = mode_btn

        capture_btn = QPushButton(self)
        capture_btn.clicked.connect(self.shutter_clicked)
        capture_btn.setFixedSize(50, 50)
        capture_btn.showFullScreen()
        capture_btn.setIcon(QIcon("./assets/shutter.png"))
        capture_btn.setIconSize(QSize(50, 50))
        capture_btn.setStyleSheet("background-color:transparent")
        capture_btn.setFlat(True)
        self.capture_btn = capture_btn

        # settings_btn = QPushButton("Settings", self)
        # settings_btn.clicked.connect(self.open_settings)
        # settings_btn.setFixedSize(50, 50)
        # settings_btn.showFullScreen()
        # self.settings_btn = settings_btn

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        hlayout.setContentsMargins(0, 0, 0, 5)

        hlayout.addWidget(self.mode_btn)
        hlayout.addWidget(self.capture_btn)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # self.setStyleSheet("background-color:transparent")

        # vlayout.addWidget(stack)
        vlayout.addLayout(hlayout)
        vlayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(vlayout)

        self.camera.start()

        self.video_mode = False
        self.capturing_video = False

    def shutter_clicked(self):
        if self.video_mode:
            self.toggle_video()
        else:
            self.capture_image()

    def capture_image(self):
        print("Capturing image")
        ts = datetime.now()
        ts = timegm(ts.utctimetuple())
        self.last_filename = f"captures/IMG_{ts}.png"
        self.capture_btn.setEnabled(False)
        self.preview_widget.setVisible(False)
        self.camera.switch_mode_and_capture_file(
            self.capture_config,
            self.last_filename,
            signal_function=self.preview_widget.signal_done,
        )

    def captured(self, job):
        self.camera.wait(job)
        self.preview_widget.setVisible(True)
        self.capture_btn.setEnabled(True)
        print("Captured")

    def switch_mode(self):
        self.video_mode = not self.video_mode
        if self.video_mode:
            self.camera.stop()
            self.camera.configure(self.video_config)
            self.mode_btn.setIcon(QIcon("assets/shutter.png"))
            self.capture_btn.setIcon(QIcon("assets/record_stopped.png"))
            self.mode_btn.setText("photo")
            self.camera.start()
        else:
            self.camera.stop()
            self.camera.configure(self.preview_config)
            self.mode_btn.setIcon(QIcon("assets/record_stopped.png"))
            self.capture_btn.setIcon(QIcon("assets/shutter.png"))
            self.mode_btn.setText("video")
            self.camera.start()

    def toggle_video(self):
        if not self.video_mode:
            return
        if self.capturing_video:
            self.capture_btn.setIcon(QIcon("assets/record_stopped.png"))
            self.camera.stop_recording()
            self.camera.configure(self.video_config)
            self.camera.start()
        else:
            print("Capturing video")
            ts = datetime.now()
            ts = timegm(ts.utctimetuple())
            self.last_filename = f"captures/VID_{ts}.mp4"
            self.capture_btn.setIcon(QIcon("assets/record_started.png"))

            self.camera.stop()
            encoder = H264Encoder(5000000, framerate=24)
            output = FfmpegOutput(self.last_filename)
            self.camera.configure(self.video_config)
            self.camera.start_recording(encoder, output)
        self.capturing_video = not self.capturing_video
