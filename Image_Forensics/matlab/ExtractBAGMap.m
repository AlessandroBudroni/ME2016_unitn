function [BAG_map] = ExtractBAGMap(grayImage, theta, thr_I)
[height, width] = size(grayImage);
%% Apply sobel filter
[~, gdir] = imgradient(grayImage, 'Sobel');

%% Compute matrix R (eq. 1): Note: this R is an inverted from (1)
R = ones(size(grayImage));
R(gdir < theta & gdir > -theta) = 0;
R(gdir < 90 + theta & gdir > 90 - theta) = 0;
R(gdir < -90 + theta & gdir > -90 - theta) = 0;
R(gdir > 180 - theta | gdir < -180 + theta) = 0;

%% Compute second-order difference (eq. 2)
grr = conv2(double(grayImage), [-1; 2; -1], 'same');
gcc = conv2(double(grayImage), [-1, 2, -1], 'same');

%% Filtering
dr = grr .* R;
dc = gcc .* R;
dr = abs(dr);
dc = abs(dc);
dr(dr > thr_I) = 0; 
dc(dc > thr_I) = 0;

%% Accumulate rows and columns (eq. 3)
a_row = conv2(dr, ones(1, 33), 'same'); % row, sum of 33 cols
a_col = conv2(dc, ones(33, 1), 'same'); % col, sum of 33 rows

%% Compute residual (eq. 4)
ar_row = a_row - medfilt2(a_row, [33 1]);
ar_col = a_col - medfilt2(a_col, [1 33]);

%% Compute BAG (eq. 5 + eq. 6)
BAG_map = zeros(height, width);
for row = 17:height - 16
    for col = 17:width - 16
        BAG_map(row, col) = median(ar_row(row-16:8:row+16,col)) + ...
            +  median(ar_col(row, col-16:8:col+16)); 
    end
end