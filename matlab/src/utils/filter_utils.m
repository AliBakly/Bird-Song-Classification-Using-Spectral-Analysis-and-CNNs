classdef filter_utils
    % Utility functions for signal filtering
    
    methods (Static)
        function signal = apply_bandpass(signal, fs, freq_range)
            % Apply bandpass filter to signal
            %
            % Parameters:
            %   signal: Input signal
            %   fs: Sampling frequency
            %   freq_range: [low_freq, high_freq] filter range
            %
            % Returns:
            %   signal: Filtered signal
            
            if ~isempty(signal)
                signal = bandpass(signal, freq_range, fs);
            end
        end
        
        function envelope = get_power_envelope(signal, window_length, fs)
            % Calculate power envelope using moving average
            %
            % Parameters:
            %   signal: Input signal
            %   window_length: Window length in milliseconds
            %   fs: Sampling frequency
            %
            % Returns:
            %   envelope: Power envelope
            
            % Convert window length from ms to samples
            window_samples = round((window_length/1000) * fs);
            
            % Create window
            window = ones(window_samples, 1) / window_samples;
            
            % Calculate power and smooth
            envelope = conv(signal.^2, window, 'same');
        end
        
        function smooth_signal = smooth(signal, window_length)
            % Smooth signal using moving average
            %
            % Parameters:
            %   signal: Input signal
            %   window_length: Window length in samples
            %
            % Returns:
            %   smooth_signal: Smoothed signal
            
            window = ones(window_length, 1) / window_length;
            smooth_signal = conv(signal, window, 'same');
        end
    end
end