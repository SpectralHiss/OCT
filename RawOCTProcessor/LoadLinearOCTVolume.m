%
% Load OCT Linear Volume
% Pete Tomlins, 30 June 2016
%
function linearVolume=LoadLinearOCTVolume(rootInputFolder, linearVolumeFileName,parametersFileName)
%rootInputFolder='C:\Users\OCT\Desktop\Pete\PSF Phantom Large Scan';
rootInputFolder=strrep(rootInputFolder,'\','/');
%
f=fopen([rootInputFolder '/' linearVolumeFileName]); %'/LinearOCTVolume.bin']);

%
% Read the parameters file
%
parameters=readtable([rootInputFolder '/' parametersFileName],'ReadVariableNames',false);
%
% Get the OCT image dimensions
%
numBScans=str2double(parameters{2,2});
numAScansPerBScan=str2double(parameters{3,2});
spectrumLength=1024;
%ascanLength=floor(spectrumLength/2);

data=fread(f,spectrumLength*numAScansPerBScan*numBScans,'float32');

linearVolume=reshape(data,[spectrumLength,numAScansPerBScan,numBScans]);

fclose(f);


end

