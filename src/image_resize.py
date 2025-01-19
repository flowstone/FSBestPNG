import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QPainter
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QGraphicsView,
    QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QSlider, QLabel
)

class ImageResizeApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("图片等比例缩放应用")

        # 初始化图片
        self.image = None
        self.original_image = None  # 保存原始 QImage

        # 主布局
        layout = QVBoxLayout(self)

        # 创建 QGraphicsView 和 QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.view.setFixedSize(600, 400)  # 设置固定视图大小
        layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)

        # 水平布局，放置上传和保存按钮
        button_layout = QHBoxLayout()
        self.upload_button = QPushButton("上传图片")
        self.upload_button.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_button)

        self.save_button = QPushButton("保存图片")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)  # 初始禁用保存按钮
        button_layout.addWidget(self.save_button)


        # 缩小比例滑块
        self.scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.scale_slider.setRange(10, 100)  # 缩放范围为 10% 到 100%
        self.scale_slider.setValue(100)  # 默认值为 100%（不缩放）
        self.scale_slider.valueChanged.connect(self.scale_image)
        layout.addWidget(self.scale_slider)
        layout.addLayout(button_layout)

        # 显示当前比例的标签
        self.scale_label = QLabel("当前比例: 100%")
        layout.addWidget(self.scale_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def upload_image(self):
        """上传并显示图片"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = QImage(file_path)
            self.original_image = self.image.copy()  # 保存原始图片
            self.display_image()
            self.save_button.setEnabled(True)  # 启用保存按钮

    def display_image(self, scale=1.0):
        """按比例显示图片"""
        if self.original_image:
            # 获取 QGraphicsView 的固定大小
            view_width = self.view.width()
            view_height = self.view.height()

            # 按比例缩放图片
            scaled_image = self.original_image.scaled(
                view_width * scale,
                view_height * scale,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # 转换为 QPixmap 并显示在 QGraphicsView 中
            pixmap = QPixmap.fromImage(scaled_image)
            self.scene.clear()  # 清空场景
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(pixmap_item)

            # 调整视图以适应场景
            self.view.setSceneRect(self.scene.sceneRect())

    def scale_image(self):
        """根据滑块值动态缩小图片"""
        if self.original_image:
            scale_percentage = self.scale_slider.value()  # 获取滑块的值
            self.scale_label.setText(f"当前比例: {scale_percentage}%")  # 更新比例显示
            scale_factor = scale_percentage / 100.0  # 转换为缩放比例
            self.display_image(scale_factor)  # 显示按比例缩小的图片

    def save_image(self):
        """保存当前显示的图片"""
        if self.original_image:
            # 打开保存文件对话框
            file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Image Files (*.png *.jpg *.bmp)")
            if file_path:
                # 获取滑块当前比例，按比例保存缩放后的图片
                scale_factor = self.scale_slider.value() / 100.0
                scaled_image = self.original_image.scaled(
                    self.original_image.width() * scale_factor,
                    self.original_image.height() * scale_factor,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                scaled_image.save(file_path)  # 保存图片


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ImageResizeApp()
    window.show()

    sys.exit(app.exec())
