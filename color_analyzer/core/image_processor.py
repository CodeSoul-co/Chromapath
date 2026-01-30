"""Image processing utilities for color analysis."""

import os
from typing import List, Tuple, Optional
import cv2
import numpy as np


class ImageProcessor:
    """Handles image loading, filtering, and preprocessing."""

    SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    def __init__(self, gray_threshold: int = 1):
        """
        Initialize the image processor.

        Args:
            gray_threshold: Threshold for filtering out gray pixels.
                           Pixels with max-min channel difference below this are filtered.
        """
        self.gray_threshold = gray_threshold

    def load_image(self, image_path: str) -> np.ndarray:
        """
        Load an image and convert to RGB format.

        Args:
            image_path: Path to the image file.

        Returns:
            RGB image as numpy array.

        Raises:
            FileNotFoundError: If image file doesn't exist.
            ValueError: If image cannot be loaded.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image: {image_path}")

        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def filter_gray_pixels(self, pixels: np.ndarray) -> np.ndarray:
        """
        Filter out gray and near-gray pixels.

        Args:
            pixels: Array of RGB pixels with shape (N, 3).

        Returns:
            Filtered pixels array.
        """
        gray_distance = np.abs(np.max(pixels, axis=1) - np.min(pixels, axis=1))
        return pixels[gray_distance >= self.gray_threshold]

    def extract_pixels(self, image: np.ndarray, filter_gray: bool = True) -> np.ndarray:
        """
        Extract pixels from an image.

        Args:
            image: RGB image array.
            filter_gray: Whether to filter out gray pixels.

        Returns:
            Array of pixels with shape (N, 3).
        """
        pixels = image.reshape(-1, 3)
        if filter_gray:
            pixels = self.filter_gray_pixels(pixels)
        return pixels

    def load_and_extract_pixels(
        self, image_path: str, filter_gray: bool = True
    ) -> np.ndarray:
        """
        Load an image and extract its pixels.

        Args:
            image_path: Path to the image file.
            filter_gray: Whether to filter out gray pixels.

        Returns:
            Array of pixels with shape (N, 3).
        """
        image = self.load_image(image_path)
        return self.extract_pixels(image, filter_gray)

    @classmethod
    def get_image_files(cls, folder_path: str) -> List[str]:
        """
        Get all image files in a folder.

        Args:
            folder_path: Path to the folder.

        Returns:
            List of image file paths.
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Not a directory: {folder_path}")

        files = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(cls.SUPPORTED_EXTENSIONS):
                files.append(os.path.join(folder_path, filename))
        return sorted(files)

    @classmethod
    def get_image_filenames(cls, folder_path: str) -> List[str]:
        """
        Get all image filenames in a folder.

        Args:
            folder_path: Path to the folder.

        Returns:
            List of image filenames (not full paths).
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Not a directory: {folder_path}")

        return sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(cls.SUPPORTED_EXTENSIONS)
        ])
