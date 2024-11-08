# src/birdsong_classification/models/train.py
from pathlib import Path
import numpy as np

from birdsong_classification.data.dataset import BirdSongDataset
from birdsong_classification.models.model import BirdSongClassifier
from birdsong_classification.utils.path_utils import get_project_root, get_data_dir, get_models_dir
from birdsong_classification.utils.visualization import Visualizer

def main():
    # Get directories using utility functions
    data_dir = get_data_dir() / "processed" / "train"
    models_dir = get_models_dir()
    
    # Create models directory if it doesn't exist
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading data from: {data_dir}")
    print(f"Saving model to: {models_dir}")
    
    try:
        # Load processed data
        X, y = BirdSongDataset.load_pickle_data(data_dir)
        print(f"Loaded {len(X)} samples with shape {X.shape}")
        
        # Create and train model
        model = BirdSongClassifier(
            input_shape=X.shape[1:],
            num_classes=len(np.unique(y))
        )
        
        # Train model
        print("Training model...")
        history = model.train(X, y, epochs=50)
        
        # Save model
        model_path = models_dir / "birdsong_classifier.h5"
        model.save(model_path)
        print(f"Model saved to {model_path}")
        
        # Plot training history
        try:
            visualizer = Visualizer()
            visualizer.plot_training_history(history)
            print("Training plots saved to results directory")
        except Exception as viz_error:
            print(f"Warning: Could not create visualization: {viz_error}")
        
    except Exception as e:
        print(f"Error during training: {e}")
        raise

if __name__ == "__main__":
    main()