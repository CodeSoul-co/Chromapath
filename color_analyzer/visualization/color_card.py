"""Color card generation and visualization."""

import os
from typing import Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt


class ColorCardGenerator:
    """Generate color palette cards from extracted colors."""

    def __init__(self, card_height: int = 150, card_width_scale: int = 400):
        """
        Initialize the color card generator.

        Args:
            card_height: Height of the color card in pixels.
            card_width_scale: Scale factor for card width based on percentages.
        """
        self.card_height = card_height
        self.card_width_scale = card_width_scale

    def create_card(
        self,
        colors: np.ndarray,
        percentages: np.ndarray
    ) -> np.ndarray:
        """
        Create a color card image.

        Args:
            colors: Array of RGB colors (0-255).
            percentages: Array of percentages for each color.

        Returns:
            Color card as numpy array.
        """
        # Sort by percentage descending
        sorted_indices = np.argsort(-percentages)
        sorted_colors = colors[sorted_indices] / 255.0
        sorted_percentages = percentages[sorted_indices]

        # Calculate card dimensions
        widths = [int(p * self.card_width_scale) for p in sorted_percentages]
        total_width = sum(widths)

        if total_width == 0:
            total_width = self.card_width_scale
            widths = [self.card_width_scale // len(colors)] * len(colors)

        # Create color card
        card = np.zeros((self.card_height, total_width, 3))
        start = 0
        for color, width in zip(sorted_colors, widths):
            end = start + width
            card[:, start:end, :] = color
            start = end

        return card

    def save_card(
        self,
        colors: np.ndarray,
        percentages: np.ndarray,
        output_path: str,
        dpi: int = 100
    ) -> None:
        """
        Create and save a color card to file.

        Args:
            colors: Array of RGB colors.
            percentages: Array of percentages.
            output_path: Path to save the image.
            dpi: Image resolution.
        """
        card = self.create_card(colors, percentages)

        plt.figure(figsize=(8, 2))
        plt.imshow(card)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
        plt.close()

    def create_bar_chart(
        self,
        colors: np.ndarray,
        percentages: np.ndarray,
        figsize: Tuple[int, int] = (10, 5)
    ) -> plt.Figure:
        """
        Create a bar chart showing color distribution.

        Args:
            colors: Array of RGB colors.
            percentages: Array of percentages.
            figsize: Figure size.

        Returns:
            Matplotlib figure.
        """
        # Sort by percentage
        sorted_data = sorted(
            zip(colors, percentages),
            key=lambda x: x[1],
            reverse=True
        )
        sorted_colors, sorted_percentages = zip(*sorted_data)

        fig, ax = plt.subplots(figsize=figsize)

        for i, (color, pct) in enumerate(zip(sorted_colors, sorted_percentages)):
            ax.bar(i, pct, color=np.array(color) / 255, edgecolor='black')

        ax.set_xlabel('Color Index')
        ax.set_ylabel('Percentage')
        ax.set_title('Color Distribution')
        ax.set_xticks(range(len(sorted_colors)))

        return fig


def format_color_data(
    colors: np.ndarray,
    percentages: np.ndarray
) -> str:
    """
    Format color data as a readable string.

    Args:
        colors: Array of RGB colors.
        percentages: Array of percentages.

    Returns:
        Formatted string.
    """
    sorted_indices = np.argsort(-percentages)
    lines = ["["]
    for idx in sorted_indices:
        r, g, b = colors[idx].astype(int)
        pct = percentages[idx]
        lines.append(f"    ([{r}, {g}, {b}], {pct:.4f}),")
    lines.append("]")
    return "\n".join(lines)
