"""Genetic algorithm for color scheme optimization."""

import random
from typing import List, Tuple, Optional
import numpy as np
from sklearn.cluster import KMeans

from .image_processor import ImageProcessor


# Default color palette
DEFAULT_COLORS = [
    [171, 162, 157],
    [175, 186, 196],
    [211, 196, 182],
    [84, 33, 35],
    [216, 160, 80],
    [86, 86, 69],
    [229, 170, 72],
    [0, 0, 0],
    [255, 255, 255],
]


class GeneticColorOptimizer:
    """Genetic algorithm for optimizing color schemes."""

    def __init__(
        self,
        image_path: str,
        n_colors: int,
        population_size: int = 16,
        mutation_rate: float = 0.3,
        max_mutation_change: float = 0.3,
        elite_threshold: float = 7.5,
        predefined_colors: Optional[List[List[int]]] = None
    ):
        """
        Initialize the genetic optimizer.

        Args:
            image_path: Path to the image file.
            n_colors: Number of colors in each scheme.
            population_size: Number of individuals in population.
            mutation_rate: Proportion of population to mutate.
            max_mutation_change: Maximum color value change ratio.
            elite_threshold: Score threshold for elite retention.
            predefined_colors: Optional list of predefined RGB colors.
        """
        self.image_path = image_path
        self.n_colors = n_colors
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_mutation_change = max_mutation_change
        self.elite_threshold = elite_threshold
        self.predefined_colors = predefined_colors or DEFAULT_COLORS

        self.processor = ImageProcessor()
        self.image = self.processor.load_image(image_path)
        self.labels = self._cluster_image()
        self.population = self._generate_initial_population()
        self.scores = [5.0] * population_size
        self.generation = 0
        self.fitness_history = {"average": [], "best": []}

    def _cluster_image(self) -> np.ndarray:
        """Cluster image pixels and return labels."""
        pixels = self.image.reshape(-1, 3)
        kmeans = KMeans(n_clusters=self.n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)
        return kmeans.labels_

    def _generate_initial_population(self) -> List[List[List[int]]]:
        """Generate initial population from predefined colors."""
        selected = self.predefined_colors[:self.n_colors]
        return [
            random.sample(selected, len(selected))
            for _ in range(self.population_size)
        ]

    def apply_scheme(self, scheme: List[List[int]]) -> np.ndarray:
        """
        Apply a color scheme to the image.

        Args:
            scheme: List of RGB colors.

        Returns:
            Recolored image array.
        """
        return np.array([
            scheme[label] for label in self.labels
        ]).reshape(self.image.shape)

    def set_scores(self, scores: List[float]) -> None:
        """
        Set fitness scores for the current population.

        Args:
            scores: List of scores (0-10) for each individual.
        """
        if len(scores) != self.population_size:
            raise ValueError(f"Expected {self.population_size} scores")
        self.scores = scores

    def evolve(self) -> None:
        """Evolve to the next generation."""
        if not all(score >= 0 for score in self.scores):
            raise ValueError("All schemes must be scored before evolution")

        # Record fitness history
        self.fitness_history["average"].append(np.mean(self.scores))
        self.fitness_history["best"].append(max(self.scores))

        # Preserve elite individuals
        elite = [
            scheme for i, scheme in enumerate(self.population)
            if self.scores[i] >= self.elite_threshold
        ]

        # Generate offspring
        num_offspring = self.population_size - len(elite)
        offspring = self._generate_offspring(num_offspring)

        # Apply mutation
        mutated = self._mutate(offspring)

        # Create new population
        self.population = mutated + elite
        self.scores = [5.0] * self.population_size
        self.generation += 1

    def _generate_offspring(self, count: int) -> List[List[List[int]]]:
        """Generate offspring through selection and crossover."""
        offspring = []
        while len(offspring) < count:
            parent1, parent2 = self._roulette_selection()
            child = self._crossover(parent1, parent2)
            offspring.append(child)
        return offspring

    def _roulette_selection(self) -> Tuple[List[List[int]], List[List[int]]]:
        """Select two parents using roulette wheel selection."""
        total = sum(self.scores)
        if total == 0:
            return (
                random.choice(self.population),
                random.choice(self.population)
            )

        weights = [s / total for s in self.scores]
        parent1 = random.choices(self.population, weights=weights, k=1)[0]
        parent2 = random.choices(self.population, weights=weights, k=1)[0]
        return parent1, parent2

    def _crossover(
        self,
        parent1: List[List[int]],
        parent2: List[List[int]]
    ) -> List[List[int]]:
        """Perform two-point crossover."""
        if len(parent1) < 3:
            return parent1.copy()

        points = sorted(random.sample(range(1, len(parent1)), 2))
        return (
            parent1[:points[0]] +
            parent2[points[0]:points[1]] +
            parent1[points[1]:]
        )

    def _mutate(
        self,
        population: List[List[List[int]]]
    ) -> List[List[List[int]]]:
        """Apply mutation to a portion of the population."""
        count = int(self.mutation_rate * len(population))
        indices = random.sample(range(len(population)), min(count, len(population)))

        for idx in indices:
            scheme = population[idx]
            population[idx] = [
                [
                    max(0, min(255, int(
                        c * (1 + random.uniform(
                            -self.max_mutation_change,
                            self.max_mutation_change
                        ))
                    )))
                    for c in color
                ]
                for color in scheme
            ]

        return population

    def get_best_scheme(self) -> Tuple[List[List[int]], float]:
        """Get the best scoring scheme."""
        best_idx = np.argmax(self.scores)
        return self.population[best_idx], self.scores[best_idx]
