function [syllables, time_points] = syllable_cut(signal, fs, min_length, max_length)
    arguments
        signal (:,1) double
        fs (1,1) double {mustBePositive}
        min_length (1,1) double {mustBePositive}
        max_length (1,1) double {mustBePositive}
    end
    
    % Find last non-zero sample - this is useful from old implementation
    last_nonzero = find(signal ~= 0, 1, 'last');
    signal = signal(1:last_nonzero);
    
    % Calculate power envelopes
    power_short = filter_utils.get_power_envelope(signal, constants.SHORT_WINDOW_MS, fs);
    power_long = filter_utils.get_power_envelope(signal, constants.LONG_WINDOW_MS, fs);
    
    % Get boundaries with minimum space requirement
    boundaries = detect_boundaries(power_short, power_long, fs);
    
    % Extract syllables
    [syllables, time_points] = extract_syllables(signal, boundaries, min_length, max_length, fs);
end

function boundaries = detect_boundaries(power_short, power_long, fs)
    % The old implementation's approach of keeping minimum space is actually important
    % We should incorporate it while keeping our cleaner detection logic
    
    % First detect threshold crossings (our original approach is good here)
    threshold = 0.01 * max(power_long);  % Using original 1/100 threshold
    detected = power_short > (power_long + threshold);
    
    % Find initial boundaries
    initial_bounds = find(diff([0; detected; 0]));
    
    % Now add minimum space requirement (from old implementation)
    min_space = round((constants.MIN_SPACE_MS/1000) * fs);
    
    % Split into start/end pairs
    starts = initial_bounds(1:2:end);
    ends = initial_bounds(2:2:end);
    
    % Filter based on minimum space
    valid_segments = true(length(starts), 1);
    for i = 1:(length(starts)-1)
        if (starts(i+1) - ends(i)) < min_space
            valid_segments(i) = false;
        end
    end
    
    % Reconstruct boundaries
    boundaries = reshape([starts(valid_segments); ends(valid_segments)], [], 1);
end

function [syllables, time_points] = extract_syllables(signal, boundaries, min_length, max_length, fs)
    % Convert lengths to samples
    min_samples = round((min_length/1000) * fs);
    max_samples = round((max_length/1000) * fs);
    
    num_segments = floor(length(boundaries)/2);
    syllables = [];
    time_points = [];
    
    for i = 1:num_segments
        start_idx = boundaries(2*i-1);
        end_idx = boundaries(2*i);
        
        % Check length requirements
        if (end_idx - start_idx)/fs > min_length/1000
            segment = signal(start_idx:end_idx);
            
            % Cut to minimum length (removing padding concept)
            if length(segment) > min_samples
                segment = segment(1:min_samples);
            end
            
            % Store syllable
            syllables = [syllables, segment];
            time_points = [time_points, [start_idx; end_idx]/fs];
        end
    end
end