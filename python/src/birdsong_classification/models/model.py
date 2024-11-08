import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dense, Dropout, 
    Activation, Flatten, BatchNormalization
)
import numpy as np
from tensorflow.keras import regularizers
from tensorflow.keras.optimizers import Adam
from typing import Tuple

class BirdSongClassifier:
    """CNN model for bird song classification"""
    
    def __init__(self, input_shape: Tuple[int, int, int], num_classes: int = 3):
        """
        Initialize model
        
        Args:
            input_shape: Shape of input images (height, width, channels)
            num_classes: Number of bird species to classify
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_model()
        
    def _build_model(self) -> Sequential:
        """
        Build the CNN architecture
        
        Returns:
            Compiled Keras model
        """
        model = Sequential([
            # First Conv Block
            Conv2D(32, (3, 3), 
                  input_shape=self.input_shape,
                  kernel_regularizer=regularizers.l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            
            # Second Conv Block
            Conv2D(32, (3, 3),
                  kernel_regularizer=regularizers.l2(0.001)),
            BatchNormalization(),
            Activation('relu'),
            MaxPooling2D(pool_size=(2, 2)),
            
            # Flatten and Dense Layers
            Flatten(),
            Dense(16, kernel_regularizer=regularizers.l2(0.001)),
            Dropout(0.5),
            Dense(self.num_classes),
            Activation('softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.0001),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self, 
              X_train: np.ndarray, 
              y_train: np.ndarray,
              validation_split: float = 0.1,
              batch_size: int = 64,
              epochs: int = 3,
              verbose: int = 1) -> tf.keras.callbacks.History:
        """
        Train the model
        
        Args:
            X_train: Training images
            y_train: Training labels
            validation_split: Fraction of data to use for validation
            batch_size: Batch size for training
            epochs: Number of epochs to train
            verbose: Verbosity mode
            
        Returns:
            Training history
        """
        return self.model.fit(
            X_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            validation_split=validation_split,
            verbose=verbose
        )
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Tuple[float, float]:
        """
        Evaluate model on test data
        
        Args:
            X_test: Test images
            y_test: Test labels
            
        Returns:
            Tuple of (loss, accuracy)
        """
        return self.model.evaluate(X_test, y_test)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data
        
        Args:
            X: Input images
            
        Returns:
            Predicted probabilities for each class
        """
        return self.model.predict(X)
    
    def save(self, filepath: str):
        """Save model to file"""
        self.model.save(filepath)
    
    @classmethod
    def load(cls, filepath: str) -> 'BirdSongClassifier':
        """Load model from file"""
        model = tf.keras.models.load_model(filepath)
        instance = cls(model.input_shape[1:])
        instance.model = model
        return instance