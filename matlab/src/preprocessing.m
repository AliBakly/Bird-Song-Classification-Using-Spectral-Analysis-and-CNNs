function [syllables, params] = preprocessing(config)    
    % Initialize output containers
    syllables = cell(1, config.num_files);
    params = struct();
    
    % Process each audio file
    counter = 1;
    for file_idx = 1:config.num_files
        try
            % Load and preprocess audio using utility functions
            [signal, fs] = load_and_preprocess_audio(file_idx, config);
            
            % Detect syllables
            
            [detected_syllables, time_points] = syllable_cut(signal, ...
                config.target_fs, config.min_length, config.max_length);
            % Sample random syllables
            syllables{file_idx} = sample_syllables(detected_syllables, config.max_syllables);
            fprintf('Processed %d audio files\n', counter);
            counter = counter + 1;
        catch ME
            warning('Failed to process file %d: %s', file_idx, ME.message);
            continue;
        end
    end
    
    % Remove empty cells
    syllables = syllables(~cellfun('isempty', syllables));
    
    % Store parameters
    params = config;

end

function [signal, fs] = load_and_preprocess_audio(file_idx, config)
    filename = sprintf('%d%s', file_idx, constants.AUDIO_FORMAT);
    filepath = fullfile(config.input_dir, filename);
    
    % Use utility functions for audio processing
    [signal, fs] = audio_utils.load_audio(filepath);
    signal = audio_utils.resample_audio(signal, fs, config.target_fs);
    signal = filter_utils.apply_bandpass(signal, config.target_fs, config.filter_band);
end
