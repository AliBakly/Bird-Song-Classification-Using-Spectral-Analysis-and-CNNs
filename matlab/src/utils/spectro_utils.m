classdef spectro_utils
    % Utility functions for spectrogram generation and processing
    
    methods (Static)
        function [S, f, t] = compute_spectrogram(signal, window, overlap, nfft, fs)
            % Compute spectrogram with given parameters
            %
            % Parameters:
            %   signal: Input signal
            %   window: Window length
            %   overlap: Overlap between windows
            %   nfft: Number of FFT points
            %   fs: Sampling frequency
            %
            % Returns:
            %   S: Spectrogram matrix
            %   f: Frequency vector
            %   t: Time vector
            
            [S, f, t] = spectrogram(signal, window, overlap, nfft, fs, 'yaxis');
        end
        
        function fig = create_spectrogram_figure(signal, params)
            % Create spectrogram figure with standard settings
            %
            % Parameters:
            %   signal: Input signal
            %   params: Struct with fields window, overlap, nfft, fs
            %
            % Returns:
            %   fig: Figure handle
            
            fig = figure('Visible', 'off');
            
            % Generate spectrogram
            spectrogram(signal, params.window, params.overlap, ...
                params.nfft, params.fs, 'yaxis');
            
            % Configure appearance
            set(gca, 'Visible', 'off');
            colorbar('off');
        end
        
        function configure_spectrogram_plot(colormap_name)
            % Configure spectrogram plot appearance
            %
            % Parameters:
            %   colormap_name: Name of colormap to use (default: 'jet')
            
            if nargin < 1
                colormap_name = 'jet';
            end
            
            colormap(colormap_name);
            axis tight;
            box off;
        end
    end
end