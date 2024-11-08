# src/birdsong_classification/evaluation/metrics.py
import numpy as np
from typing import Dict, List
import sklearn.metrics

def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray, categories: List[str]) -> Dict:
    """
    Calculate various classification metrics
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        categories: List of category names
        
    Returns:
        Dictionary containing various metrics
    """
    metrics = {}
    
    # Basic metrics
    metrics['confusion_matrix'] = sklearn.metrics.confusion_matrix(y_true, y_pred)
    metrics['accuracy'] = sklearn.metrics.accuracy_score(y_true, y_pred)
    
    # Per-class metrics
    metrics['per_class'] = {}
    for i, category in enumerate(categories):
        metrics['per_class'][category] = {
            'precision': sklearn.metrics.precision_score(y_true, y_pred, average=None)[i],
            'recall': sklearn.metrics.recall_score(y_true, y_pred, average=None)[i],
            'f1': sklearn.metrics.f1_score(y_true, y_pred, average=None)[i]
        }
    
    return metrics