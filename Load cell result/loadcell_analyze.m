% clc
% clear all

%% Load and Prepare Data
data = importdata('loadcell.txt');
data = data(1:end-1);

%% Step 1: Initial Detection
baseline = mean(data(data < 85));
threshold = baseline + 5;

above_threshold = data > threshold;
event_starts_raw = find(diff([0; above_threshold]) == 1);
event_ends_raw = find(diff([above_threshold; 0]) == -1);

%% Step 2: Apply Filters
min_duration = 5;    % At least 5 samples
min_peak = baseline + 20;  % At least 20 units above baseline

% Calculate properties for all detected events
valid_mask = true(length(event_starts_raw), 1);

for i = 1:length(event_starts_raw)
    event_range = event_starts_raw(i):event_ends_raw(i);
    duration = length(event_range);
    peak = max(data(event_range));
    
    % Mark as invalid if too short or too weak
    if duration < min_duration || peak < min_peak
        valid_mask(i) = false;
        fprintf('Removed Event at sample %d: Peak=%.1f, Duration=%d\n', ...
            event_starts_raw(i), peak, duration);
    end
end

% Keep only valid events
event_starts = event_starts_raw(valid_mask);
event_ends = event_ends_raw(valid_mask);
num_events = length(event_starts);

fprintf('\n=== Detection Summary ===\n');
fprintf('Initial detections: %d\n', length(event_starts_raw));
fprintf('False positives removed: %d\n', sum(~valid_mask));
fprintf('Valid events: %d ✓\n\n', num_events);

%% Step 3: Extract Valid Events with Padding
padding = 20;
events = cell(num_events, 1);
event_ranges_padded = cell(num_events, 1);

for i = 1:num_events
    start_idx = max(1, event_starts(i) - padding);
    end_idx = min(length(data), event_ends(i) + padding);
    events{i} = data(start_idx:end_idx);
    event_ranges_padded{i} = start_idx:end_idx;
end

%% Step 4: Calculate Statistics (Using Padded Range)
peaks = zeros(num_events, 1);
durations = zeros(num_events, 1);
areas = zeros(num_events, 1);
peak_positions = zeros(num_events, 1);

for i = 1:num_events
    padded_range = event_ranges_padded{i};
    event_data = data(padded_range);
    
    [peaks(i), local_peak_idx] = max(event_data);
    peak_positions(i) = padded_range(local_peak_idx);
    
    event_range = event_starts(i):event_ends(i);
    durations(i) = length(event_range);
    
    areas(i) = sum(max(data(padded_range) - baseline, 0));
    
    fprintf('Event %d: Peak=%.1f, Duration=%d samples, Position=%d\n', ...
        i, peaks(i), durations(i), event_starts(i));
end

%% Step 5: Plot All Valid Events
figure('Position', [100, 100, 1400, 900]);
rows = ceil(sqrt(num_events));
cols = ceil(num_events / rows);



