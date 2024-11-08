function main()
    % MAIN Main script for bird song analysis pipeline.
    %
    % This script iterates through each species directory in the raw data folder,
    % processes the audio files to extract syllables, and generates spectrograms
    % for each species. Spectrograms are saved in species-specific output directories.

    % Add necessary paths
    addpath(genpath(fullfile(pwd, 'src', 'utils')));
    addpath(genpath(fullfile(pwd, 'src')));

    % Main script execution
    try
        fprintf('Starting bird song analysis pipeline...\n');
        
        % Define raw data directory
        raw_data_dir = fullfile('..', 'data', 'raw');
        
        % Verify that raw data directory exists
        if ~exist(raw_data_dir, 'dir')
            error('Raw data directory "%s" does not exist.', raw_data_dir);
        end
        
        % List all species directories in raw data
        species_dirs = dir(raw_data_dir);
        species_dirs = species_dirs([species_dirs.isdir]); % Keep only directories
        species_dirs = species_dirs(~ismember({species_dirs.name}, {'.', '..'})); % Remove '.' and '..'
        
        % Check if there are any species directories
        if isempty(species_dirs)
            error('No species directories found in "%s".', raw_data_dir);
        end
        
        % Iterate through each species directory
        for i = 1:length(species_dirs)
            species_name = species_dirs(i).name;
            fprintf('\nProcessing species: %s\n', species_name);
            
            try
                % Generate configuration for the current species
                cfg = config(species_name);
                
                % Create output directory if it doesn't exist
                if ~exist(cfg.output_dir, 'dir')
                    mkdir(cfg.output_dir);
                    fprintf('Created output directory: %s\n', cfg.output_dir);
                else
                    fprintf('Output directory already exists: %s\n', cfg.output_dir);
                end
                
                % Process audio files and extract syllables
                fprintf('Processing audio files...\n');
                [syllables, params] = preprocessing(cfg);
                fprintf('Processed %d files, extracted syllables\n', length(syllables));
                
                % Launch syllable player if debug mode is enabled
                if isfield(cfg, 'debug') && isfield(cfg.debug, 'listen_syllables') && cfg.debug.listen_syllables
                    SyllablePlayer.launch(syllables, cfg.target_fs);
          
                end

                % Generate spectrograms
                fprintf('Generating spectrograms...\n');
                generate_spectrograms(syllables, cfg.spectro, cfg.output_dir);
                
                fprintf('Completed processing for species: %s\n', species_name);
                
            catch speciesME
                fprintf('Error processing species "%s": %s\n', species_name, speciesME.message);
                fprintf('Continuing to next species.\n');
                % Optionally, log the error to a file for later review
                continue;  % Proceed to the next species
            end
        end
        
        fprintf('\nAll species processed successfully!\n');
        
    catch ME
        fprintf('Fatal Error: %s\n', ME.message);
        fprintf('Stack trace:\n');
        disp(getReport(ME, 'extended'));
    end
end
