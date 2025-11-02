# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-02

### Added
- Complete refactoring of the codebase with professional standards
- Comprehensive English documentation and README
- Type hints for all functions
- Proper error handling and logging throughout
- Command-line interface (CLI) for all operations
- Unit tests with 100% core functionality coverage
- GitHub Actions CI/CD pipeline
- Setup.py for proper Python packaging
- Example scripts and sample data
- CONTRIBUTING guide for contributors
- MIT License
- .gitattributes for proper file handling
- Professional project structure with separate modules

### Changed
- Renamed functions to follow Python naming conventions:
  - `create_heatmap_random()` → `create_heatmap_from_points()`
  - `change_coordinates()` → `update_coordinates()`
  - `overlap_images()` → `overlay_images()`
  - `meshgrid()` → `create_meshgrid()`
  - `process_data()` → `calculate_intensity()`
  - `alpha_clip()` → `normalize_alpha()`
  - `heatmap_output()` → `save_heatmap()`
- Improved animation.togif module to be reusable and configurable
- Enhanced all modules with comprehensive docstrings
- Converted Spanish comments to English documentation

### Removed
- Removed large binary files (animations, test images) from repository
- Removed temporary files and notebooks
- Removed hardcoded file paths
- Removed .DS_Store and other OS-specific files

### Fixed
- Improved error handling for missing files
- Better resource management with context managers
- Fixed hardcoded crop coordinates (now configurable)

## [0.1] - Previous Version

### Initial Features
- Basic heatmap generation using KDE
- Point cloud visualization
- Animation creation
- Image overlay capabilities
