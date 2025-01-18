import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QSlider, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget
)
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtCore import Qt, QRect

class ImageEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像编辑器")
        self.setGeometry(100, 100, 800, 600)

        # 图像存储
        self.image = None
        self.processed_image = None

        # 裁剪相关变量
        self.is_cropping = False
        self.start_point = None
        self.end_point = None
        self.selection_rect = None

        # UI 初始化
        self.init_ui()

    def init_ui(self):
        # 主布局
        layout = QVBoxLayout()

        # 图像显示区域
        self.image_label = QLabel("加载图片以开始编辑")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(600, 400)  # 设置固定宽高
        self.image_label.setStyleSheet("border: 1px solid black;")  # 添加边框
        layout.addWidget(self.image_label)

        # 按钮区域
        button_layout = QHBoxLayout()

        load_button = QPushButton("加载图片")
        load_button.clicked.connect(self.load_image)
        button_layout.addWidget(load_button)

        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_image)
        button_layout.addWidget(reset_button)

        crop_button = QPushButton("裁剪")
        crop_button.clicked.connect(self.enable_cropping)
        button_layout.addWidget(crop_button)

        save_button = QPushButton("保存图片")
        save_button.clicked.connect(self.save_image)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

        # 设置中心窗口
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.processed_image = self.image.copy()
            self.display_image()

    def reset_image(self):
        """将图片重置为原始状态"""
        if self.image is not None:
            self.processed_image = self.image.copy()
            self.display_image()

    def display_image(self):
        """将处理后的图像显示在 QLabel 中"""
        if self.processed_image is not None:
            # 确保内存连续
            contiguous_image = np.ascontiguousarray(self.processed_image)
            height, width, channel = contiguous_image.shape
            bytes_per_line = 3 * width

            # 创建 QImage
            q_image = QImage(
                contiguous_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888
            ).rgbSwapped()
            pixmap = QPixmap.fromImage(q_image)

            # 将图像缩放以适应 QLabel 区域
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)

    def enable_cropping(self):
        """启用裁剪功能"""
        if self.processed_image is not None:
            self.is_cropping = True

    def crop_image(self):
        """根据选择的区域裁剪图像"""
        if self.selection_rect and self.processed_image is not None:
            # QLabel 的宽高
            label_width = self.image_label.width()
            label_height = self.image_label.height()

            # 图像的宽高
            height, width, _ = self.processed_image.shape

            # 计算缩放比例
            scale_w = width / label_width
            scale_h = height / label_height

            # 将裁剪区域映射到原始图像尺寸
            x1 = int(self.selection_rect.x() * scale_w)
            y1 = int(self.selection_rect.y() * scale_h)
            x2 = int((self.selection_rect.x() + self.selection_rect.width()) * scale_w)
            y2 = int((self.selection_rect.y() + self.selection_rect.height()) * scale_h)

            # 确保坐标合法
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(width, x2), min(height, y2)

            # 裁剪图像
            self.processed_image = self.processed_image[y1:y2, x1:x2]
            self.display_image()

            # 重置裁剪相关变量
            self.is_cropping = False
            self.start_point = None
            self.end_point = None
            self.selection_rect = None

    def save_image(self):
        """保存图像到文件"""
        if self.processed_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Images (*.png *.jpg *.bmp)")
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                print("图片已保存:", file_path)

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if self.is_cropping and event.button() == Qt.MouseButton.LeftButton:
            # 获取鼠标在 QLabel 中的局部坐标
            pos = self.image_label.mapFromParent(event.position().toPoint())
            if self.image_label.pixmap() and self.image_label.pixmap().rect().contains(pos):
                self.start_point = pos

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.is_cropping and self.start_point:
            # 获取鼠标在 QLabel 中的局部坐标
            pos = self.image_label.mapFromParent(event.position().toPoint())
            self.end_point = pos
            self.selection_rect = QRect(self.start_point, self.end_point)
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if self.is_cropping and event.button() == Qt.MouseButton.LeftButton:
            self.crop_image()

    def paintEvent(self, event):
        """绘制裁剪区域"""
        super().paintEvent(event)  # 确保其他组件正常绘制

        if self.selection_rect and self.is_cropping:
            if self.processed_image is not None:
                # 在原始图像副本上绘制裁剪框
                temp_image = self.processed_image.copy()
                height, width, channel = temp_image.shape
                bytes_per_line = 3 * width
                q_image = QImage(temp_image.data, width, height, bytes_per_line,
                                 QImage.Format.Format_RGB888).rgbSwapped()
                pixmap = QPixmap.fromImage(q_image)

                # 使用 QPainter 在 Pixmap 上绘制
                painter = QPainter(pixmap)
                painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.PenStyle.DashLine))
                painter.drawRect(self.selection_rect)
                painter.end()

                # 更新 QLabel 显示
                scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
                self.image_label.setPixmap(scaled_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditor()
    editor.show()
    sys.exit(app.exec())
