"""Color extractor UI - extracts and analyzes colors from image folders."""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QProgressBar,
    QLineEdit, QTextEdit, QFrame, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.rcParams['font.family'] = ['Arial', 'sans-serif']
matplotlib.rcParams['axes.unicode_minus'] = False

from ..core.color_extractor import ColorExtractor
from ..visualization.color_card import ColorCardGenerator, format_color_data


class ColorExtractorWindow(QMainWindow):
    """Window for extracting colors from multiple images."""

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Color Extractor")
        self.setGeometry(100, 100, 700, 900)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Image Folder:"))
        self.folder_input = QLineEdit()
        self.folder_input.setReadOnly(True)
        folder_layout.addWidget(self.folder_input)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Number of colors
        colors_layout = QHBoxLayout()
        colors_layout.addWidget(QLabel("Number of Colors:"))
        self.colors_input = QLineEdit("18")
        self.colors_input.setFixedWidth(100)
        colors_layout.addWidget(self.colors_input)
        colors_layout.addStretch()
        layout.addLayout(colors_layout)

        # Analyze button
        self.analyze_btn = QPushButton("Analyze Images")
        self.analyze_btn.clicked.connect(self.analyze_images)
        layout.addWidget(self.analyze_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Chart frame
        self.chart_frame = QFrame()
        self.chart_layout = QVBoxLayout(self.chart_frame)
        layout.addWidget(self.chart_frame)

        # Results text
        layout.addWidget(QLabel("Color Data:"))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(200)
        layout.addWidget(self.result_text)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.image_folder = folder
            self.folder_input.setText(folder)

    def analyze_images(self):
        if not self.image_folder:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")
            return

        try:
            n_colors = int(self.colors_input.text())
        except ValueError:
            n_colors = 18

        self.progress_bar.setValue(30)

        extractor = ColorExtractor(n_colors=n_colors)
        colors, percentages = extractor.extract_from_folder(self.image_folder)

        if colors.size == 0:
            QMessageBox.warning(self, "Warning", "No valid images found.")
            return

        self.progress_bar.setValue(70)

        # Create chart
        card_gen = ColorCardGenerator()
        fig = card_gen.create_bar_chart(colors, percentages)

        # Clear previous canvas
        if self.canvas:
            self.chart_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(self.canvas)
        self.canvas.draw()

        # Display color data
        self.result_text.setText(format_color_data(colors, percentages))

        self.progress_bar.setValue(100)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ColorExtractorWindow()
    window.show()
    sys.exit(app.exec_())
