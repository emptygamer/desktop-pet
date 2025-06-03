import os
import sys
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import QApplication, QWidget, QLabel
from typing import Literal
from pathlib import Path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class SequenceData():
    def __init__(self, files, type:Literal["image", "gif"] = "image", imageTimerMS=100) -> None:
        self.files = []
        self.type = type
        self.imageTimerMS = imageTimerMS
        # Convert file paths
        for f in files:
            self.files.append(resource_path(f))
        print(self.files)
        if not type in ["image","gif"]:
            raise Exception("類別需要是 image 或 gif。")
        if len(self.files) == 0:
            raise Exception("請提供動畫檔案。")
        if type == "image":
            for f in self.files:
                if not (os.path.exists(f)):
                    raise Exception(f"圖片:{f}不存在。")
                if not (Path(f).suffix.lower() in [".png", ".jpg", ".jpeg"]):
                    raise Exception("圖片檔案必須為 .png 或 .jpg/.jpeg。")
        elif type == "video":
            if not (os.path.exists(self.files[0])):
                raise Exception(f"圖片:{f}不存在。")
            if not (Path(self.files[0]).suffix.lower() in [".mp4", ".gif"]):
                raise Exception("影像檔案必須為 .mp4 或 .gif。")

class DesktopPet(QWidget):
    def __init__(self, sequenceData:SequenceData):
        super().__init__()
        self.sequenceData = sequenceData
        self.current_frame = 0
        self.pet_images = []
        self.movie = None
        self.label = QLabel(self)
        self.init()

    def init(self):
        # 設定無窗、釘選在畫面上
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # 設置圖片
        if self.sequenceData.type == "image":
            for f in self.sequenceData.files:
                self.pet_images.append(QPixmap(f))
            self.label.setPixmap(self.pet_images[self.current_frame])
            self.label.resize(self.pet_images[self.current_frame].size())
        elif self.sequenceData.type == "gif":
            print(self.sequenceData.files[0])
            self.movie = QMovie(self.sequenceData.files[0])
            self.label.setMovie(self.movie)
            self.movie.start()
            self.movie.frameChanged.connect(self.resizeToMovie)

        # 動畫切換
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(self.sequenceData.imageTimerMS)

        # 拖拉用的位置
        self.drag_position = QPoint()

    def resizeToMovie(self):
        self.label.resize(self.movie.currentPixmap().size())
        self.resize(self.movie.currentPixmap().size())

    def updateAnimation(self):
        if self.sequenceData.type=="image":
            self.current_frame = (self.current_frame + 1) % len(self.sequenceData.files)
            self.label.setPixmap(self.pet_images[self.current_frame])
            self.label.resize(self.pet_images[self.current_frame].size())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        sequenceData = SequenceData(["./frames/my.gif"],"gif")
        # sequenceData = SequenceData([
        #     "./frames/1.png",
        #     "./frames/2.png",
        #     "./frames/3.png",
        #     "./frames/4.png",
        #     "./frames/5.png",
        # ],"image",100)
        pet = DesktopPet(sequenceData)
        pet.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
    