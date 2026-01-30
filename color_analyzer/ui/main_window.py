"""Main launcher window for all color analysis tools."""

import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QApplication
)
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    """Main launcher window for color analysis tools."""

    def __init__(self):
        super().__init__()
        self.windows = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chromapath")
        self.setGeometry(100, 100, 400, 350)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel("Chromapath")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)

        # Description
        desc = QLabel(
            "A comprehensive toolkit for image color analysis,\n"
            "palette extraction, and visualization."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setStyleSheet("margin-bottom: 20px;")
        layout.addWidget(desc)

        # Tool buttons
        tools = [
            ("Palette Generator", "Generate color palettes from images",
             self.open_palette_generator),
            ("Color Extractor", "Extract and analyze colors from image folders",
             self.open_color_extractor),
            ("Co-occurrence Analyzer", "Analyze color co-occurrence patterns",
             self.open_cooccurrence),
            ("Network Viewer", "Visualize color relationships",
             self.open_network_viewer),
            ("Genetic Optimizer", "Interactive genetic algorithm optimization",
             self.open_genetic_optimizer),
        ]

        for name, tooltip, callback in tools:
            btn = QPushButton(name)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setStyleSheet("padding: 10px; margin: 5px;")
            layout.addWidget(btn)

        layout.addStretch()

        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def open_palette_generator(self):
        from .palette_generator import PaletteGeneratorWindow
        self._open_window("palette", PaletteGeneratorWindow)

    def open_color_extractor(self):
        from .color_extractor import ColorExtractorWindow
        self._open_window("extractor", ColorExtractorWindow)

    def open_cooccurrence(self):
        from .cooccurrence_analyzer import CooccurrenceWindow
        self._open_window("cooccurrence", CooccurrenceWindow)

    def open_network_viewer(self):
        from .network_viewer import NetworkViewerWindow
        self._open_window("network", NetworkViewerWindow)

    def open_genetic_optimizer(self):
        from .genetic_optimizer import GeneticOptimizerWindow
        self._open_window("genetic", GeneticOptimizerWindow)

    def _open_window(self, key: str, window_class):
        """Open or focus a tool window."""
        if key in self.windows and self.windows[key].isVisible():
            self.windows[key].raise_()
            self.windows[key].activateWindow()
        else:
            self.windows[key] = window_class()
            self.windows[key].show()
        self.status_label.setText(f"Opened: {window_class.__name__}")


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
