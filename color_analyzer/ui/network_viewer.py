"""Network viewer UI - visualizes color relationships as a network graph."""

import sys
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar, QMessageBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from ..visualization.network_plot import (
    NetworkPlotter, parse_color_input, parse_matrix_input
)


class NetworkViewerWindow(QMainWindow):
    """Window for visualizing color relationship networks."""

    def __init__(self):
        super().__init__()
        self.canvas = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Network Viewer")
        self.setGeometry(100, 100, 800, 900)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Color input
        layout.addWidget(QLabel("Color Data (R G B Size, one per line):"))
        self.color_input = QTextEdit()
        self.color_input.setPlaceholderText(
            "Example:\n"
            "255 0 0 10\n"
            "0 255 0 8\n"
            "0 0 255 12"
        )
        self.color_input.setMaximumHeight(120)
        layout.addWidget(self.color_input)

        # Matrix input
        layout.addWidget(QLabel("Frequency Matrix (space-separated):"))
        self.matrix_input = QTextEdit()
        self.matrix_input.setPlaceholderText(
            "Example:\n"
            "0 5 3\n"
            "5 0 8\n"
            "3 8 0"
        )
        self.matrix_input.setMaximumHeight(120)
        layout.addWidget(self.matrix_input)

        # Threshold inputs
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Base Threshold:"))
        self.base_threshold = QTextEdit("3")
        self.base_threshold.setMaximumHeight(30)
        self.base_threshold.setMaximumWidth(60)
        threshold_layout.addWidget(self.base_threshold)
        threshold_layout.addWidget(QLabel("Highlight Threshold:"))
        self.highlight_threshold = QTextEdit("7")
        self.highlight_threshold.setMaximumHeight(30)
        self.highlight_threshold.setMaximumWidth(60)
        threshold_layout.addWidget(self.highlight_threshold)
        threshold_layout.addStretch()
        layout.addLayout(threshold_layout)

        # Generate button
        self.generate_btn = QPushButton("Generate Network")
        self.generate_btn.clicked.connect(self.generate_network)
        layout.addWidget(self.generate_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Chart area
        self.chart_frame = QWidget()
        self.chart_layout = QVBoxLayout(self.chart_frame)
        layout.addWidget(self.chart_frame)

    def generate_network(self):
        try:
            colors, sizes = parse_color_input(self.color_input.toPlainText())
            matrix = parse_matrix_input(self.matrix_input.toPlainText())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Invalid input: {e}")
            return

        if len(colors) == 0:
            QMessageBox.warning(self, "Warning", "No color data provided.")
            return

        try:
            base_thresh = int(self.base_threshold.toPlainText())
            highlight_thresh = int(self.highlight_threshold.toPlainText())
        except ValueError:
            base_thresh, highlight_thresh = 3, 7

        def progress_callback(current, total):
            self.progress_bar.setValue(int(current / total * 100))

        plotter = NetworkPlotter(
            base_threshold=base_thresh,
            highlight_threshold=highlight_thresh
        )

        fig = plotter.plot(
            colors, sizes, matrix,
            progress_callback=progress_callback
        )

        # Clear previous canvas
        if self.canvas:
            self.chart_layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

        self.canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(self.canvas)
        self.canvas.draw()

        self.progress_bar.setValue(100)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = NetworkViewerWindow()
    window.show()
    sys.exit(app.exec_())
