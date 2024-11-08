# Bird Song Classification Using Spectral Analysis and CNNs

---

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Installation](#installation)
    - [MATLAB Setup](#matlab-setup)
    - [Python Setup](#python-setup)
4. [Usage](#usage)
    - [1. Preprocessing with MATLAB](#1-preprocessing-with-matlab)
    - [2. Data Preparation with Python](#2-data-preparation-with-python)
    - [3. Training the Model](#3-training-the-model)
    - [4. Evaluating the Model](#4-evaluating-the-model)
    - [5. Making Predictions](#5-making-predictions)
5. [Results](#results)
6. [Contributing](#contributing)
7. [License](#license)
8. [Contact](#contact)

---

## Overview

The **Birdsong Classification** project aims to accurately classify different bird species based solely on their vocalizations. Specifically, the project focuses on three species:

- **Common Chaffinch** (*Fringilla coelebs*)
- **House Sparrow** (*Passer domesticus*)
- **Eurasian Blue Tit** (*Cyanistes caeruleus*)

The classification process involves two main components:

1. **Preprocessing (MATLAB):** Processes raw audio files, extracts syllables, and generates spectrograms.
2. **Classification (Python):** Utilizes Convolutional Neural Networks (CNN) to classify the generated spectrograms.

This approach leverages signal processing techniques in MATLAB to prepare the data, followed by machine learning methodologies in Python to achieve high classification accuracy.

*Image here*
---

## Directory Structure

```
birdsong-classification/
├── data/
│   ├── processed/
│   │   ├── test/
│   │   │   ├── X.pickle
│   │   │   └── y.pickle
│   │   └── train/
│   │       ├── X.pickle
│   │       └── y.pickle
│   ├── raw/
│   │   ├── common_chaffinch/
│   │   │   ├── 1.mp3
│   │   │   ├── 10.mp3
│   │   │   └── 100.mp3
│   │   ├── eurasian_blue_tit/
│   │   │   ├── 1.mp3
│   │   │   ├── 10.mp3
│   │   │   └── 100.mp3
│   │   └── house_sparrow/
│   │       ├── 1.mp3
│   │       ├── 10.mp3
│   │       └── 100.mp3
│   └── spectrograms/
│       ├── common_chaffinch/
│       │   ├── 1001.jpg
│       │   ├── 1002.jpg
│       │   └── 1003.jpg
│       ├── eurasian_blue_tit/
│       │   ├── 1001.jpg
│       │   ├── 1002.jpg
│       │   └── 1003.jpg
│       └── house_sparrow/
│           ├── 1001.jpg
│           ├── 1002.jpg
│           └── 1003.jpg
├── matlab/
│   ├── config.m
│   ├── main.m
│   ├── MATLAB_Documentation.md
│   ├── src/
│   │   ├── generate_spectrograms.m
│   │   ├── preprocessing.m
│   │   ├── process_single_audio.m
│   │   ├── sample_syllables.m
│   │   ├── syllable_cut.m
│   │   └── utils/
│   │       ├── audio_utils.m
│   │       ├── constants.m
│   │       ├── filter_utils.m
│   │       ├── spectro_utils.m
│   │       └── SyllablePlayer.m
├── models/
│   ├── birdsong_classifier.h5
│   └── train_stats.npz
├── python/
│   ├── setup.py
│   ├── Python_Documentation.md
│   ├── src/
│   │   └── birdsong_classification/
│   │       ├── __init__.py
│   │       ├── data/
│   │       │   ├── dataset.py
│   │       │   ├── download_bird_songs.py
│   │       │   ├── prepare_data.py
│   │       │   └── preprocessing.py
│   │       ├── evaluation/
│   │       │   ├── evaluate.py
│   │       │   └── metrics.py
│   │       ├── models/
│   │       │   ├── model.py
│   │       │   └── train.py
│   │       ├── predict.py
│   │       └── utils/
│   │           ├── path_utils.py
│   │           └── visualization.py
├── results/
│   ├── confusion_matrix.png
│   ├── species_accuracy.png
│   └── training_history.png
├── README.md
└── project_structure.text
```

## Installation

### MATLAB Setup
*See the MATLAB documentation for more details.*

**Prerequisites:**

- **MATLAB:** Version R2020a or later.
- **Toolboxes:**
  - Signal Processing Toolbox
  - Parallel Computing Toolbox (for `parfor` loops)

**Setup Instructions:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/birdsong-classification.git
   ```

2. **Navigate to the MATLAB Directory:**
   ```bash
   cd birdsong-classification/matlab
   ```

3. **Configure Constants:**
   - Open `src/utils/constants.m` in MATLAB.
   - Adjust parameters as needed (e.g., sampling rate, frequency bands).

4. **Verify MATLAB Toolboxes:**
   - Ensure that the required toolboxes are installed and accessible.

---

### Python Setup
*See the Python documentation for more details.*

**Prerequisites:**

- **Python:** Version 3.7 or higher.
- **MATLAB:** Required for prediction functionalities.
- **MATLAB Engine API for Python:** Must be installed separately.

**Setup Instructions:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/birdsong-classification.git
   ```

2. **Navigate to the Python Directory:**
   ```bash
   cd birdsong-classification/python
   ```

3. **Install Dependencies:**
   ```bash
   pip install -e .
   ```
   *This command installs the package in editable mode along with all required dependencies.*

4. **Install MATLAB Engine API for Python:**
   - **Locate MATLAB Engine API:**
     - Navigate to the MATLAB Engine directory, typically found at:
       ```
       <MATLAB_INSTALL_DIR>/extern/engines/python
       ```
   - **Install the Engine:**
     ```bash
     cd <MATLAB_INSTALL_DIR>/extern/engines/python
     python setup.py install
     ```
   - **Verify Installation:**
     ```python
     import matlab.engine
     ```
     *If no errors are thrown, the installation was successful.*

5. **Verify Installation:**
   ```bash
   python -m birdsong_classification.utils.path_utils
   ```
   *Ensure no errors are thrown, indicating successful installation.*

---

## Usage

### 1. Preprocessing with MATLAB

**Steps:**

1. **Organize Raw Data:**
   - Place your `.mp3` audio files in `data/raw/`, categorized by species:
     ```
     data/raw/
     ├── common_chaffinch/
     │   ├── 1.mp3
     │   ├── 10.mp3
     │   └── 100.mp3
     ├── eurasian_blue_tit/
     │   ├── 1.mp3
     │   ├── 10.mp3
     │   └── 100.mp3
     └── house_sparrow/
         ├── 1.mp3
         ├── 10.mp3
         └── 100.mp3
     ```
    - Or use the `download_bird_songs.py` script.

2. **Run the Main Script:**
   - Open MATLAB.
   - Navigate to the `matlab` directory.
   - Execute the `main` function:
     ```matlab
     main
     ```

3. **Process Overview:**
   - **Configuration:** `config.m` sets parameters based on species.
   - **Preprocessing:** Extracts syllables from audio files.
   - **Spectrogram Generation:** Converts syllables into spectrogram images.
   - **Output:** Spectrograms are saved in `data/spectrograms/`, organized by species.

4. **Debugging (Optional):**
   - **Enable Syllable Listening:**
     - In `config.m`, set:
       ```matlab
       cfg.debug.listen_syllables = true;
       ```
     - This launches the `SyllablePlayer` UI, allowing you to play and inspect extracted syllables.

*Include a screenshot of the SyllablePlayer UI if available.*

![SyllablePlayer UI](docs/images/syllable_player_ui.png)

---

### 2. Data Preparation with Python

**Steps:**

1. **Navigate to the Python Directory:**
   ```bash
   cd birdsong-classification/python
   ```

2. **Download Additional Bird Songs (If Needed):**
   - Use the `download_bird_songs.py` script to fetch more audio files.
   - **Command:**
     ```bash
     python -m birdsong_classification.data.download_bird_songs --species "Eurasian blue tit,House sparrow,Common chaffinch" --quality "A" --num-files 300
     ```
   - **Parameters:**
     - `--species`: Comma-separated list of bird species.
     - `--quality`: Recording quality (A-E).
     - `--num-files`: Number of files to download per species.

3. **Prepare and Preprocess Data:**
   - Preprocess the downloaded data to generate training and testing datasets.
   - **Command:**
     ```bash
     python -m birdsong_classification.data.prepare_data
     ```
   - **Process Overview:**
     - **Loading Data:** Loads spectrogram images and labels.
     - **Splitting Data:** Divides data into training and testing sets.
     - **Normalization:** Standardizes data based on training statistics.
     - **Saving Processed Data:** Stores processed datasets as `.pickle` files.

---

### 3. Training the Model

**Steps:**

1. **Navigate to the Python Directory:**
   ```bash
   cd birdsong-classification/python
   ```

2. **Train the CNN Model:**
   - Use the `train.py` script to train the model.
   - **Command:**
     ```bash
     python -m birdsong_classification.models.train
     ```
   - **Process Overview:**
     - **Loading Data:** Imports training data from `data/processed/train/`.
     - **Model Initialization:** Builds the CNN architecture.
     - **Training:** Fits the model on training data for a specified number of epochs.
     - **Saving Model:** Stores the trained model in the `models/` directory.
     - **Visualization:** Generates plots for training history.

---

### 4. Evaluating the Model

**Steps:**

1. **Navigate to the Python Directory:**
   ```bash
   cd birdsong-classification/python
   ```

2. **Evaluate the Trained Model:**
   - Use the `evaluate.py` script to assess model performance.
   - **Command:**
     ```bash
     python -m birdsong_classification.evaluation.evaluate
     ```
   - **Process Overview:**
     - **Loading Test Data:** Imports testing data from `data/processed/test/`.
     - **Model Loading:** Retrieves the trained model from `models/`.
     - **Evaluation:** Computes overall accuracy and loss.
     - **Per-Species Evaluation:** Calculates accuracy for each bird species.
     - **Confusion Matrix:** Generates and saves a confusion matrix plot.
     - **Classification Report:** Outputs precision, recall, and F1 scores.

---

### 5. Making Predictions

**Steps:**

1. **Navigate to the Python Directory:**
   ```bash
   cd birdsong-classification/python
   ```

2. **Predict Bird Species from New Audio Files:**
   - Use the `predict.py` script to classify new audio samples.
   - **Command:**
     ```bash
     python -m birdsong_classification.predict path/to/new_audio.mp3
     ```
   - **Process Overview:**
     - **Audio Processing:** Uses MATLAB to extract syllables and generate spectrograms.
     - **Loading Model:** Imports the trained CNN model.
     - **Prediction:** Classifies the bird species and outputs confidence scores.

---

## Results

The project achieved a high classification accuracy of **96.31%** using the following configuration:

- **Model:** Model 2 with standardized RGB spectrogram images and syllable lengths set to 100ms.
- **CNN Architecture:** 
  - **Convolutional Layers:** 64 and 128 filters with ReLU activation.
  - **Pooling Layers:** $3 \times 3$ max-pooling to reduce computational complexity.
  - **Fully Connected Layers:** Increased from 32 to 128 neurons with dropout regularization.
- **Training Parameters:**
  - **Optimizer:** Adam with a learning rate of 0.0001.
  - **Epochs:** 50
  - **Batch Size:** 64

**Confusion Matrix:**

![Confusion Matrix](docs/images/confusion_matrix.png)

*Interpretation:*

- **Common Chaffinch:** 98% accurately classified.
- **House Sparrow:** 100% accurately classified.
- **Eurasian Blue Tit:** 95% accurately classified.

**Training History:**

![Training History](docs/images/training_history.png)

*The training and validation accuracy steadily increased, while the loss decreased, indicating effective learning without significant overfitting.*

---
