classdef audio_utils
    % Utility functions for audio processing
    
    methods (Static)
        function [signal, fs] = load_audio(filepath)
            % Load audio file and convert to mono if stereo
            %
            % Parameters:
            %   filepath: Path to audio file
            %
            % Returns:
            %   signal: Audio signal (mono)
            %   fs: Sampling frequency
            
            [signal, fs] = audioread(filepath);
            
            % Convert to mono if stereo
            if size(signal, 2) > 1
                signal = signal(:, 1);
            end
        end
        
        function signal = resample_audio(signal, original_fs, target_fs)
            % Resample audio signal to target frequency
            %
            % Parameters:
            %   signal: Input audio signal
            %   original_fs: Original sampling frequency
            %   target_fs: Target sampling frequency
            %
            % Returns:
            %   signal: Resampled signal
            
            if original_fs ~= target_fs
                signal = resample(signal, target_fs, original_fs);
            end
        end
        
        function signal = normalize_signal(signal)
            % Normalize audio signal to range [-1, 1]
            %
            % Parameters:
            %   signal: Input audio signal
            %
            % Returns:
            %   signal: Normalized signal
            
            if ~isempty(signal)
                signal = signal / max(abs(signal));
            end
        end
        
        function duration_sec = get_duration(signal, fs)
            % Get duration of audio signal in seconds
            %
            % Parameters:
            %   signal: Input audio signal
            %   fs: Sampling frequency
            %
            % Returns:
            %   duration_sec: Duration in seconds
            
            duration_sec = length(signal) / fs;
        end
    end
end