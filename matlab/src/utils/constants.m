% utils/constants.m
classdef constants
    % Constants used throughout the bird song analysis pipeline
    
    properties (Constant)
        % Audio processing
        DEFAULT_FS = 22050        % Default sampling frequency
        MIN_FREQ = 1000          % Minimum frequency for bandpass
        MAX_FREQ = 10000         % Maximum frequency for bandpass
        
        % Syllable detection
        MIN_LENGTH_MS = 100      % Minimum syllable length (ms)
        MAX_LENGTH_MS = 300      % Maximum syllable length (ms)
        MIN_SPACE_MS = 50        % Minimum space between syllables (ms)
        
        % Power envelope calculation
        SHORT_WINDOW_MS = 48     % Short window for power calculation
        LONG_WINDOW_MS = 50     % Long window for power calculation
        
        % Spectrogram parameters
        WINDOW_LENGTH = 128      % Window length
        NFFT = 512              % Number of FFT points
        OVERLAP = 120           % Overlap between windows
        
        % File formats
        AUDIO_FORMAT = '.mp3'
        IMAGE_FORMAT = '.jpg'
        
        % Plotting
        DEFAULT_COLORMAP = 'default'
        FIGURE_DPI = 300        % Resolution for saved figures
    end
end