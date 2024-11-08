% matlab/src/utils/SyllablePlayer.m
classdef SyllablePlayer
    methods (Static)
        function launch(syllables, fs)
            % State variables in shared workspace
            current_file = 1;
            current_syllable = 1;
            is_playing = false;
            
            % Create the main figure
            fig = figure('Name', 'Syllable Player', ...
                        'Position', [100 100 800 600], ...
                        'MenuBar', 'none', ...
                        'NumberTitle', 'off', ...
                        'WindowStyle', 'modal');

            % Create UI Layout
            plot_panel = uipanel('Parent', fig, ...
                                'Position', [0.05 0.2 0.9 0.75]);
            
            % Create subplots
            waveform_ax = subplot(2,1,1, 'Parent', plot_panel);
            title(waveform_ax, 'Waveform');
            spec_ax = subplot(2,1,2, 'Parent', plot_panel);
            title(spec_ax, 'Spectrogram');
            
            % Control panel
            control_panel = uipanel('Parent', fig, ...
                                   'Position', [0.05 0.05 0.9 0.1]);
            
            % Previous button
            uicontrol('Parent', control_panel, ...
                      'Style', 'pushbutton', ...
                      'String', '⏮', ...
                      'Position', [50 10 60 30], ...
                      'Callback', @previous_syllable);
            
            % Play/Pause button
            play_btn = uicontrol('Parent', control_panel, ...
                                'Style', 'pushbutton', ...
                                'String', '▶', ...
                                'Position', [120 10 60 30], ...
                                'Callback', @toggle_play);
            
            % Next button
            uicontrol('Parent', control_panel, ...
                      'Style', 'pushbutton', ...
                      'String', '⏭', ...
                      'Position', [190 10 60 30], ...
                      'Callback', @next_syllable);
            
            % Information text
            info_text = uicontrol('Parent', control_panel, ...
                                 'Style', 'text', ...
                                 'Position', [260 10 200 30], ...
                                 'String', 'File 1, Syllable 1');
            
            % Close button
            uicontrol('Parent', control_panel, ...
                      'Style', 'pushbutton', ...
                      'String', '✖', ...
                      'Position', [470 10 60 30], ...
                      'Callback', @close_player);
            
            % Set keyboard callbacks
            set(fig, 'KeyPressFcn', @handle_key_press);
            
            % Initial display
            update_display();
            
            % Make figure visible
            fig.Visible = 'on';
            uiwait(fig);
            
            % Nested functions with access to shared workspace
            function update_display()
                current_syllable_data = syllables{current_file}(:,current_syllable);
                current_syllable_data = current_syllable_data / max(abs(current_syllable_data));
                
                % Create time vector for waveform (in ms)
                t = (0:length(current_syllable_data)-1) / fs * 1000;
                
                % Update waveform plot
                cla(waveform_ax);
                plot(waveform_ax, t, current_syllable_data);
                xlabel(waveform_ax, 'Time (ms)');
                ylabel(waveform_ax, 'Amplitude');
                title(waveform_ax, 'Waveform');
                
                % Update spectrogram
                cla(spec_ax);
                axes(spec_ax);
                spectrogram(current_syllable_data, hamming(128), 120, 512, fs, 'yaxis');
                title(spec_ax, 'Spectrogram');
                
                % Update info text
                info_text.String = sprintf('File %d/%d, Syllable %d/%d', ...
                    current_file, length(syllables), ...
                    current_syllable, size(syllables{current_file}, 2));
            end
            
            function toggle_play(~,~)
                if ~is_playing
                    current_syllable_data = syllables{current_file}(:,current_syllable);
                    current_syllable_data = current_syllable_data / max(abs(current_syllable_data));
                    sound(current_syllable_data, fs);
                    play_btn.String = '⏸';
                    is_playing = true;
                else
                    clear sound;
                    play_btn.String = '▶';
                    is_playing = false;
                end
            end
            
            function next_syllable(~,~)
                clear sound;
                is_playing = false;
                play_btn.String = '▶';
                
                if current_syllable < size(syllables{current_file}, 2)
                    current_syllable = current_syllable + 1;
                elseif current_file < length(syllables)
                    current_file = current_file + 1;
                    current_syllable = 1;
                end
                
                update_display();
            end
            
            function previous_syllable(~,~)
                clear sound;
                is_playing = false;
                play_btn.String = '▶';
                
                if current_syllable > 1
                    current_syllable = current_syllable - 1;
                elseif current_file > 1
                    current_file = current_file - 1;
                    current_syllable = size(syllables{current_file}, 2);
                end
                
                update_display();
            end
            
            function handle_key_press(~, event)
                switch event.Key
                    case 'rightarrow'
                        next_syllable();
                    case 'leftarrow'
                        previous_syllable();
                    case 'space'
                        toggle_play();
                    case 'escape'
                        close_player();
                end
            end
            
            function close_player(~,~)
                clear sound;
                uiresume(fig);
                close(fig);
            end
        end
    end
end