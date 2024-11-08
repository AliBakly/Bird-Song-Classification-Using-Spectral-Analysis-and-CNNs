# src/birdsong_classification/data/preprocessing.py
import numpy as np
from typing import Tuple
from sklearn.model_selection import train_test_split
from birdsong_classification.utils.path_utils import get_project_root, get_models_dir

def preprocess_data(X: np.ndarray, y: np.ndarray, test_size: float = 0.1, random_state: int = 42) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    """
    Preprocess data by standardizing and splitting into train/test sets
    
    Args:
        X: Image data
        y: Labels
        test_size: Fraction of data to use for testing
        random_state: Random seed for reproducibility
        
    Returns:
        (X_train, y_train), (X_test, y_test): Train and test splits
    """
    # Split data first
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Calculate mean and std from training data
    train_mean = np.mean(X_train)
    train_std = np.std(X_train)
    
    # Save training statistics
    models_dir = get_models_dir()
    models_dir.mkdir(exist_ok=True, parents=True)
    np.savez(
        models_dir / 'train_stats.npz',
        mean=train_mean,
        std=train_std
    )
    print(f"Saved training statistics to {models_dir/'train_stats.npz'}")
    
    # Standardize both sets using training statistics
    X_train = (X_train - train_mean) / train_std
    X_test = (X_test - train_mean) / train_std
    
    return (X_train, y_train), (X_test, y_test)