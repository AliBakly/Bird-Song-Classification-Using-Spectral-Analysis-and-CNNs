# src/birdsong_classification/evaluation/evaluate.py
from pathlib import Path
import numpy as np

from birdsong_classification.data.dataset import BirdSongDataset
from birdsong_classification.models.model import BirdSongClassifier
from birdsong_classification.utils.visualization import Visualizer
from birdsong_classification.utils.path_utils import get_data_dir, get_models_dir, get_results_dir
import sklearn.metrics
# Use lowercase for directories to match actual folder names
CATEGORIES = ["common_chaffinch", "eurasian_blue_tit", "house_sparrow"]

def main():
    # Get directories using utility functions
    data_dir = get_data_dir() / "processed" / "test"
    models_dir = get_models_dir()
    results_dir = get_results_dir()
    
    print(f"Loading test data from: {data_dir}")
    print(f"Loading model from: {models_dir}")
    print(f"Saving results to: {results_dir}")
    
    try:
        # Load test data
        X, y = BirdSongDataset.load_pickle_data(data_dir)
        print(f"Loaded {len(X)} test samples")
        
        # Load model
        model_path = models_dir / "birdsong_classifier.h5"
        model = BirdSongClassifier.load(model_path)
        print("Model loaded successfully")
        
        # Overall evaluation
        loss, acc = model.evaluate(X, y)
        print(f"\nOverall Evaluation:")
        print(f"Loss: {loss:.4f}")
        print(f"Accuracy: {acc:.4f}")
        
        # Evaluate by species
        species_accuracies = {}
        print("\nEvaluation by Species:")
        for class_idx, category in enumerate(CATEGORIES):
            # Get indices for current species
            species_mask = (y == class_idx)
            X_species = X[species_mask]
            y_species = y[species_mask]
            
            # Evaluate
            loss, acc = model.evaluate(X_species, y_species)
            print(f"{category}:")
            print(f"  Samples: {len(X_species)}")
            print(f"  Loss: {loss:.4f}")
            print(f"  Accuracy: {acc:.4f}")
            species_accuracies[category] = acc
        
        # Generate predictions and confusion matrix
        print("\nGenerating predictions and plotting results...")
        predictions = model.predict(X)
        pred_classes = np.argmax(predictions, axis=1)
        
        # Create confusion matrix
        conf_matrix = sklearn.metrics.confusion_matrix(y, pred_classes)
        
        # Create visualizations
        visualizer = Visualizer()
        
        # Plot and save confusion matrix
        visualizer.plot_confusion_matrix(
            conf_matrix=conf_matrix,
            categories=CATEGORIES,
            save_name="confusion_matrix.png"
        )
        
        # Plot species performance
        visualizer.plot_species_performance(
            accuracies=species_accuracies,
            save_name="species_accuracy.png"
        )
        
        # Additional metrics
        print("\nDetailed Classification Report:")
        print(sklearn.metrics.classification_report(
            y, pred_classes,
            target_names=CATEGORIES,
            digits=4
        ))
        
        print(f"\nResults saved to {results_dir}")
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        raise

if __name__ == "__main__":
    main()