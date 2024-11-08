% matlab/src/process_single_audio.m
function process_single_audio(audio_path, output_dir)
    % Create default config
    cfg = config('placeholder');
    
    % Process audio
    [signal, fs] = audio_utils.load_audio(audio_path);
    signal = audio_utils.resample_audio(signal, fs, cfg.target_fs);
    signal = filter_utils.apply_bandpass(signal, cfg.target_fs, cfg.filter_band);
    
    % Extract syllables
    [detected_syllables, ~] = syllable_cut(signal, ...
        cfg.target_fs, cfg.min_length, cfg.max_length);
    
    syllables = {sample_syllables(detected_syllables, cfg.max_syllables)};
    % Generate spectrograms
    generate_spectrograms(syllables, cfg.spectro, output_dir);
end