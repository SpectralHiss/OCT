%
% Measure the contrast in an OCT image
%
function [contrast]=GetImageContrast(image)

    [H,W]=size(image);
    vec=reshape(image,[H*W,1]);
    %contrast=std(vec);
    contrast=mean(mean(image(25:floor(H/2),:)))/mean(mean(image(floor(H/2):H,:)));
    
end