#!/usr/bin/env python3
"""
Chromapath - Main Entry Point

A comprehensive toolkit for image color analysis, palette extraction,
and visualization.

Usage:
    python main.py              # Launch the main GUI
    python main.py --help       # Show help
"""

import sys
import argparse


def main():
    """Main entry point for Chromapath."""
    parser = argparse.ArgumentParser(
        description="Chromapath - Image color analysis toolkit"
    )
    parser.add_argument(
        "--tool",
        choices=["palette", "extractor", "cooccurrence", "network", "genetic"],
        help="Launch a specific tool directly"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Chromapath 1.0.0"
    )

    args = parser.parse_args()

    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    if args.tool == "palette":
        from color_analyzer.ui.palette_generator import PaletteGeneratorWindow
        window = PaletteGeneratorWindow()
    elif args.tool == "extractor":
        from color_analyzer.ui.color_extractor import ColorExtractorWindow
        window = ColorExtractorWindow()
    elif args.tool == "cooccurrence":
        from color_analyzer.ui.cooccurrence_analyzer import CooccurrenceWindow
        window = CooccurrenceWindow()
    elif args.tool == "network":
        from color_analyzer.ui.network_viewer import NetworkViewerWindow
        window = NetworkViewerWindow()
    elif args.tool == "genetic":
        from color_analyzer.ui.genetic_optimizer import GeneticOptimizerWindow
        window = GeneticOptimizerWindow()
    else:
        from color_analyzer.ui.main_window import MainWindow
        window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
