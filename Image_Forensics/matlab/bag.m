function [ feature ] = bag(I, theta, thr_I, roi_size)
%BAG Summary of this function goes here
%   Detailed explanation goes here
    grayImage = rgb2gray(I);

    BAG_map = ExtractBAGMap(grayImage, theta, thr_I);
    BAG = ExtractBAGFeatures(BAG_map);
    
    roi = [1,1];
    ma = sum(sum(BAG(1:roi_size, 1:roi_size)));
    for i = 2:size(BAG,1) - roi_size
        for j = 2:size(BAG,2) - roi_size
            v = sum(sum(BAG(i:(i+roi_size-1),j:(j+roi_size-1))));
            if v > ma
                ma = v;
                roi = [i,j];
            end
        end
    end
    
    max_final_roi = reshape(BAG(roi(1):(roi(1)+roi_size-1),...
        roi(2):(roi(2)+roi_size-1)),[1 roi_size*roi_size]);
    
    feature = [max(max_final_roi), min(max_final_roi), mean(max_final_roi),...
        var(max_final_roi)];
end

