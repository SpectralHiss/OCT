%
% Save image
% Save a matrix as an image
%function
function [img]=SaveImage(filename,M,minVal,maxVal)
    img=(M-minVal)/(maxVal-minVal) * 255;
    img(img<0)=0;
    img(img>255)=255;
    imwrite(uint8(img),filename);

end