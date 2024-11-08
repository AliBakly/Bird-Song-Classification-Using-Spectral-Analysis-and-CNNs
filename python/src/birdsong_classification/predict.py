# python/src/birdsong_classification/predict.py
import sys
from pathlib import Path
import matlab.engine
import numpy as np
import json
from typing import Dict
import tensorflow as tf
import h5py

from birdsong_classification.data.dataset import BirdSongDataset
from birdsong_classification.models.model import BirdSongClassifier
from birdsong_classification.utils.path_utils import get_project_root, get_models_dir

CATEGORIES = ["common_chaffinch", "eurasian_blue_tit", "house_sparrow"]

def predict_bird_species(audio_path: str) -> Dict:
    """
    Predict bird species from audio file
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Dictionary containing predictions and confidence scores
    """
    print(f"Processing audio file: {audio_path}")
    
    # Create temporary directory for spectrograms
    temp_dir = Path(get_project_root()) / "temp_predict"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Start MATLAB engine
        print("Starting MATLAB engine...")
        eng = matlab.engine.start_matlab()
        
        # Add MATLAB paths
        matlab_dir = get_project_root() / "matlab"
        eng.addpath(str(matlab_dir))
        eng.addpath(str(matlab_dir / "src"))
        eng.addpath(eng.genpath(str(matlab_dir / "src" / "utils")))
        
        # Process audio in MATLAB
        print("Extracting syllables and generating spectrograms...")
        eng.process_single_audio(str(audio_path), str(temp_dir), nargout=0)
        
        # Load spectrograms
        print("Loading spectrograms...")
        dataset = BirdSongDataset(str(temp_dir), CATEGORIES)
        X, _ = dataset.load_data(prediction_mode=True)
        
        # Load and apply training data statistics
        stats = np.load(get_models_dir() / 'train_stats.npz')
        X = (X - stats['mean']) / stats['std']
        print(X.shape)
        # Load model and predict
        print(get_models_dir() / "birdsong_classifier.h5")
        model = BirdSongClassifier.load(get_models_dir() / "birdsong_classifier.h5")

        predictions = model.predict(X)
        pred_classes = np.argmax(predictions, axis=1)
        
        # Vote and calculate confidence
        final_class = np.bincount(pred_classes).argmax()
        confidence_scores = {
            cat: float(np.mean(pred_classes == i))
            for i, cat in enumerate(CATEGORIES)
        }
        
        result = {
            'predicted_species': CATEGORIES[final_class],
            'confidence_scores': confidence_scores,
            'individual_predictions': [CATEGORIES[i] for i in pred_classes]
        }
        
        print("\nPrediction Results:")
        print(f"Predicted Species: {result['predicted_species']}")
        print("\nConfidence Scores:")
        for species, score in result['confidence_scores'].items():
            print(f"  {species}: {score*100:.1f}%")
        
        return result
        
    finally:
        # Cleanup
        try:
            eng.quit()
        except:
            pass
        
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m birdsong_classification.predict <audio_file>")
        sys.exit(1)
    
    predict_bird_species(sys.argv[1])