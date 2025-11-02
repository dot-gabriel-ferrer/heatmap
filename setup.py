"""Setup configuration for heatmap package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").splitlines()

setup(
    name="heatmap-generator",
    version="1.0.0",
    author="Heatmap Contributors",
    description="A professional Python toolkit for generating heatmaps over geographic maps and point cloud data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dot-gabriel-ferrer/heatmap",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "heatmap=cli:main",
        ],
    },
    keywords="heatmap visualization kde geographic point-cloud mapping",
    project_urls={
        "Bug Reports": "https://github.com/dot-gabriel-ferrer/heatmap/issues",
        "Source": "https://github.com/dot-gabriel-ferrer/heatmap",
    },
)
