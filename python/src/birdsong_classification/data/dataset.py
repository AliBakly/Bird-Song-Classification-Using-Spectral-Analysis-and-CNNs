from pathlib import Path
import numpy as np
import cv2
from tqdm import tqdm
from typing import List, Tuple, Optional
import pickle

class BirdSongDataset:
    """Dataset class for bird song spectrograms"""
    
    def __init__(self, data_dir: str, categories: List[str], img_size: int = 150):
        """
        Initialize dataset
        
        Args:
            data_dir: Path to data directory
            categories: List of bird species categories
            img_size: Size to resize images to (square)
        """
        self.data_dir = Path(data_dir)
        self.categories = categories
        self.img_size = img_size
        self.data = []
        
    def load_data(self, prediction_mode=False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and preprocess all images
        
        Args:
            prediction_mode: If True, load all images from root directory without categories
        
        Returns:
            X: Image data of shape (n_samples, img_size, img_size, 3)
            y: Labels of shape (n_samples,)
        """
        print("Loading data...")
        X = []
        y = []
        
        if prediction_mode:
            # Load directly from root directory
            print(f"Loading from {self.data_dir}")
            for img_path in tqdm(list(self.data_dir.glob('*.jpg')), desc="Loading images"):
                try:
                    img = cv2.imread(str(img_path))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (self.img_size, self.img_size))
                    X.append(img)
                    y.append(0)  # Dummy label
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
                    continue
        else:
            # Original category-based loading
            for category in self.categories:
                class_num = self.categories.index(category)
                path = self.data_dir / category
                print(path)
                for img_path in tqdm(list(path.glob('*.jpg')), desc=f"Loading {category}"):
                    try:
                        img = cv2.imread(str(img_path))
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (self.img_size, self.img_size))
                        X.append(img)
                        y.append(class_num)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
                        continue
                    
        return np.array(X), np.array(y)
    
    def save_data(self, X: np.ndarray, y: np.ndarray, save_dir: str):
        """
        Save processed data to pickle files
        
        Args:
            X: Image data
            y: Labels
            save_dir: Directory to save pickle files
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        with open(save_dir / "X.pickle", "wb") as f:
            pickle.dump(X, f)
            
        with open(save_dir / "y.pickle", "wb") as f:
            pickle.dump(y, f)
            
    @staticmethod
    def load_pickle_data(data_dir: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load data from pickle files
        
        Args:
            data_dir: Directory containing pickle files
            
        Returns:
            X: Image data
            y: Labels
        """
        data_dir = Path(data_dir)
        
        with open(data_dir / "X.pickle", "rb") as f:
            X = pickle.load(f)
            
        with open(data_dir / "y.pickle", "rb") as f:
            y = pickle.load(f)
            
        return X, y
