"""Palette generator UI - generates color cards from images."""

import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QProgressBar,
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt

from ..core.color_extractor import ColorExtractor
from ..visualization.color_card import ColorCardGenerator


class PaletteGeneratorWindow(QMainWindow):
    """Window for generating color palettes from images."""

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.output_folder = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Palette Generator")
        self.setGeometry(100, 100, 600, 350)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Image folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Image Folder:"))
        self.folder_input = QLineEdit()
        self.folder_input.setReadOnly(True)
        folder_layout.addWidget(self.folder_input)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_image_folder)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Output folder selection
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Folder:"))
        self.output_input = QLineEdit()
        self.output_input.setReadOnly(True)
        output_layout.addWidget(self.output_input)
        output_btn = QPushButton("Browse")
        output_btn.clicked.connect(self.select_output_folder)
        output_layout.addWidget(output_btn)
        layout.addLayout(output_layout)

        # Gray threshold
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Gray Threshold:"))
        self.threshold_input = QLineEdit("1")
        self.threshold_input.setFixedWidth(100)
        threshold_layout.addWidget(self.threshold_input)
        threshold_layout.addStretch()
        layout.addLayout(threshold_layout)

        # Number of colors
        colors_layout = QHBoxLayout()
        colors_layout.addWidget(QLabel("Number of Colors:"))
        self.colors_input = QLineEdit("8")
        self.colors_input.setFixedWidth(100)
        colors_layout.addWidget(self.colors_input)
        colors_layout.addStretch()
        layout.addLayout(colors_layout)

        # Generate button
        self.generate_btn = QPushButton("Generate Palettes")
        self.generate_btn.clicked.connect(self.generate_palettes)
        layout.addWidget(self.generate_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def select_image_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.image_folder = folder
            self.folder_input.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_input.setText(folder)

    def generate_palettes(self):
        if not self.image_folder or not self.output_folder:
            QMessageBox.warning(self, "Warning", "Please select both folders.")
            return

        try:
            n_colors = int(self.colors_input.text())
            gray_threshold = int(self.threshold_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid number input.")
            return

        os.makedirs(self.output_folder, exist_ok=True)

        extractor = ColorExtractor(n_colors=n_colors, gray_threshold=gray_threshold)
        card_gen = ColorCardGenerator()

        def progress_callback(current, total, filename):
            progress = int((current / total) * 100)
            self.progress_bar.setValue(progress)
            self.status_label.setText(f"Processing: {filename}")

        results = extractor.extract_per_image(
            self.image_folder,
            progress_callback=progress_callback
        )

        for filename, colors, percentages in results:
            name = os.path.splitext(filename)[0]
            output_path = os.path.join(self.output_folder, f"{name}.png")
            card_gen.save_card(colors, percentages, output_path)

        self.progress_bar.setValue(100)
        self.status_label.setText(f"Completed! Generated {len(results)} palettes.")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = PaletteGeneratorWindow()
    window.show()
    sys.exit(app.exec_())
