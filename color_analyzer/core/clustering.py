"""Color clustering using K-Means algorithm."""

from typing import Tuple, List
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


class ColorClusterer:
    """Performs color clustering using K-Means algorithm."""

    def __init__(self, n_colors: int = 18, n_init: int = 10, random_state: int = None):
        """
        Initialize the color clusterer.

        Args:
            n_colors: Number of color clusters to extract.
            n_init: Number of K-Means initializations.
            random_state: Random seed for reproducibility.
        """
        self.n_colors = n_colors
        self.n_init = n_init
        self.random_state = random_state

    def fit(self, pixels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Cluster pixels and extract dominant colors with percentages.

        Args:
            pixels: Array of RGB pixels with shape (N, 3).

        Returns:
            Tuple of (colors, percentages):
                - colors: Array of RGB colors with shape (n_colors, 3)
                - percentages: Array of percentages for each color
        """
        kmeans = KMeans(
            n_clusters=self.n_colors,
            n_init=self.n_init,
            random_state=self.random_state
        )
        labels = kmeans.fit_predict(pixels)
        
        label_counts = Counter(labels)
        total_counts = len(labels)
        
        colors = kmeans.cluster_centers_
        percentages = np.array([
            label_counts[i] / total_counts for i in range(self.n_colors)
        ])
        
        return colors, percentages

    def fit_sorted(self, pixels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Cluster pixels and return colors sorted by percentage (descending).

        Args:
            pixels: Array of RGB pixels with shape (N, 3).

        Returns:
            Tuple of (sorted_colors, sorted_percentages).
        """
        colors, percentages = self.fit(pixels)
        sorted_indices = np.argsort(-percentages)
        return colors[sorted_indices], percentages[sorted_indices]


def cluster_multiple_images(
    pixels_list: List[np.ndarray],
    n_colors: int = 18
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Cluster colors from multiple images combined.

    Args:
        pixels_list: List of pixel arrays from different images.
        n_colors: Number of color clusters.

    Returns:
        Tuple of (colors, percentages).
    """
    all_pixels = np.vstack(pixels_list)
    clusterer = ColorClusterer(n_colors=n_colors, n_init=20)
    return clusterer.fit_sorted(all_pixels)
