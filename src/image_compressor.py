import sys
import cv2
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QSlider, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt

class ImageCompressor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片压缩工具")

        # 显示图片的 QLabel
        self.image_label = QLabel("请选择一张图片")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid gray; min-height: 200px;")

        # 上传和压缩按钮
        self.upload_button = QPushButton("上传图片")
        self.compress_button = QPushButton("压缩图片")
        self.compress_button.setEnabled(False)  # 默认禁用压缩按钮

        # 压缩质量滑动条
        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(50)  # 默认压缩质量为50
        self.quality_slider.setTickInterval(10)
        self.quality_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        # 布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.upload_button)
        button_layout.addWidget(self.compress_button)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.quality_slider)
        self.setLayout(layout)

        # 当前图片的文件路径
        self.image_path = None
        self.original_image = None  # 用于保存原始图像数据

        # 按钮事件绑定
        self.upload_button.clicked.connect(self.upload_image)
        self.compress_button.clicked.connect(self.compress_image)

    def upload_image(self):
        # 打开文件对话框选择图片
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        if file_dialog.exec():
            self.image_path = file_dialog.selectedFiles()[0]
            # 使用 OpenCV 加载图片
            self.original_image = cv2.imread(self.image_path)
            if self.original_image is None:
                self.image_label.setText("无法加载图片，请选择有效图片")
                self.compress_button.setEnabled(False)
                return

            # 显示图片
            self.display_image(self.original_image)
            self.compress_button.setEnabled(True)  # 启用压缩按钮

    def display_image(self, image):
        # 检查是否有透明通道 (Alpha 通道)
        if image.shape[-1] == 4:  # BGRA 格式
            # 转换为 RGBA 格式
            image_rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
            height, width, channels = image_rgba.shape
            bytes_per_line = channels * width
            q_image = QImage(image_rgba.data, width, height, bytes_per_line, QImage.Format.Format_RGBA8888)
        else:
            # 如果没有透明通道，转换为 RGB 格式
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channels = image_rgb.shape
            bytes_per_line = channels * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)

        # 设置图片到 QLabel
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def compress_image(self):
        # 确保图像已加载
        if self.original_image is None:
            self.image_label.setText("没有加载有效图片")
            return

        # 获取压缩质量（通过滑动条）
        quality = self.quality_slider.value()

        # 打开文件保存对话框选择压缩后的文件路径
        save_path, _ = QFileDialog.getSaveFileName(self, "保存压缩图片", "", "JPEG (*.jpg);;PNG (*.png)")
        if save_path:
            if save_path.endswith(".jpg"):
                # 保存为JPEG格式
                success = cv2.imwrite(save_path, self.original_image, [cv2.IMWRITE_JPEG_QUALITY, quality])
                if not success:
                    self.image_label.setText("保存失败，请检查文件路径和权限")
                    return
            elif save_path.endswith(".png"):
                # 保存为PNG格式
                success = cv2.imwrite(save_path, self.original_image, [cv2.IMWRITE_PNG_COMPRESSION, 3])
                if not success:
                    self.image_label.setText("保存失败，请检查文件路径和权限")
                    return

            self.image_label.setText("图片已成功压缩并保存！")
            self.compress_button.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageCompressor()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec())
