% generate_spectro.m
function generate_spectrograms(syllables, params, output_dir)
    arguments
        syllables cell
        params struct
        output_dir (1,1) string
    end
    
    % Use constants for default parameters
    if ~isfield(params, 'window'), params.window = constants.WINDOW_LENGTH; end
    if ~isfield(params, 'nfft'), params.nfft = constants.NFFT; end
    if ~isfield(params, 'overlap'), params.overlap = constants.OVERLAP; end
    if ~isfield(params, 'fs'), params.fs = constants.DEFAULT_FS; end
    
    % Create output directory if needed
    if ~exist(output_dir, 'dir')
        mkdir(output_dir);
    end
    
    % Process syllables in parallel
    parfor i = 1:length(syllables)
        for j = 1:length(syllables{i}(1,:))
            try
                generate_single_spectrogram(syllables{i}(:,j), params, output_dir, i, j);
                fprintf('Processed spectrogram for audio file %d, syllable %d\n', i, j);
            catch ME
                warning('Failed to generate spectrogram %d-%d: %s', i, j, ME.message);
            end
        end
    end
end

function generate_single_spectrogram(syllable, params, output_dir, i, j)
    % Use utility functions to create spectrogram
    fig = spectro_utils.create_spectrogram_figure(syllable, params);
    spectro_utils.configure_spectrogram_plot(constants.DEFAULT_COLORMAP);
    
    % Save spectrogram
    filename = fullfile(output_dir, sprintf('%d%d%s', i, j, constants.IMAGE_FORMAT));
    exportgraphics(fig, filename, 'Resolution', constants.FIGURE_DPI);
    
    close(fig);
end