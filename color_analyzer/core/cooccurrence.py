"""Color co-occurrence analysis."""

import os
from typing import List, Tuple, Optional
from itertools import combinations
import numpy as np

from .image_processor import ImageProcessor


class CooccurrenceAnalyzer:
    """Analyze color co-occurrence patterns across images."""

    def __init__(self, distance_threshold: float = 1.0):
        """
        Initialize the co-occurrence analyzer.

        Args:
            distance_threshold: Euclidean distance threshold for color matching.
        """
        self.distance_threshold = distance_threshold
        self.processor = ImageProcessor()

    def is_color_present(
        self,
        pixels: np.ndarray,
        color: np.ndarray
    ) -> bool:
        """
        Check if a color is present in the pixel array.

        Args:
            pixels: Array of RGB pixels with shape (N, 3).
            color: RGB color to search for.

        Returns:
            True if color is found within threshold distance.
        """
        distances = np.sqrt(np.sum((pixels - color) ** 2, axis=-1))
        return np.any(distances <= self.distance_threshold)

    def are_colors_present(
        self,
        pixels: np.ndarray,
        colors: List[np.ndarray]
    ) -> bool:
        """
        Check if any of the specified colors are present.

        Args:
            pixels: Array of RGB pixels.
            colors: List of RGB colors to search for.

        Returns:
            True if any color is found.
        """
        for color in colors:
            if self.is_color_present(pixels, color):
                return True
        return False

    def analyze_folder(
        self,
        folder_path: str,
        colors: List[np.ndarray],
        progress_callback: Optional[callable] = None
    ) -> np.ndarray:
        """
        Analyze color co-occurrence across all images in a folder.

        Args:
            folder_path: Path to the image folder.
            colors: List of RGB colors to analyze.
            progress_callback: Optional callback(current, total).

        Returns:
            Co-occurrence frequency matrix of shape (n_colors, n_colors).
        """
        image_files = self.processor.get_image_files(folder_path)
        num_colors = len(colors)
        color_pairs = list(combinations(range(num_colors), 2))
        cooccurrence_count = np.zeros((num_colors, num_colors), dtype=int)

        total = len(image_files)
        for idx, image_path in enumerate(image_files):
            if progress_callback:
                progress_callback(idx, total)

            try:
                image = self.processor.load_image(image_path)
                pixels = self.processor.extract_pixels(image, filter_gray=False)

                if self.are_colors_present(pixels, colors):
                    for i, j in color_pairs:
                        if self.are_colors_present(pixels, [colors[i], colors[j]]):
                            cooccurrence_count[i, j] += 1
                            cooccurrence_count[j, i] += 1
            except Exception:
                continue

        if total > 0:
            return cooccurrence_count / total
        return cooccurrence_count.astype(float)

    @staticmethod
    def format_matrix(matrix: np.ndarray, precision: int = 2) -> str:
        """
        Format a matrix as a readable string.

        Args:
            matrix: 2D numpy array.
            precision: Decimal precision for formatting.

        Returns:
            Formatted string representation.
        """
        lines = ["["]
        fmt = f"{{:.{precision}f}}"
        for row in matrix:
            row_str = ", ".join(fmt.format(val) for val in row)
            lines.append(f"    [{row_str}],")
        lines.append("]")
        return "\n".join(lines)
