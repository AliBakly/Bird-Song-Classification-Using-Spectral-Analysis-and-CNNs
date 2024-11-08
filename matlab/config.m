function cfg = config(species)
    % CONFIG Configuration parameters for bird song analysis.
    %
    % Syntax:
    %   cfg = config(species)
    %
    % Description:
    %   Generates a configuration structure for the specified bird species.
    %
    % Input Arguments:
    %   species - String specifying the bird species name (e.g., 'eurasian_blue_tit').
    %
    % Output Arguments:
    %   cfg - Configuration structure containing parameters for analysis.
    
    arguments
        species (1, :) char
    end
    
    % Validate species name
    if isempty(species)
        error('Species name cannot be empty.');
    end
    
    % Audio processing configuration
    cfg.input_dir = fullfile('..', 'data', 'raw', species);
    cfg.output_dir = fullfile('..', 'data', 'spectrograms', species);
    cfg.num_files = 300;  % Consider making this species-specific if needed
    
    % Use constants for standard parameters
    cfg.target_fs = constants.DEFAULT_FS;
    cfg.filter_band = [constants.MIN_FREQ, constants.MAX_FREQ];
    cfg.min_length = constants.MIN_LENGTH_MS;
    cfg.max_length = constants.MAX_LENGTH_MS;
    cfg.max_syllables = 5;
    
    % Spectrogram parameters
    cfg.spectro.window = constants.WINDOW_LENGTH;
    cfg.spectro.nfft = constants.NFFT;
    cfg.spectro.overlap = constants.OVERLAP;
    cfg.spectro.fs = constants.DEFAULT_FS;

    % True if you want to listen to the syllables (dedicated ui).
    cfg.debug.listen_syllables = false;  
end
