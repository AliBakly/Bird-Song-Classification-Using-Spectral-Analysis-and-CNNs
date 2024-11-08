from pathlib import Path
from dataset import BirdSongDataset
from preprocessing import preprocess_data
from birdsong_classification.utils.path_utils import get_project_root, get_data_dir
import os
import numpy as np
def main():
    # Get directories using utility functions
    project_root = get_project_root()
    data_dir = get_data_dir()
    DATA_DIR = data_dir / "spectrograms"
    TRAIN_DIR = data_dir / "processed" / "train"
    TEST_DIR = data_dir / "processed" / "test"
    CATEGORIES = ["common_chaffinch", "eurasian_blue_tit", "house_sparrow"]
    IMG_SIZE = 150
    
    # Ensure directories exist
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Data directory not found: {DATA_DIR}\n"
            f"Current working directory: {os.getcwd()}\n"
            f"Project root: {project_root}"
        )
    
    # Create save directories
    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Project root: {project_root}")
    print(f"Loading data from: {DATA_DIR}")
    print(f"Saving train data to: {TRAIN_DIR}")
    print(f"Saving test data to: {TEST_DIR}")
    
    # Create dataset
    dataset = BirdSongDataset(DATA_DIR, CATEGORIES, IMG_SIZE)
    
    try:
        # Load data
        X, y = dataset.load_data()
        
        # Split and preprocess data
        (X_train, y_train), (X_test, y_test) = preprocess_data(X, y)
        
        # Save train data
        dataset.save_data(X_train, y_train, TRAIN_DIR)
        print(f"Saved {len(X_train)} training samples")
        
        # Save test data
        dataset.save_data(X_test, y_test, TEST_DIR)
        print(f"Saved {len(X_test)} test samples")
        
        # Print class distribution
        for split_name, y_data in [("Train", y_train), ("Test", y_test)]:
            print(f"\n{split_name} set class distribution:")
            for category, count in zip(CATEGORIES, np.bincount(y_data)):
                print(f"{category}: {count} samples")
        
    except Exception as e:
        print(f"Error processing data: {e}")
        raise

if __name__ == "__main__":
    main()