"""High-level color extraction from images."""

import os
from typing import List, Tuple, Optional
import numpy as np

from .image_processor import ImageProcessor
from .clustering import ColorClusterer


class ColorExtractor:
    """Extract dominant colors from images."""

    def __init__(
        self,
        n_colors: int = 18,
        gray_threshold: int = 1
    ):
        """
        Initialize the color extractor.

        Args:
            n_colors: Number of colors to extract.
            gray_threshold: Threshold for filtering gray pixels.
        """
        self.n_colors = n_colors
        self.processor = ImageProcessor(gray_threshold=gray_threshold)
        self.clusterer = ColorClusterer(n_colors=n_colors)

    def extract_from_image(
        self, image_path: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract dominant colors from a single image.

        Args:
            image_path: Path to the image file.

        Returns:
            Tuple of (colors, percentages) sorted by percentage descending.
        """
        pixels = self.processor.load_and_extract_pixels(image_path)
        if pixels.size == 0:
            return np.array([]), np.array([])
        return self.clusterer.fit_sorted(pixels)

    def extract_from_folder(
        self,
        folder_path: str,
        progress_callback: Optional[callable] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract dominant colors from all images in a folder.

        Args:
            folder_path: Path to the folder containing images.
            progress_callback: Optional callback(current, total, filename).

        Returns:
            Tuple of (colors, percentages) from combined analysis.
        """
        image_files = self.processor.get_image_files(folder_path)
        if not image_files:
            return np.array([]), np.array([])

        all_pixels = []
        total = len(image_files)

        for i, image_path in enumerate(image_files):
            if progress_callback:
                progress_callback(i, total, os.path.basename(image_path))

            try:
                pixels = self.processor.load_and_extract_pixels(image_path)
                if pixels.size > 0:
                    all_pixels.append(pixels)
            except Exception:
                continue

        if not all_pixels:
            return np.array([]), np.array([])

        combined_pixels = np.vstack(all_pixels)
        return self.clusterer.fit_sorted(combined_pixels)

    def extract_per_image(
        self,
        folder_path: str,
        progress_callback: Optional[callable] = None
    ) -> List[Tuple[str, np.ndarray, np.ndarray]]:
        """
        Extract colors from each image separately.

        Args:
            folder_path: Path to the folder containing images.
            progress_callback: Optional callback(current, total, filename).

        Returns:
            List of (filename, colors, percentages) tuples.
        """
        image_files = self.processor.get_image_files(folder_path)
        results = []
        total = len(image_files)

        for i, image_path in enumerate(image_files):
            filename = os.path.basename(image_path)
            if progress_callback:
                progress_callback(i, total, filename)

            try:
                colors, percentages = self.extract_from_image(image_path)
                if colors.size > 0:
                    results.append((filename, colors, percentages))
            except Exception:
                continue

        return results
