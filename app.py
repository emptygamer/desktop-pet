import sys
from PySide2.QtCore import Qt, QTimer, QPoint
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication, QWidget, QLabel

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        # 設定無窗、釘選在畫面上
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 設置圖片
        self.pet_images = [QPixmap(f"./default_frames/frame_{i:04d}.png") for i in range(0, 5)]
        self.current_frame = 0

        # 顯示圖片
        self.label = QLabel(self)
        self.label.setPixmap(self.pet_images[self.current_frame])
        self.label.resize(self.pet_images[self.current_frame].size())
        self.resize(self.pet_images[self.current_frame].size())

        # 動畫切換
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(100)

        # 拖拉用的位置
        self.drag_position = QPoint()

    def updateAnimation(self):
        self.current_frame = (self.current_frame + 1) % len(self.pet_images)
        self.label.setPixmap(self.pet_images[self.current_frame])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec_())