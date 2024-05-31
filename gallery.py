import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *

from utils import upload_file


btn_press_style = (
"font-size: 16px;"
    "QPushButton"
    "{"
    "background-color : transparent;"
    "}"
    "QPushButton::pressed"
    "{"
    "background-color : gray;"
    "}"
)


class UploadWorker(QThread):
    uploaded = pyqtSignal(bool)
    uploader = None
    file_handler = None
    progress_bar = None

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            while not self.uploader.is_complete:
                self.progress_bar.show()
                self.uploader.upload_chunk()
                self.progress_bar.setValue(int(self.uploader.pct_complete))
                print(
                    f"{self.uploader.pct_complete}% - {self.uploader.uploaded_chunks}/{self.uploader.total_chunks}"
                )
                if self.uploader.uploaded_chunks == self.uploader.total_chunks:
                    self.progress_bar.hide()
                    self.file_handler.close()
                    print("done")
                    self.uploaded.emit(True)
                    break
        except Exception as e:
            print("upload exception", e)
            self.uploaded.emit(False)




class GalleryScreen(QWidget):

    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)
        self.index = 0
        self.image = QLabel(self)
        self.image.setFixedSize(640, 360)
        self.video = QVideoWidget(self)
        self.video.setFixedSize(640, 360)
        self.video.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.mediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaplayer.setVideoOutput(self.video)
        self.mediaplayer.mediaStatusChanged.connect(self.media_status_changed)
        self.active_screen = False
        self.wallet = None

        self.indicator = QLabel(self)
        self.indicator.setFixedHeight(50)

        self.prev_btn = QPushButton("", self)
        self.prev_btn.setFixedHeight(50)
        self.prev_btn.clicked.connect(self.go_prev)
        self.prev_btn.setStyleSheet(btn_press_style)
        self.prev_btn.setIcon(QIcon("assets/previous.png"))
        self.prev_btn.setIconSize(QSize(40, 40))
        self.prev_btn.setFlat(True)

        self.next_btn = QPushButton("", self)
        self.next_btn.setFixedHeight(50)
        self.next_btn.clicked.connect(self.go_next)
        self.next_btn.setStyleSheet(btn_press_style)
        self.next_btn.setIcon(QIcon("assets/next.png"))
        self.next_btn.setIconSize(QSize(40, 40))
        self.next_btn.setFlat(True)

        self.upload_btn = QPushButton("Permasave", self)
        self.upload_btn.setFixedHeight(50)
        self.upload_btn.setIcon(QIcon("assets/upload.png"))
        self.upload_btn.setIconSize(QSize(40, 40))
        self.upload_btn.setStyleSheet(btn_press_style)
        self.upload_btn.setFlat(True)
        self.upload_btn.clicked.connect(self.upload)

        self.delete_btn = QPushButton("", self)
        self.delete_btn.setFixedHeight(50)
        self.delete_btn.clicked.connect(self.delete_current)
        self.delete_btn.setIcon(QIcon("assets/trash.png"))
        self.delete_btn.setIconSize(QSize(40, 40))
        self.delete_btn.setStyleSheet(btn_press_style)
        self.delete_btn.setFlat(True)

        status_label = QLabel("...", self)
        status_label.setStyleSheet("background-color:black;")
        self.status_label=status_label

        # upload progress bar
        progress_bar = QProgressBar(self)
        # progress_bar.setFixedSize(150, 5)
        progress_bar.setStyleSheet(
            "QProgressBar {border: 2px solid grey; border-radius: 5px; background-color: white;}"
            "QProgressBar::chunk {background-color: #05B8CC;}"
        )
        # progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_bar.showFullScreen()
        progress_bar.hide()
        self.progress_bar = progress_bar





        hlayout = QHBoxLayout()
        hlayout.addWidget(self.indicator)
        hlayout.addWidget(self.prev_btn)
        hlayout.addWidget(self.next_btn)
        hlayout.addWidget(self.upload_btn)
        hlayout.addWidget(self.delete_btn)
        hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        hlayout.setContentsMargins(0, 0, 0, 3)
        vlayout.setContentsMargins(0, 0, 0, 3)

        self.setLayout(vlayout)

        self.update_indicator()
        # if len(self.gallery_files()) > 0:
        #     self.show_media()

    def upload(self):
        if self.wallet:
            self.upload_worker = UploadWorker()
            self.tx, uploader, file_handler = upload_file(self.current_item_path(), self.wallet)
            self.upload_worker.uploaded.connect(self.uploaded)
            self.upload_worker.uploader = uploader
            self.upload_worker.file_handler = file_handler
            self.progress_bar.setValue(0)
            self.upload_worker.progress_bar = self.progress_bar
            self.upload_worker.start()
        else:
            print("no wallet found")

    def uploaded(self,status):
        print("uploaded",status)
        self.status_label.show()
        if status:
            self.status_label.setText(f"Uploaded {self.tx.id}")
        else:
            self.status_label.setText(f"Failed")

        # self.delete_current()




    def set_wallet(self, wallet):
        self.wallet = wallet

    def gallery_files(self):
        f = os.listdir("captures")
        f = list(
            filter(
                lambda x: x.endswith(".jpg")
                or x.endswith(".png")
                or x.endswith(".mp4"),
                f,
            )
        )
        f.sort(key=lambda x: os.path.getmtime(f"captures/{x}"), reverse=True)
        return f

    def current_item_path(self):
        if len(self.gallery_files()) > 0:
            return os.path.abspath("captures/" + f"{self.gallery_files()[self.index]}")
        return ""

    def scale_pixmap(self, pixmap: QPixmap):
        return QPixmap.fromImage(
            QImage.scaled(
                pixmap.toImage(), 640, 360, Qt.AspectRatioMode.KeepAspectRatio
            )
        )

    def update_indicator(self):
        if len(self.gallery_files()) > 0:
            self.indicator.setText(f"{self.index+1}/{len(self.gallery_files())}")
        else:
            self.indicator.setText("No Media")

    def media_status_changed(self, status):
        print(status)
        if status == 7:  # playback complete
            self.mediaplayer.play()  # play again

    def show_media(self):
        self.update_indicator()
        is_video = self.current_item_path().endswith(".mp4")
        if is_video:
            self.image.hide()
            self.mediaplayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.current_item_path()))
            )
            self.video.show()
            self.mediaplayer.play()
        else:
            self.video.hide()
            self.image.show()
            self.image.setPixmap(self.scale_pixmap(QPixmap(self.current_item_path())))

    def goto_start(self):
        self.index = 0
        self.show_media()

    def go_next(self):
        if self.index < len(self.gallery_files()) - 1:
            self.index += 1
            self.show_media()

    def go_prev(self):
        if self.index > 0:
            self.index -= 1
            self.show_media()

    def delete_current(self):
        if len(self.gallery_files()) > 0:
            os.remove(self.current_item_path())
            if len(self.gallery_files()) <= 1:
                self.index = 0
            elif self.index == len(self.gallery_files()):
                self.index -= 1
            self.update_indicator()
            self.show_media()
