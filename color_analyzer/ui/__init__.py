"""PyQt5 UI modules for color analysis applications."""

from .palette_generator import PaletteGeneratorWindow
from .color_extractor import ColorExtractorWindow
from .cooccurrence_analyzer import CooccurrenceWindow
from .network_viewer import NetworkViewerWindow
from .genetic_optimizer import GeneticOptimizerWindow
from .main_window import MainWindow

__all__ = [
    "PaletteGeneratorWindow",
    "ColorExtractorWindow",
    "CooccurrenceWindow",
    "NetworkViewerWindow",
    "GeneticOptimizerWindow",
    "MainWindow",
]
