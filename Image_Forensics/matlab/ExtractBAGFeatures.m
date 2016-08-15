function [BAG_features] = ExtractBAGFeatures(BAG_map)

[height, width] = size(BAG_map);
%{ 
%% Find maximum translate
sum_Row = sum(BAG_map, 2);
sum_Col = sum(BAG_map, 1);
sum_Row8 = zeros(8, 1); 
sum_Col8 = zeros(8, 1); 
for i = 1:8
    sum_Row8(i) = sum(sum_Row(i:8:end));
    sum_Col8(i) = sum(sum_Col(i:8:end));
end

d_Row8 = zeros(8, 1);
d_Col8 = zeros(8, 1);
for i = 1:8
    d_Row8(i) = sum_Row8(i) - sum_Row8(mod(i, 8) +1);
    d_Col8(i) = sum_Col8(i) - sum_Col8(mod(i, 8) +1);
end

[~, trans_row] = max(d_Row8)
[~, trans_col] = max(d_Col8)
%}

trans_row = 1;
trans_col = 1;


%% Bag feature extraction
Block_cols = floor(width/8);
Block_rows = floor(height/8);

BAG = zeros(Block_rows, Block_cols);
BAG_features = zeros(height, width);
for r = 1:Block_rows
    for c = 1:Block_cols
        currentRow = (r-1)*8 + trans_row;
        currentCol = (c-1)*8 + trans_col;
        row_sum = sum(BAG_map(currentRow:currentRow+7, currentCol+1:currentCol+6), 2);
        col_sum = sum(BAG_map(currentRow+1:currentRow+6, currentCol:currentCol+7), 1);
        BAG(r,c) = max(row_sum(2:7)) + max(col_sum(2:7))...
            -min([row_sum(1), row_sum(8)])-min([col_sum(1), col_sum(8)]);
        BAG_features(currentRow:currentRow+7, currentCol:currentCol+7) = BAG(r,c) * ones(8, 8);
    end
end 

