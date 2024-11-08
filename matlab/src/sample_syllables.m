function syllables = sample_syllables(detected_syllables, max_syllables)
    num_syllables = size(detected_syllables, 2);
    if num_syllables > max_syllables
        indices = randperm(num_syllables, max_syllables);
        syllables = detected_syllables(:, indices);
    else
        syllables = detected_syllables;
    end
end