"""Setup script for Chromapath."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="chromapath",
    version="1.0.0",
    author="xiaqianlong, duanzhenke",
    author_email="xiaqianlong@code-soul.com, duanzhenke@code-soul.com",
    description="A toolkit for image color analysis and visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chromapath",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "opencv-python>=4.5.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0",
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "chromapath=main:main",
        ],
    },
)
