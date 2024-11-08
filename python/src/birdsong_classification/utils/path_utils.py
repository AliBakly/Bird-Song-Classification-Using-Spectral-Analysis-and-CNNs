# src/utils/path_utils.py
from pathlib import Path

def get_project_root() -> Path:
    """Get absolute path to project root directory"""
    # Get the location of this utility file
    current_file = Path(__file__).resolve()
    # Go up to project root (from utils/path_utils.py to project root)
    project_root = current_file.parent.parent.parent.parent.parent
    return project_root

def get_data_dir() -> Path:
    """Get path to data directory"""
    return get_project_root() / "data"

def get_models_dir() -> Path:
    """Get path to models directory"""
    return get_project_root() / "models"

def get_results_dir() -> Path:
    """Get path to results directory"""
    return get_project_root() / "results"