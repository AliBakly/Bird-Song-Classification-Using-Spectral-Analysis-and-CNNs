# MATLAB Documentation

## 1. Introduction

### **Birdsong Classification Pipeline (MATLAB)**

The MATLAB component of the Birdsong Classification project processes raw audio files, extracts syllables, and generates spectrograms. This preprocessing step prepares the data for classification using a Convolutional Neural Network (CNN) in Python.

**Key Features:**
- **Audio Processing:** Resampling, bandpass filtering, and syllable extraction.
- **Spectrogram Generation:** Converts audio syllables into spectrogram images suitable for CNN input.
- **User Interface:** Interactive UI (`SyllablePlayer`) for listening to extracted syllables, aiding in debugging and verification.

## 2. Directory Structure

```
- matlab/
  - main.m
  - config.m
  - src/
    - generate_spectrograms.m
    - preprocessing.m
    - process_single_audio.m
    - sample_syllables.m
    - syllable_cut.m
    - utils/
      - audio_utils.m
      - constants.m
      - filter_utils.m
      - spectro_utils.m
      - SyllablePlayer.m
```

**Description:**
- **main.m:** Entry point for the MATLAB pipeline.
- **config.m:** Configuration parameters for processing different bird species.
- **src/:** Core scripts for processing and spectrogram generation.
- **utils/:** Utility functions and constants supporting the main scripts.

## 3. Installation and Setup

### **Prerequisites:**
- **MATLAB:** Version R2020a or later.
- **Toolboxes:**
  - Signal Processing Toolbox
  - Parallel Computing Toolbox (for `parfor` loops)

### **Setup Instructions:**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/birdsong-classification.git
   ```

2. **Navigate to the MATLAB Directory:**
   ```bash
   cd birdsong-classification/matlab
   ```

3. **Configure Constants:**
   - Open `src/utils/constants.m` and adjust parameters as needed (e.g., sampling rate, frequency bands).

## 4. Usage Guide

### **Running the Pipeline:**

1. **Prepare Raw Data:**
   - Organize your `.mp3` audio files in `data/raw/`, categorized by species.

2. **Execute the Main Script:**
   - Open MATLAB.
   - Navigate to the `matlab` directory.
   - Run the `main` function:
     ```matlab
     main
     ```

3. **Process Overview:**
   - **Configuration:** `config.m` sets parameters based on species.
   - **Preprocessing:** Extracts syllables from audio files.
   - **Spectrogram Generation:** Converts syllables into spectrogram images.
   - **Output:** Spectrograms are saved in `data/spectrograms/`, organized by species.

### **Debugging:**

- **Enable Syllable Listening:**
  - In `config.m`, set:
    ```matlab
    cfg.debug.listen_syllables = true;
    ```
  - This launches the `SyllablePlayer` UI, allowing you to play and inspect extracted syllables.

*Optional: Add a screenshot of the SyllablePlayer UI.*

![SyllablePlayer UI](docs/images/syllable_player_ui.png)

*Replace `docs/images/syllable_player_ui.png` with your actual image path.*

## 5. Function Overview

### **Main Scripts:**

- **main.m:** Initializes the pipeline, iterates through species directories, and orchestrates processing.
- **config.m:** Generates configuration settings tailored to each species.
- **generate_spectrograms.m:** Converts syllables into spectrogram images using parallel processing.
- **preprocessing.m:** Handles audio loading, filtering, syllable detection, and sampling.
- **process_single_audio.m:** Processes individual audio files for syllable extraction and spectrogram generation.
- **sample_syllables.m:** Selects a subset of syllables for spectrogram generation.
- **syllable_cut.m:** Segments audio signals into individual syllables based on power envelope analysis.

### **Utility Scripts:**

- **audio_utils.m:** Functions for loading, resampling, normalizing audio, and calculating duration.
- **constants.m:** Centralizes constant values used across scripts (e.g., sampling rate, filter ranges).
- **filter_utils.m:** Provides filtering functions and power envelope calculations.
- **spectro_utils.m:** Handles spectrogram computation and visualization settings.
- **SyllablePlayer.m:** Implements an interactive UI for playing and visualizing syllables.

*For detailed implementations, refer to the respective `.m` files in the repository.*

## 6. Examples

### **Example 1: Running the Pipeline**

```matlab
% Navigate to the matlab directory
cd /path/to/birdsong-classification/matlab

% Run the main script
main
```

**Expected Output:**
- Spectrogram images saved in `data/spectrograms/<species_name>/`.
- Console logs indicating processing progress.

### **Example 2: Custom Configuration for Debugging**

1. **Enable Syllable Listening:**
   ```matlab
   cfg.debug.listen_syllables = true;
   ```

2. **Run the Main Script:**
   ```matlab
   main
   ```

3. **Interact with the SyllablePlayer UI:**
   - Play, pause, and navigate through syllables.
   - Visualize waveform and spectrogram of each syllable.

*Optional: Add a screenshot of the SyllablePlayer in action.*

## 7. Troubleshooting

- **Missing Raw Data Directory:**
  - **Error:** Raw data directory does not exist.
  - **Solution:** Ensure `data/raw/` contains species-specific folders with `.mp3` files.

- **No Species Directories Found:**
  - **Error:** No species directories found in `data/raw/`.
  - **Solution:** Verify species directories are correctly named and placed in `data/raw/`.

- **Spectrogram Generation Failures:**
  - **Error:** Issues during spectrogram creation.
  - **Solution:** Check `constants.m` for correct `DEFAULT_COLORMAP`, `IMAGE_FORMAT`, and `FIGURE_DPI` settings.

- **SyllablePlayer UI Not Launching:**
  - **Error:** UI does not appear when `listen_syllables` is enabled.
  - **Solution:** Ensure `cfg.debug.listen_syllables` is set to `true` and syllables are successfully extracted.

- **Audio Playback Issues:**
  - **Error:** Unable to play syllables in `SyllablePlayer`.
  - **Solution:** Confirm system audio is functional and MATLAB has access to audio hardware.