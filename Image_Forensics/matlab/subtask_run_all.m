clear all; close all;

addpath(genpath('./DJPG-TIFS2012'));
addpath(genpath('./jpegtbx_1.4'));

dataset = 'testset'; % or testset

media_path = ['/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/image-verification-corpus-master/mediaeval2016/', dataset, '_subtask_files/'];
%post_detail_file = ['/Users/quoctin/Documents/UNITN - No Dropbox/MediaEVAL/image-verification-corpus-master/mediaeval2016/', dataset, '/posts.txt'];


files = dir([media_path '*.jpg']);
nfeatures = 27;

nMedias = length(files);

features = zeros(nMedias, nfeatures);
names = cell(nMedias, 1);
eff_ind = zeros(nMedias,1);
nImgs = 0;
s = 1;

for f = files'
    file_full_path = [media_path, f.name];
    
    I = imread([media_path, f.name]);
    if ndims(I) == 4
        I = I(:,:,1:3);
    end
    
    try
        roi_size = 16;
        log_feature = log_map(file_full_path, roi_size);

        roi_size = 64;
        ela_feature = ela(im2double(I),roi_size);

        theta = 0; 
        thr_I = 100;
        roi_size = 64;
        bag_feature = bag(I, theta, thr_I, roi_size);

        features(s,:) = [ela_feature log_feature bag_feature];     
        
        nImgs = nImgs + 1;
        name = strrep(f.name, '.jpg', '');
        names{nImgs} = name;
        
        eff_ind(s) = 1;
        
        disp(name)
    catch
        disp('error')
    end
    s = s + 1;
end

features = features((eff_ind==1), :);

dlmwrite([dataset, '_subtask_features.dat'], features);

fileID = fopen([dataset, '_eff_subtask_images.dat'], 'w');
for row = 1:nImgs
    fprintf(fileID,'%s\n', names{row,:});
end

fclose(fileID);


% nMedias = size(media_details,1);
% 
% names = cell(nMedias,1);
% nImgs = 0;
% 
% nfeatures = 27;
% features = zeros(nMedias, nfeatures);
% 
% c = table2cell(media_details);
% eff_ind = zeros(nMedias,1);
% 
% for s = 1:nMedias
%     
%     disp(c{s,1});		
% 	[pathstr,name,ext] = fileparts(c{s,4});
%     
%     if strcmp(c{s,2},'video') || (~strcmp(ext,'.jpg') && ...
%             ~strcmp(ext,'.jpeg'))
%         continue;
%     end
%        
%     m = c{s,1:4};
% 
%     I = imread(c{s,4});
%         
%     if ndims(I) == 4
%         I = I(:,:,1:3);
%     end
%     
%     try
%         roi_size = 16;
%         log_feature = log_map(c{s,4}, roi_size);
% 
%         roi_size = 64;
%         ela_feature = ela(im2double(I),roi_size);
% 
%         theta = 0; 
%         thr_I = 100;
%         roi_size = 64;
%         bag_feature = bag(I, theta, thr_I, roi_size);
% 
%         features(s,:) = [ela_feature log_feature bag_feature];
%         eff_ind(s) = 1;
%         
%         nImgs = nImgs + 1;
%         names{nImgs} = c{s,1};
%     catch
%         disp('error')
%     end
%     
% end
% 
% features = features((eff_ind==1), :);
% dlmwrite([dataset, '_forensic_features.dat'], features);
% 
% fileID = fopen([dataset, '_eff_forensic_topics.dat'], 'w');
% for row = 1:nImgs
%     fprintf(fileID,'%s\n', names{row,:});
% end
% 
% fclose(fileID);

