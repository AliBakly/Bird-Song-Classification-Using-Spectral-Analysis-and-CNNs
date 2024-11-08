# python/src/utils/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import numpy as np
import tensorflow as tf
import pandas as pd
from pathlib import Path

# python/src/birdsong_classification/utils/visualization.py
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import numpy as np
import tensorflow as tf
import pandas as pd
from pathlib import Path

class Visualizer:
    """Utility class for visualizing training and evaluation results"""
    
    def __init__(self, save_dir: str = None):
        """
        Initialize visualizer
        
        Args:
            save_dir: Directory to save plots. If None, uses project's results directory
        """
        if save_dir is None:
            from birdsong_classification.utils.path_utils import get_results_dir
            self.save_dir = get_results_dir()
        else:
            self.save_dir = Path(save_dir)
            
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use('default')  # Reset to default style
        
        # Configure plot style manually
        plt.rcParams['figure.figsize'] = [10.0, 8.0]
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['font.size'] = 10
        
        # Use seaborn color palette
        self.colors = sns.color_palette("husl", 8)
        
        # Set seaborn style settings
        sns.set_style("whitegrid")
    
    def plot_training_history(self, 
                            history: tf.keras.callbacks.History,
                            save_name: Optional[str] = "training_history.png"):
        """
        Plot training history including loss and accuracy
        
        Args:
            history: Keras training history
            save_name: Filename to save plot (if None, display instead)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot training & validation loss
        ax1.plot(history.history['loss'], color=self.colors[0], label='Training Loss')
        if 'val_loss' in history.history:
            ax1.plot(history.history['val_loss'], color=self.colors[1], 
                    label='Validation Loss')
        ax1.set_title('Model Loss', fontsize=14)
        ax1.set_xlabel('Epoch', fontsize=12)
        ax1.set_ylabel('Loss', fontsize=12)
        ax1.legend(fontsize=10)
        ax1.grid(True)
        
        # Plot training & validation accuracy
        ax2.plot(history.history['accuracy'], color=self.colors[0], 
                label='Training Accuracy')
        if 'val_accuracy' in history.history:
            ax2.plot(history.history['val_accuracy'], color=self.colors[1], 
                    label='Validation Accuracy')
        ax2.set_title('Model Accuracy', fontsize=14)
        ax2.set_xlabel('Epoch', fontsize=12)
        ax2.set_ylabel('Accuracy', fontsize=12)
        ax2.legend(fontsize=10)
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.save_dir / save_name, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_confusion_matrix(self,
                            conf_matrix: np.ndarray,
                            categories: List[str],
                            save_name: Optional[str] = "confusion_matrix.png"):
        """
        Plot confusion matrix
        
        Args:
            conf_matrix: Confusion matrix
            categories: List of category names
            save_name: Filename to save plot (if None, display instead)
        """
        plt.figure(figsize=(10, 7))
        
        # Normalize matrix
        conf_matrix_norm = conf_matrix.astype('float') / conf_matrix.sum(axis=1)[:, np.newaxis]
        
        # Create heatmap
        sns.heatmap(conf_matrix_norm,
                   annot=True,
                   cmap='Blues',
                   xticklabels=categories,
                   yticklabels=categories,
                   fmt='.2f')
        
        plt.title('Confusion Matrix', fontsize=20)
        plt.xlabel('True Label', fontsize=16)
        plt.ylabel('Predicted Label', fontsize=16)
        
        if save_name:
            plt.savefig(self.save_dir / save_name, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_species_performance(self,
                               accuracies: Dict[str, float],
                               save_name: Optional[str] = "species_accuracy.png"):
        """
        Plot accuracy by species
        
        Args:
            accuracies: Dictionary mapping species names to accuracies
            save_name: Filename to save plot (if None, display instead)
        """
        plt.figure(figsize=(10, 6))
        
        # Create bar plot
        bars = plt.bar(range(len(accuracies)), 
                      list(accuracies.values()),
                      color=self.colors[:len(accuracies)])
        
        # Customize plot
        plt.title('Accuracy by Species', fontsize=14)
        plt.xlabel('Species', fontsize=12)
        plt.ylabel('Accuracy', fontsize=12)
        plt.xticks(range(len(accuracies)), 
                  list(accuracies.keys()),
                  rotation=45,
                  ha='right')
        plt.ylim(0, 1.0)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2%}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.save_dir / save_name, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()
    
    def plot_sample_spectrograms(self,
                               spectrograms: List[np.ndarray],
                               labels: List[str],
                               predictions: Optional[List[str]] = None,
                               save_name: Optional[str] = "sample_predictions.png"):
        """
        Plot sample spectrograms with their true and predicted labels
        
        Args:
            spectrograms: List of spectrogram images
            labels: True labels
            predictions: Predicted labels (optional)
            save_name: Filename to save plot (if None, display instead)
        """
        n_samples = len(spectrograms)
        fig, axes = plt.subplots(1, n_samples, figsize=(4*n_samples, 4))
        
        if n_samples == 1:
            axes = [axes]
        
        for i, (img, ax) in enumerate(zip(spectrograms, axes)):
            ax.imshow(img)
            title = f"True: {labels[i]}"
            if predictions:
                title += f"\nPred: {predictions[i]}"
            ax.set_title(title)
            ax.axis('off')
        
        plt.tight_layout()
        
        if save_name:
            plt.savefig(self.save_dir / save_name, dpi=300, bbox_inches='tight')
            plt.close()
        else:
            plt.show()