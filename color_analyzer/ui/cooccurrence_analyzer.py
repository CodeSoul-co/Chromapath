"""Co-occurrence analyzer UI - analyzes color co-occurrence in images."""

import sys
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox
)

from ..core.cooccurrence import CooccurrenceAnalyzer


class CooccurrenceWindow(QMainWindow):
    """Window for analyzing color co-occurrence patterns."""

    def __init__(self):
        super().__init__()
        self.image_folder = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Co-occurrence Analyzer")
        self.setGeometry(100, 100, 700, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Folder selection
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Image Folder:"))
        self.folder_input = QTextEdit()
        self.folder_input.setMaximumHeight(30)
        folder_layout.addWidget(self.folder_input)
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(browse_btn)
        layout.addLayout(folder_layout)

        # Color input
        layout.addWidget(QLabel("Colors (format: [([R, G, B], weight), ...]):"))
        self.color_input = QTextEdit()
        self.color_input.setPlaceholderText(
            "Example:\n"
            "[([255, 0, 0], 0.3), ([0, 255, 0], 0.2), ([0, 0, 255], 0.5)]"
        )
        self.color_input.setMaximumHeight(150)
        layout.addWidget(self.color_input)

        # Analyze button
        self.analyze_btn = QPushButton("Analyze Co-occurrence")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)

        # Results
        layout.addWidget(QLabel("Co-occurrence Matrix:"))
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            self.image_folder = folder
            self.folder_input.setText(folder)

    def parse_colors(self):
        """Parse color input text."""
        text = self.color_input.toPlainText().strip()
        try:
            color_list = eval(text)
            if not isinstance(color_list, list):
                raise ValueError("Input must be a list")
            colors = []
            for item in color_list:
                if isinstance(item, tuple) and len(item) == 2:
                    colors.append(np.array(item[0]))
                elif isinstance(item, (list, np.ndarray)) and len(item) == 3:
                    colors.append(np.array(item))
                else:
                    raise ValueError("Invalid color format")
            return colors
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Invalid color format: {e}\n\n"
                "Expected format: [([R, G, B], weight), ...]"
            )
            return []

    def analyze(self):
        folder = self.folder_input.toPlainText().strip()
        if not folder:
            QMessageBox.warning(self, "Warning", "Please select a folder.")
            return

        colors = self.parse_colors()
        if not colors:
            return

        analyzer = CooccurrenceAnalyzer()
        matrix = analyzer.analyze_folder(folder, colors)
        result = analyzer.format_matrix(matrix)

        self.result_text.setText(f"Co-occurrence Frequency Matrix:\n\n{result}")


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = CooccurrenceWindow()
    window.show()
    sys.exit(app.exec_())
