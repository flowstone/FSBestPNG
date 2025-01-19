from PySide6.QtGui import QIcon
from loguru import logger
import os
from PIL import Image, ImageEnhance
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox,
    QComboBox, QSpinBox
)
from PySide6.QtCore import Qt, QThread, Signal

from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar


def process_single_image(image_path, watermark, position, transparency, scale, output_folder):
    try:
        image = Image.open(image_path).convert("RGBA")

        # 缩放水印
        original_size = watermark.size
        scaled_size = (int(original_size[0] * scale / 100), int(original_size[1] * scale / 100))
        watermark_resized = watermark.resize(scaled_size, Image.Resampling.LANCZOS)

        # 设置透明度
        alpha = watermark_resized.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(transparency / 100.0)
        watermark_resized.putalpha(alpha)

        # 计算水印位置
        position_cords = (0, 0)
        image_width, image_height = image.size
        watermark_width, watermark_height = watermark_resized.size
        if position == "左上角":
            position_cords = (0, 0)
        elif position == "右上角":
            position_cords = (image_width - watermark_width, 0)
        elif position == "左下角":
            position_cords = (0, image_height - watermark_height)
        elif position == "右下角":
            position_cords = (image_width - watermark_width, image_height - watermark_height)

        # 添加水印
        image.paste(watermark_resized, position_cords, mask=watermark_resized)
        output_path = os.path.join(output_folder, os.path.basename(image_path))
        image.save(output_path, 'PNG')
    except Exception as e:
        logger.error(f"{e}")
        raise e


class WatermarkWorker(QThread):
    progress = Signal(int)
    completed = Signal()
    error = Signal(str)

    def __init__(self, input_folder, watermark_path, output_folder, position, transparency, scale):
        super().__init__()
        self.input_folder = input_folder
        self.watermark_path = watermark_path
        self.output_folder = output_folder
        self.position = position
        self.transparency = transparency
        self.scale = scale

    def run(self):
        try:
            watermark = Image.open(self.watermark_path).convert("RGBA")
            images = [f for f in os.listdir(self.input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
            total_images = len(images)

            for idx, filename in enumerate(images):
                image_path = os.path.join(self.input_folder, filename)
                process_single_image(image_path, watermark, self.position, self.transparency, self.scale,
                                     self.output_folder)
                self.progress.emit(int((idx + 1) / total_images * 100))  # 更新进度
            self.completed.emit()
        except Exception as e:
            self.error.emit(str(e))


class BatchWatermarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("批量添加水印")
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.worker = None

        # Input folder
        self.input_label = QLabel("输入文件夹路径:")
        self.input_edit = QLineEdit()
        self.input_button = QPushButton("选择")
        self.input_button.clicked.connect(self.select_input_folder)

        # Watermark path
        self.watermark_label = QLabel("水印文件路径:")
        self.watermark_edit = QLineEdit()
        self.watermark_button = QPushButton("选择")
        self.watermark_button.clicked.connect(self.select_watermark_file)

        # Output folder
        self.output_label = QLabel("输出文件夹路径:")
        self.output_edit = QLineEdit()
        self.output_button = QPushButton("选择")
        self.output_button.clicked.connect(self.select_output_folder)

        # Watermark position
        self.position_label = QLabel("水印位置:")
        self.position_combo = QComboBox()
        self.position_combo.addItems(["左上角", "右上角", "左下角", "右下角"])

        # Transparency
        self.transparency_label = QLabel("透明度(%):")
        self.transparency_spinbox = QSpinBox()
        self.transparency_spinbox.setRange(0, 100)
        self.transparency_spinbox.setValue(100)

        # Scale
        self.scale_label = QLabel("水印缩放比例(%):")
        self.scale_spinbox = QSpinBox()
        self.scale_spinbox.setRange(10, 300)
        self.scale_spinbox.setValue(100)

        # Progress bar
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()


        # Process button
        self.process_button = QPushButton("开始处理")
        self.process_button.clicked.connect(self.process_images)

        # Layout
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(self.input_button)

        watermark_layout = QHBoxLayout()
        watermark_layout.addWidget(self.watermark_label)
        watermark_layout.addWidget(self.watermark_edit)
        watermark_layout.addWidget(self.watermark_button)

        output_layout = QHBoxLayout()
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(self.output_button)

        position_layout = QHBoxLayout()
        position_layout.addWidget(self.position_label)
        position_layout.addWidget(self.position_combo)

        transparency_layout = QHBoxLayout()
        transparency_layout.addWidget(self.transparency_label)
        transparency_layout.addWidget(self.transparency_spinbox)

        scale_layout = QHBoxLayout()
        scale_layout.addWidget(self.scale_label)
        scale_layout.addWidget(self.scale_spinbox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.process_button)
        layout.addLayout(input_layout)
        layout.addLayout(watermark_layout)
        layout.addLayout(output_layout)
        layout.addLayout(transparency_layout)
        layout.addLayout(scale_layout)
        layout.addLayout(position_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输入文件夹")
        if folder:
            self.input_edit.setText(folder)

    def select_watermark_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择水印文件", filter="Images (*.png *.jpg *.jpeg)")
        if file:
            self.watermark_edit.setText(file)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if folder:
            self.output_edit.setText(folder)

    def process_images(self):
        input_folder = self.input_edit.text()
        watermark_path = self.watermark_edit.text()
        output_folder = self.output_edit.text()
        position = self.position_combo.currentText()
        transparency = self.transparency_spinbox.value()
        scale = self.scale_spinbox.value()

        if not input_folder or not watermark_path or not output_folder:
            MessageUtil.show_warning_message("请填写所有路径！")
            return
        # 初始化线程
        self.worker = WatermarkWorker(input_folder, watermark_path, output_folder, position, transparency, scale)
        self.worker.progress.connect(self.progress_bar.update_progress)
        self.worker.completed.connect(self.on_completed)
        self.worker.error.connect(self.on_error)
        self.worker.start()
        self.progress_bar.show()

        self.process_button.setEnabled(False)



    def on_completed(self):
        self.process_button.setEnabled(True)
        self.progress_bar.hide()
        MessageUtil.show_success_message("所有图片已成功添加水印！")

    def on_error(self, error_message):
        self.process_button.setEnabled(True)
        self.progress_bar.hide()
        MessageUtil.show_error_message(f"处理过程中出现错误：\n{error_message}")


if __name__ == "__main__":
    app = QApplication([])
    window = BatchWatermarkApp()
    window.show()
    app.exec()
