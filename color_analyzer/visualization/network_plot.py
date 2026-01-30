"""Network visualization for color relationships."""

from typing import List, Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt


class NetworkPlotter:
    """Plot network graphs showing color relationships."""

    def __init__(
        self,
        base_threshold: int = 3,
        highlight_threshold: int = 7
    ):
        """
        Initialize the network plotter.

        Args:
            base_threshold: Minimum weight to draw an edge.
            highlight_threshold: Weight threshold for highlighted edges.
        """
        self.base_threshold = base_threshold
        self.highlight_threshold = highlight_threshold

    def plot(
        self,
        colors: List[Tuple[int, int, int]],
        sizes: List[float],
        matrix: np.ndarray,
        figsize: Tuple[int, int] = (10, 10),
        ax: Optional[plt.Axes] = None,
        progress_callback: Optional[callable] = None
    ) -> plt.Figure:
        """
        Create a network plot of color relationships.

        Args:
            colors: List of RGB colors (0-255).
            sizes: List of node sizes.
            matrix: Adjacency matrix of relationships.
            figsize: Figure size.
            ax: Optional existing axes to plot on.
            progress_callback: Optional callback(current, total).

        Returns:
            Matplotlib figure.
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = ax.figure

        num_nodes = len(colors)

        # Generate positions (circular layout)
        angles = np.linspace(0, 2 * np.pi, num_nodes, endpoint=False)
        positions = np.column_stack([np.cos(angles), np.sin(angles)])

        # Normalize colors
        node_colors = [tuple(c / 255 for c in color) for color in colors]
        node_sizes = [s * 100 for s in sizes]

        # Draw edges
        total_edges = num_nodes * (num_nodes - 1) // 2
        edge_count = 0

        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                weight = matrix[i][j]

                if weight >= self.highlight_threshold:
                    edge_color = 'red'
                    linewidth = 2
                elif weight >= self.base_threshold:
                    edge_color = 'gray'
                    linewidth = 1
                else:
                    edge_count += 1
                    continue

                ax.plot(
                    [positions[i][0], positions[j][0]],
                    [positions[i][1], positions[j][1]],
                    color=edge_color,
                    lw=linewidth,
                    alpha=0.6
                )

                edge_count += 1
                if progress_callback and total_edges > 0:
                    progress_callback(edge_count, total_edges)

        # Draw nodes
        ax.scatter(
            positions[:, 0],
            positions[:, 1],
            c=node_colors,
            s=node_sizes,
            alpha=0.8,
            edgecolors='black',
            linewidths=1
        )

        # Add labels
        for i, pos in enumerate(positions):
            ax.annotate(
                str(i + 1),
                pos,
                ha='center',
                va='center',
                fontsize=8,
                fontweight='bold'
            )

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Color Relationship Network')

        return fig


def parse_color_input(text: str) -> Tuple[List[Tuple[int, int, int]], List[float]]:
    """
    Parse color input text in format: R G B size (one per line).

    Args:
        text: Input text with color data.

    Returns:
        Tuple of (colors, sizes).
    """
    colors = []
    sizes = []

    for line in text.strip().split('\n'):
        parts = line.split()
        if len(parts) >= 4:
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
            size = float(parts[3])
            colors.append((r, g, b))
            sizes.append(size)

    return colors, sizes


def parse_matrix_input(text: str) -> np.ndarray:
    """
    Parse matrix input text.

    Args:
        text: Input text with matrix data.

    Returns:
        Numpy array matrix.
    """
    rows = []
    for line in text.strip().split('\n'):
        if line.strip():
            row = list(map(float, line.split()))
            rows.append(row)
    return np.array(rows)
