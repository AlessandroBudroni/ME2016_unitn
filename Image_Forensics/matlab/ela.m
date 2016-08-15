function [ feature ] = ela(I, roi_size)
%ELA Summary of this function goes here
%   Detailed explanation goes here

    imwrite(I,'out.jpg','quality',95);
        
    newImg = im2double(imread('out.jpg'));
    
    diffI = abs(newImg - I);
    
    max_diff = max(diffI(:));
    scale = 1.0 + 1.0/max_diff;
    diffI = diffI*scale;
    
    diffI = diffI(:,:,1);

    roi = [1,1];
    ma = sum(sum(diffI(1:roi_size, 1:roi_size)));
    for i = 2:size(diffI,1) - roi_size
        for j = 2:size(diffI,2) - roi_size
            v = sum(sum(diffI(i:(i+roi_size-1),j:(j+roi_size-1))));
            if v > ma
                ma = v;
                roi = [i,j];
            end
        end
    end
    
    max_final_roi = reshape(diffI(roi(1):(roi(1)+roi_size-1),...
        roi(2):(roi(2)+roi_size-1)),[1 roi_size*roi_size]);
    
    feature = [max(max_final_roi), mean(max_final_roi),...
        var(max_final_roi)];
    
end

