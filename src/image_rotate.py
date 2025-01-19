import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap, QTransform, QPainter
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, \
    QGraphicsPixmapItem, QFileDialog, QGraphicsItem, QHBoxLayout


class ImageRotateApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("旋转图像应用")

        # 初始化图片
        self.image = None

        # 主布局
        layout = QVBoxLayout(self)

        # 创建 QGraphicsView 和 QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.view.setFixedSize(600, 400)  # 设置固定视图大小
        layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)

        button_layout = QHBoxLayout()
        # 上传图片按钮
        self.upload_button = QPushButton("上传图片")
        self.upload_button.clicked.connect(self.upload_image)
        button_layout.addWidget(self.upload_button)

        # 旋转按钮
        self.rotate_button = QPushButton("旋转 90°")
        self.rotate_button.clicked.connect(self.rotate_image)
        button_layout.addWidget(self.rotate_button)

        # 保存按钮
        self.save_button = QPushButton("保存图片")
        self.save_button.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_button)
        layout.addLayout(button_layout)

    def upload_image(self):
        """上传并显示图片"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = QImage(file_path)
            self.display_image()

    def display_image(self):
        """显示加载的图片，并按比例缩放"""
        if self.image:

            # 获取 QGraphicsView 的固定大小
            view_width = self.view.width()
            view_height = self.view.height()

            # 等比例缩放图片
            scaled_image = self.image.scaled(view_width, view_height, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)
            # 创建 QGraphicsPixmapItem 并添加到场景
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()  # 清空场景
            self.scene.addItem(pixmap_item)  # 添加图片到场景

    def rotate_image(self):
        """旋转图像 90 度"""
        if self.image:
            transform = QTransform()
            transform.rotate(90)
            rotated_image = self.image.transformed(transform)

            # 更新图像
            pixmap = QPixmap.fromImage(rotated_image)

            # 获取 QGraphicsView 的固定大小
            view_width = self.view.width()
            view_height = self.view.height()

            # 等比例缩放图片
            pixmap = pixmap.scaled(view_width, view_height, Qt.AspectRatioMode.KeepAspectRatio)

            # 创建 QGraphicsPixmapItem 并添加到场景
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene.clear()  # 清空场景
            self.scene.addItem(pixmap_item)  # 添加旋转后的图片到场景

            self.image = rotated_image  # 更新原始图像

    def save_image(self):
        """保存旋转后的图片"""
        if self.image:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "Image Files (*.png *.jpg *.bmp)")
            if file_path:
                self.image.save(file_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = ImageRotateApp()
    window.show()

    sys.exit(app.exec())
