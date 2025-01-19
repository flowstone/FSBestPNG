import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt, QRect, Signal, QPoint
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QScreen


class ScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("截图工具")
        self.setGeometry(100, 100, 800, 600)

        # 截图显示区域
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)

        # 按钮布局
        self.full_screenshot_btn = QPushButton("全屏截图", self)
        self.full_screenshot_btn.clicked.connect(self.take_full_screenshot)

        self.region_screenshot_btn = QPushButton("区域截图", self)
        self.region_screenshot_btn.clicked.connect(self.start_region_screenshot)

        self.save_screenshot_btn = QPushButton("保存截图", self)
        self.save_screenshot_btn.clicked.connect(self.save_screenshot)

        # 主布局
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.full_screenshot_btn)
        layout.addWidget(self.region_screenshot_btn)
        layout.addWidget(self.save_screenshot_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 截图数据
        self.screenshot = None

    def take_full_screenshot(self):
        """全屏截图"""
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0)  # 截取整个屏幕
        self.screenshot = screenshot.toImage()
        self.display_screenshot()

    def start_region_screenshot(self):
        """启动区域截图模式"""
        self.hide()  # 隐藏主窗口
        self.region_window = RegionCaptureWindow()
        self.region_window.region_selected.connect(self.region_screenshot_taken)
        self.region_window.showFullScreen()

    def region_screenshot_taken(self, image):
        """接收区域截图并显示"""
        self.screenshot = image
        self.display_screenshot()
        self.show()  # 显示主窗口

    def display_screenshot(self):
        """显示截图"""
        if self.screenshot:
            pixmap = QPixmap.fromImage(self.screenshot)
            self.image_label.setPixmap(pixmap)

    def save_screenshot(self):
        """保存截图到文件"""
        if self.screenshot is None:
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存截图", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_path:
            self.screenshot.save(file_path)


class RegionCaptureWindow(QWidget):
    """用于区域截图的窗口"""
    region_selected = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)

        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setCursor(Qt.CrossCursor)  # 鼠标变为十字形
        self.setGeometry(QApplication.primaryScreen().geometry())  # 设置窗口为全屏

        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_selecting = False
        # 设置窗口覆盖所有屏幕
        geometry = QApplication.primaryScreen().geometry()  # 获取多显示器范围
        self.setGeometry(geometry)
        # 获取当前屏幕截图作为背景
        screen = QApplication.primaryScreen()
        self.device_pixel_ratio = screen.devicePixelRatio()
        self.background_pixmap = screen.grabWindow(
            0, geometry.x(), geometry.y(), geometry.width(), geometry.height()
        )

        # 悬浮按钮
        self.copy_button = QPushButton("复制", self)
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_image)
        self.copy_button.hide()
        self.save_button.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.position().toPoint()
            self.is_selecting = True

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.end_point = event.position().toPoint()
            self.update()  # 触发窗口重绘

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.is_selecting = False
            self.capture_region()
            self.close()

    def paintEvent(self, event):
        """绘制半透明背景和红色矩形"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 绘制背景截图
        painter.drawPixmap(self.rect(), self.background_pixmap)

        # 绘制红色矩形
        if self.is_selecting:
            # 绘制半透明遮罩
            painter.fillRect(self.rect(), QColor(0, 0, 0, 100))

            rect = QRect(self.start_point, self.end_point).normalized()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor(255, 0, 0, 200))  # 红色边框
            painter.drawRect(rect)

    def capture_region(self):
        """截取选定区域"""
        rect = QRect(self.start_point, self.end_point).normalized()
        # 考虑 DPI 缩放
        rect = QRect(
            rect.x() * self.device_pixel_ratio,
            rect.y() * self.device_pixel_ratio,
            rect.width() * self.device_pixel_ratio,
            rect.height() * self.device_pixel_ratio,
        )
        self.result_pixmap = self.background_pixmap.copy(rect)
        #self.region_selected.emit(cropped_pixmap.toImage())
        # 显示悬浮按钮
        self.show_buttons()

    def show_buttons(self):
        """显示悬浮按钮"""
        rect = QRect(self.start_point, self.end_point).normalized()
        button_width = 80
        button_height = 30

        # 计算按钮位置
        x = rect.right() - button_width
        y = rect.bottom() + 5

        # 设置按钮位置和大小
        self.copy_button.setGeometry(x - button_width, y, button_width, button_height)
        self.save_button.setGeometry(x, y, button_width, button_height)
        self.copy_button.show()
        self.save_button.show()

    def copy_to_clipboard(self):
        """复制截图到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setPixmap(self.result_pixmap)
        self.close()

    def save_image(self):
        """保存截图到文件"""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "保存截图", "", "PNG Files (*.png);;All Files (*)",
                                                   options=options)
        if file_path:
            self.result_pixmap.toImage().save(file_path)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotTool()
    window.show()
    sys.exit(app.exec())
