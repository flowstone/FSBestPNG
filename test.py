from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QGraphicsView, QGraphicsScene, QGraphicsRectItem, QLineEdit)


class CropTool(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图像裁剪工具")
        self.setGeometry(100, 100, 800, 600)

        # 主布局
        main_layout = QHBoxLayout(self)

        # 左侧裁剪区域 (透明背景和蓝色边框)
        self.image_area = QGraphicsView()
        self.image_area.setRenderHint(QPainter.Antialiasing)
        self.image_area.setRenderHint(QPainter.SmoothPixmapTransform)
        self.image_area.setBackgroundBrush(QColor(240, 240, 240))  # 可以设置棋盘格背景
        self.scene = QGraphicsScene(self)
        self.image_area.setScene(self.scene)
        main_layout.addWidget(self.image_area)

        # 右侧参数和预览区域
        right_layout = QVBoxLayout()

        # 预览区域
        self.preview_label = QLabel("预览区域")
        self.preview_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.preview_label)

        # 参数设置区域
        self.param_layout = QVBoxLayout()

        self.x_input = QLineEdit("-3px")
        self.y_input = QLineEdit("-1px")
        self.width_input = QLineEdit("3px")
        self.height_input = QLineEdit("3px")
        self.rotate_input = QLineEdit("0度")
        self.scale_x_input = QLineEdit("1")
        self.scale_y_input = QLineEdit("1")

        self.param_layout.addWidget(QLabel("X:"))
        self.param_layout.addWidget(self.x_input)
        self.param_layout.addWidget(QLabel("Y:"))
        self.param_layout.addWidget(self.y_input)
        self.param_layout.addWidget(QLabel("Width:"))
        self.param_layout.addWidget(self.width_input)
        self.param_layout.addWidget(QLabel("Height:"))
        self.param_layout.addWidget(self.height_input)
        self.param_layout.addWidget(QLabel("Rotate:"))
        self.param_layout.addWidget(self.rotate_input)
        self.param_layout.addWidget(QLabel("Scale X:"))
        self.param_layout.addWidget(self.scale_x_input)
        self.param_layout.addWidget(QLabel("Scale Y:"))
        self.param_layout.addWidget(self.scale_y_input)

        right_layout.addLayout(self.param_layout)

        # 操作按钮
        buttons_layout = QVBoxLayout()
        self.zoom_in_button = QPushButton("放大")
        self.zoom_out_button = QPushButton("缩小")
        self.move_left_button = QPushButton("左移")
        self.move_right_button = QPushButton("右移")
        self.move_up_button = QPushButton("上移")
        self.move_down_button = QPushButton("下移")
        self.rotate_left_button = QPushButton("左旋")
        self.rotate_right_button = QPushButton("右旋")

        buttons_layout.addWidget(self.zoom_in_button)
        buttons_layout.addWidget(self.zoom_out_button)
        buttons_layout.addWidget(self.move_left_button)
        buttons_layout.addWidget(self.move_right_button)
        buttons_layout.addWidget(self.move_up_button)
        buttons_layout.addWidget(self.move_down_button)
        buttons_layout.addWidget(self.rotate_left_button)
        buttons_layout.addWidget(self.rotate_right_button)

        right_layout.addLayout(buttons_layout)

        # 提交按钮
        self.submit_button = QPushButton("提交")
        right_layout.addWidget(self.submit_button)

        main_layout.addLayout(right_layout)

        # 设定裁剪区域
        self.crop_area = QGraphicsRectItem(50, 50, 200, 200)
        self.crop_area.setPen(QColor(0, 0, 255))  # 蓝色边框
        self.scene.addItem(self.crop_area)

    def update_crop_area(self):
        # 更新裁剪区域的参数
        x = int(self.x_input.text().replace("px", ""))
        y = int(self.y_input.text().replace("px", ""))
        width = int(self.width_input.text().replace("px", ""))
        height = int(self.height_input.text().replace("px", ""))
        rotate = int(self.rotate_input.text().replace("度", ""))
        scale_x = float(self.scale_x_input.text())
        scale_y = float(self.scale_y_input.text())

        # 更新裁剪区域的位置、大小、旋转和缩放
        self.crop_area.setRect(x, y, width, height)
        self.crop_area.setRotation(rotate)
        self.crop_area.setScale(scale_x)


if __name__ == "__main__":
    app = QApplication([])

    window = CropTool()
    window.show()

    app.exec()
