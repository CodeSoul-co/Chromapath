"""Genetic optimizer UI - interactive genetic algorithm for color schemes."""

import sys
from typing import List
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFileDialog, QSpinBox, QDoubleSpinBox,
    QScrollArea, QMessageBox, QSlider, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

from ..core.genetic import GeneticColorOptimizer


class ColorSchemeWidget(QFrame):
    """Widget displaying a single color scheme."""

    def __init__(self, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)

        layout = QVBoxLayout(self)

        # Title
        self.title_label = QLabel(f"Scheme {index + 1}")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # Image display
        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 150)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        # Score slider
        score_layout = QHBoxLayout()
        score_layout.addWidget(QLabel("Score:"))
        self.score_slider = QSlider(Qt.Horizontal)
        self.score_slider.setRange(0, 100)
        self.score_slider.setValue(50)
        score_layout.addWidget(self.score_slider)
        self.score_label = QLabel("5.0")
        self.score_slider.valueChanged.connect(
            lambda v: self.score_label.setText(f"{v/10:.1f}")
        )
        score_layout.addWidget(self.score_label)
        layout.addLayout(score_layout)

    def set_image(self, fig):
        """Set the displayed image from a matplotlib figure."""
        canvas = FigureCanvas(fig)
        canvas.draw()

        # Convert to pixmap
        width, height = fig.canvas.get_width_height()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(height, width, 3)

        from PyQt5.QtGui import QImage, QPixmap
        qimg = QImage(img.data, width, height, 3 * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(
            200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(pixmap)
        plt.close(fig)

    def get_score(self) -> float:
        return self.score_slider.value() / 10.0


class GeneticOptimizerWindow(QMainWindow):
    """Window for interactive genetic color optimization."""

    def __init__(self):
        super().__init__()
        self.optimizer = None
        self.scheme_widgets: List[ColorSchemeWidget] = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Genetic Color Optimizer")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Control panel
        control_layout = QHBoxLayout()

        # Open image button
        self.open_btn = QPushButton("Open Image")
        self.open_btn.clicked.connect(self.open_image)
        control_layout.addWidget(self.open_btn)

        # Parameters
        control_layout.addWidget(QLabel("Colors:"))
        self.colors_spin = QSpinBox()
        self.colors_spin.setRange(2, 9)
        self.colors_spin.setValue(5)
        control_layout.addWidget(self.colors_spin)

        control_layout.addWidget(QLabel("Grid:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 6)
        self.rows_spin.setValue(3)
        control_layout.addWidget(self.rows_spin)
        control_layout.addWidget(QLabel("x"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 6)
        self.cols_spin.setValue(3)
        control_layout.addWidget(self.cols_spin)

        control_layout.addWidget(QLabel("Mutation:"))
        self.mutation_spin = QDoubleSpinBox()
        self.mutation_spin.setRange(0.0, 1.0)
        self.mutation_spin.setSingleStep(0.1)
        self.mutation_spin.setValue(0.3)
        control_layout.addWidget(self.mutation_spin)

        control_layout.addWidget(QLabel("Elite Threshold:"))
        self.elite_spin = QDoubleSpinBox()
        self.elite_spin.setRange(0.0, 10.0)
        self.elite_spin.setSingleStep(0.5)
        self.elite_spin.setValue(7.5)
        control_layout.addWidget(self.elite_spin)

        control_layout.addStretch()
        main_layout.addLayout(control_layout)

        # Action buttons
        action_layout = QHBoxLayout()
        self.evolve_btn = QPushButton("Evolve Next Generation")
        self.evolve_btn.clicked.connect(self.evolve)
        self.evolve_btn.setEnabled(False)
        action_layout.addWidget(self.evolve_btn)

        self.best_btn = QPushButton("Show Best")
        self.best_btn.clicked.connect(self.show_best)
        self.best_btn.setEnabled(False)
        action_layout.addWidget(self.best_btn)

        action_layout.addStretch()

        # Generation info
        self.gen_label = QLabel("Generation: 0")
        action_layout.addWidget(self.gen_label)

        main_layout.addLayout(action_layout)

        # Scroll area for schemes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.schemes_widget = QWidget()
        self.schemes_layout = QGridLayout(self.schemes_widget)
        scroll.setWidget(self.schemes_widget)
        main_layout.addWidget(scroll)

        # Fitness plot
        self.figure, self.ax = plt.subplots(figsize=(8, 2))
        self.fitness_canvas = FigureCanvas(self.figure)
        self.fitness_canvas.setMaximumHeight(150)
        main_layout.addWidget(self.fitness_canvas)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image",
            "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return

        n_colors = self.colors_spin.value()
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        mutation_rate = self.mutation_spin.value()
        elite_threshold = self.elite_spin.value()

        try:
            self.optimizer = GeneticColorOptimizer(
                image_path=file_path,
                n_colors=n_colors,
                population_size=rows * cols,
                mutation_rate=mutation_rate,
                elite_threshold=elite_threshold
            )
            self.display_population(rows, cols)
            self.evolve_btn.setEnabled(True)
            self.best_btn.setEnabled(True)
            self.gen_label.setText(f"Generation: {self.optimizer.generation}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load image: {e}")

    def display_population(self, rows: int, cols: int):
        # Clear existing widgets
        for widget in self.scheme_widgets:
            widget.deleteLater()
        self.scheme_widgets.clear()

        # Create new widgets
        for i, scheme in enumerate(self.optimizer.population):
            widget = ColorSchemeWidget(i)

            # Create scheme image
            fig, ax = plt.subplots(figsize=(3, 2))
            segmented = self.optimizer.apply_scheme(scheme)
            ax.imshow(segmented.astype(np.uint8))
            ax.axis('off')
            widget.set_image(fig)

            row, col = i // cols, i % cols
            self.schemes_layout.addWidget(widget, row, col)
            self.scheme_widgets.append(widget)

    def evolve(self):
        if not self.optimizer:
            return

        # Collect scores
        scores = [w.get_score() for w in self.scheme_widgets]
        self.optimizer.set_scores(scores)

        # Evolve
        self.optimizer.evolve()

        # Update display
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        self.display_population(rows, cols)
        self.gen_label.setText(f"Generation: {self.optimizer.generation}")

        # Update fitness plot
        self.update_fitness_plot()

    def update_fitness_plot(self):
        self.ax.clear()
        history = self.optimizer.fitness_history
        if history["average"]:
            self.ax.plot(history["average"], 'b-o', label='Average')
            self.ax.plot(history["best"], 'r-s', label='Best')
            self.ax.set_xlabel('Generation')
            self.ax.set_ylabel('Fitness')
            self.ax.legend()
            self.ax.set_title('Fitness Over Generations')
        self.fitness_canvas.draw()

    def show_best(self):
        if not self.optimizer:
            return

        scheme, score = self.optimizer.get_best_scheme()

        fig, ax = plt.subplots(figsize=(8, 6))
        segmented = self.optimizer.apply_scheme(scheme)
        ax.imshow(segmented.astype(np.uint8))
        ax.set_title(f"Best Scheme (Score: {score:.1f})")
        ax.axis('off')
        plt.show()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GeneticOptimizerWindow()
    window.show()
    sys.exit(app.exec_())
