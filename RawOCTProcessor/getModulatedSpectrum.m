%
% SI-OCT from multiple volumes at different source currents
%
function [modulatedVolume,linearVolumes]=getModulatedSpectrum(volumePath,sourceIntensity)

    %
    % Load the volumes
    %
    linearVolumeFilename='LinearOCTVolume.bin';
    parametersFilename='parameters.csv';
    numVolumes=max(size(volumePath));
    for v=1:numVolumes
        vol=LoadLinearOCTVolume(volumePath{v}, linearVolumeFilename, parametersFilename);
        
        if (v==1)
            volSize=size(vol);
            linearVolumes=zeros(volSize(1),volSize(2),volSize(3),numVolumes);
            modulatedVolume=zeros(volSize);
        end
        
        linearVolumes(:,:,:,v)=vol;
    end

end