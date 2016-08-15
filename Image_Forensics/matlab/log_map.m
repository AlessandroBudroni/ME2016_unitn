function [feature] = log_map(path, roi_size)
%LOG_MAP Summary of this function goes here
%   Detailed explanation goes here
    c2=6;
    coeff = [1 9 2 3 10 17];
    
    im=jpeg_read(path);
    
    [LLRmap, LLRmap_s, q1table, alphat] = getJmap_EM(im, 1, c2);
    map_final_A = imfilter(sum(LLRmap,3), ones(3), 'symmetric', 'same');
    ma = sum(sum(map_final_A(1:roi_size, 1:roi_size)));
    
    steps_A = q1table(coeff);
    
    roiA = [1,1];
    for i = 2:size(map_final_A,1) - roi_size
        for j = 2:size(map_final_A,2) - roi_size
            v = sum(sum(map_final_A(i:(i+roi_size-1),j:(j+roi_size-1))));
            if v > ma
                ma = v;
                roiA = [i,j];
            end
        end
    end
    
    max_final_A = reshape(map_final_A(roiA(1):(roiA(1)+roi_size-1),...
        roiA(2):(roiA(2)+roi_size-1)),[1 roi_size*roi_size]);
    
    feature = [max(max_final_A), min(max_final_A), mean(max_final_A),...
        var(max_final_A), steps_A];
    
    [LLRmap, LLRmap_s, q1table, k1e, k2e, alphat] = getJmapNA_EM(im, 1, c2);
    map_final_NA = smooth_unshift(sum(LLRmap,3),k1e,k2e);
    
    steps_NA = q1table(coeff);
    
    ma = sum(sum(map_final_NA(1:roi_size, 1:roi_size)));
    roiNA = [1,1];
    
    for i = 2:size(map_final_NA,1) - roi_size
        for j = 2:size(map_final_NA,2) - roi_size
            v = sum(sum(map_final_NA(i:(i+roi_size-1),j:(j+roi_size-1))));
            if v > ma
                ma = v;
                roiNA = [i,j];
            end
        end
    end
    
    max_final_NA = reshape(map_final_NA(roiNA(1):(roiNA(1)+roi_size-1),...
        roiNA(2):(roiNA(2)+roi_size-1)),[1 roi_size*roi_size]);
    
    feature = [feature, max(max_final_NA), min(max_final_NA), mean(max_final_NA),...
        var(max_final_NA), steps_NA];
end

