clear; close all;
theta = 0; 
thr_I = 100;

l=dir('test/*.jpg');
list={l.name};


for i=1:length(list)
    disp([num2str(i) '/' num2str(length(list))]);
    name = list{i};
    
    inputImage = imread(['test/' name]);

    grayImage = rgb2gray(inputImage);
    [height, width] = size(grayImage);

    BAG_map = ExtractBAGMap(grayImage, theta, thr_I);
    BAG = ExtractBAGFeatures(BAG_map);
    
    %save(['output/' name(1:end-4) '_BAG.mat'] , 'BAG');
    ma = max(max(BAG));
    mi = min(min(BAG));
    BAG = (BAG - mi) / (ma - mi);
    imshowpair(inputImage, BAG, 'montage')
    close all
end