for i = 1:num_events
    subplot(rows, cols, i);
    
    padded_range = event_ranges_padded{i};
    event_data = data(padded_range);
    
    plot(padded_range, event_data, 'b-', 'LineWidth', 2);
    hold on;
    yline(baseline, 'k--', 'Baseline', 'LineWidth', 1);
    yline(threshold, 'r--', 'Threshold', 'LineWidth', 1);
    
    plot(peak_positions(i), peaks(i), 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');
    
    xlabel('Sample Number');
    ylabel('Force (Newton)');
    title(sprintf('Event %d (Peak: %.1f)', i, peaks(i)));
    grid on;
    hold off;
end

%% Step 6: Show Original Timeline with Valid Events Only
figure('Position', [100, 100, 1200, 500]);
plot(data, 'b-', 'LineWidth', 0.5);
hold on;
yline(threshold, 'g--', 'Threshold', 'LineWidth', 1.5);

for i = 1:num_events
    plot(event_starts(i):event_ends(i), ...
        data(event_starts(i):event_ends(i)), 'r-', 'LineWidth', 2);
end

xlabel('Sample Number');
ylabel('Reading');
title(sprintf('Valid Events Detected: %d', num_events));
grid on;
hold off;

%% Step 7: Summary Table
fprintf('\n=== Event Summary ===\n');
fprintf('Event | Peak  | Duration | Area   | Start Sample\n');
fprintf('------|-------|----------|--------|-------------\n');
for i = 1:num_events
    fprintf('%5d | %5.1f | %8d | %6.0f | %12d\n', ...
        i, peaks(i), durations(i), areas(i), event_starts(i));
end

%% Step 8: Statistics
figure('Position', [100, 100, 1200, 400]);

subplot(1,3,1);
bar(peaks);
xlabel('Event Number');
ylabel('Peak Value');
title(sprintf('Peak Values (%d Events)', num_events));
grid on;

subplot(1,3,2);
bar(durations);
xlabel('Event Number');
ylabel('Duration (samples)');
title('Event Durations');
grid on;

subplot(1,3,3);
bar(areas);
xlabel('Event Number');
ylabel('Area');
title('Area Under Curve');
grid on;

%% ========================================================================
%% NEW: INDIVIDUAL GRAPHS FOR EACH PEAK (SEPARATE WINDOWS)
%% ========================================================================

fprintf('\n=== Creating Individual Peak Graphs ===\n');

for i = 1:num_events
    % Create new figure window for each event
    fig = figure('Position', [50 + (i-1)*40, 50 + (i-1)*30, 900, 700]);
    fig.Name = sprintf('Event %d Details', i);
    
    % Get data for this event
    padded_range = event_ranges_padded{i};
    event_data = data(padded_range);
    detected_range = event_starts(i):event_ends(i);
    
    % Main plot
    plot(padded_range, event_data, 'b-', 'LineWidth', 2.5);
    hold on;
    
    % Add reference lines
    yline(baseline, 'k--', 'Baseline', 'LineWidth', 1.5, ...
        'LabelHorizontalAlignment', 'left', 'FontSize', 10);
    yline(threshold, 'r--', 'Threshold', 'LineWidth', 1.5, ...
        'LabelHorizontalAlignment', 'left', 'FontSize', 10);
    
    % Highlight detected event region in green
    plot(detected_range, data(detected_range), 'g-', 'LineWidth', 3.5);
    
    % Mark peak with large red circle
    plot(peak_positions(i), peaks(i), 'ro', 'MarkerSize', 15, ...
        'MarkerFaceColor', 'r', 'LineWidth', 2);
    
    % Add peak value annotation
    text(peak_positions(i), peaks(i) + 5, ...
        sprintf('Peak: %.1f', peaks(i)), ...
        'HorizontalAlignment', 'center', 'FontSize', 13, ...
        'FontWeight', 'bold', 'BackgroundColor', 'white', ...
        'EdgeColor', 'black', 'Margin', 3);
    
    % Calculate rise from baseline
    rise_value = peaks(i) - baseline;
    rise_percent = (rise_value / baseline) * 100;
    
    % Create detailed info box
    info_text = sprintf(['EVENT %d STATISTICS\n' ...
        '═══════════════════════\n' ...
        'Peak Value:    %.1f Newton\n' ...
        'Baseline:      %.1f Newton\n' ...
        'Rise:          %.1f Newton\n' ...
        'Rise %%:        %.1f%%\n' ...
        '───────────────────────\n' ...
        'Duration:      %d samples\n' ...
        'Area:          %.0f\n' ...
        'Start Sample:  %d\n' ...
        'Peak Sample:   %d'], ...
        i, peaks(i), baseline, rise_value, rise_percent, ...
        durations(i), areas(i), event_starts(i), peak_positions(i));
    
    % Position info box in upper left
    annotation('textbox', [0.15, 0.60, 0.30, 0.30], ...
        'String', info_text, 'FontSize', 11, 'FontName', 'FixedWidth', ...
        'BackgroundColor', [1 1 0.9], 'EdgeColor', 'black', ...
        'LineWidth', 2, 'FitBoxToText', 'on');
    
    % Labels and title
    xlabel('Sample Number', 'FontSize', 13, 'FontWeight', 'bold');
    ylabel('Force (Newton)', 'FontSize', 13, 'FontWeight', 'bold');
    title(sprintf('Event %d - Detailed Analysis', i), ...
        'FontSize', 16, 'FontWeight', 'bold');
    
    % Legend
    legend('Sensor Data', 'Baseline', 'Threshold', 'Detected Event', 'Peak', ...
        'Location', 'southeast', 'FontSize', 10);
    
    grid on;
    xlim([padded_range(1), padded_range(end)]);
    ylim([min(event_data)-5, max(event_data)+10]);
    hold off;
    
    % % Save figure as PNG
    % filename = sprintf('Event_%d_Detail.png', i);
    % saveas(fig, filename);
    % 
    % fprintf('  ✓ Created graph for Event %d (saved as %s)\n', i, filename);
end

fprintf('\n=== Individual Peak Graphs Complete ===\n');
fprintf('Total figures created: %d\n', num_events);
fprintf('All graphs saved as PNG files (Event_1_Detail.png to Event_%d_Detail.png)\n\n', num_events);

% %% ========================================================================
% %% Step 9: Compare filtered vs unfiltered detections
% %% ========================================================================
% 
% figure('Position', [100, 100, 1200, 800]);
% subplot(2,1,1);
% plot(data);
% hold on;
% for i = 1:length(event_starts_raw)
%     plot(event_starts_raw(i):event_ends_raw(i), ...
%         data(event_starts_raw(i):event_ends_raw(i)), 'r-', 'LineWidth', 2);
% end
% title(sprintf('Before Filter: %d detections', length(event_starts_raw)), ...
%     'FontSize', 14, 'FontWeight', 'bold');
% yline(threshold, 'g--', 'LineWidth', 2);
% xlabel('Sample Number', 'FontSize', 11);
% ylabel('Reading', 'FontSize', 11);
% grid on;
% hold off;
% 
% subplot(2,1,2);
% plot(data);
% hold on;
% for i = 1:num_events
%     plot(event_starts(i):event_ends(i), ...
%         data(event_starts(i):event_ends(i)), 'r-', 'LineWidth', 2);
% end
% title(sprintf('After Filter: %d valid events ✓', num_events), ...
%     'FontSize', 14, 'FontWeight', 'bold');
% yline(threshold, 'g--', 'LineWidth', 2);
% xlabel('Sample Number', 'FontSize', 11);
% ylabel('Reading', 'FontSize', 11);
% grid on;
% hold off;

%plot only peak
%plot(peaks,"-square",'LineWidth',2)

plot(peaks, 'b-', 'LineWidth', 1);
hold on;
plot(peaks, 'ro', 'MarkerSize', 3, ...
        'MarkerFaceColor', 'r', 'LineWidth', 2);
title(sprintf('Peak force graph'));
xlabel('Sample Number');
ylabel('Force (Newton)');
grid on;

%% Final Summary
fprintf('╔════════════════════════════════════════════════════════╗\n');
fprintf('║           LOAD CELL ANALYSIS COMPLETE                 ║\n');
fprintf('╠════════════════════════════════════════════════════════╣\n');
fprintf('║  Total valid events detected:    %2d                   ║\n', num_events);
fprintf('║  Average peak value:              %.1f Newton         ║\n', mean(peaks));
fprintf('║  Peak standard deviation:         %.1f Newton         ║\n', std(peaks));
fprintf('║  Average event duration:          %.1f samples        ║\n', mean(durations));
fprintf('╚════════════════════════════════════════════════════════╝\n');
