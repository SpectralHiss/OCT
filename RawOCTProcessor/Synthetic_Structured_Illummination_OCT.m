%
% Synthetic Structured Illumination OCT
% Pete Tomlins, QMUL
%
% Can we produce structured illumination in B-Scans by measuring the same
% volume at different intensities?
%
clear all;
sourceCurrent(1)=400;
sourceCurrent(2)=381;
sourceCurrent(3)=331;
sourceCurrent(4)=269;
sourceCurrent(5)=219;
sourceCurrent(6)=200;

startBScan=250;
endBScan=250;
numBScans=endBScan-startBScan+1;

numVolumes=max(size(sourceCurrent));

for n=1:numVolumes
    volumePath{n}=['C:\Users\OCT\Desktop\SI-OCT\Intensity Modulation\Linear ' num2str(sourceCurrent(n)) 'mA'];
end

%
% Load the linear volumes
%
linearVolumeFilename='LinearOCTVolume.bin';
parametersFilename='parameters.csv';
for v=1:numVolumes
    disp(['Loading volume ' num2str(v) '...']);
    vol=LoadLinearOCTVolume(volumePath{v}, linearVolumeFilename, parametersFilename);

    %
    % On first pass create the linearVolumes array - if this can't be
    % done, then there isn't sufficient memory
    %
    if (v==1)
        volSize=size(vol);
        ascanLength=volSize(1)/2;
        numAScansPerBScan=volSize(2);
        
        linearVolumes=zeros(ascanLength,numAScansPerBScan,numBScans,numVolumes);
    end
    
    linearVolumes(1:ascanLength,:,1:numBScans,v)=vol(1:ascanLength,:,startBScan:endBScan);
end

%
% For each pixel in the volume, create a cubic spline interpolant
%
disp('Creating interpolation matrix...');
i=0;
total=ascanLength*numAScansPerBScan*numBScans;

vx=sourceCurrent;
vy=zeros(size(vx));


for y=1:numBScans
    for x=1:numAScansPerBScan
        for z=1:ascanLength
            
            vy(:)=linearVolumes(z,x,y,:);
            pp=spline(vx,vy);
            if (i==0)
                %ppSize=max(size(pp));
                interpolant(ascanLength,numAScansPerBScan,numBScans)=pp;
            end
            
            interpolant(z,x,y)=pp;
            i=i+1;
            
        end
        disp([sprintf('%5.2f',i/total*100) ' % complete...']);         
    end
end
disp(['100 % complete...']); 
    
% Create a structured intensity mask
modulated=zeros([ascanLength,numAScansPerBScan,numBScans,3]);
Imin=min(sourceCurrent);
Imax=max(sourceCurrent);
Iamp=(Imax-Imin)/2;
numPeriods=100;
for i=1:3
    
    phi=2*pi/3 * (i-1);
    
    for z=1:ascanLength
        intensity(z)=Iamp*cos((z-1)/ascanLength*2*pi*numPeriods + phi) + Imin + Iamp;
    
    
        for x=1:numAScansPerBScan
            for y=1:numBScans
                modulated(z,x,y,i)=ppval(interpolant(z,x,y),intensity(z));
            end
        end
    end
    
end
for i=1:3
    figure(i);
    imshow(squeeze(log(modulated(:,:,:,i))),[]);
end

Is=sqrt(2)/3*sqrt( (modulated(:,:,:,1)-modulated(:,:,:,2)).^2 + (modulated(:,:,:,1)-modulated(:,:,:,3)).^2 +(modulated(:,:,:,2)-modulated(:,:,:,3)).^2);
Ic=   mean(modulated,4);       
figure(4);imshow(squeeze(20*log10(Is)),[-180 -90]);
figure(5);imshow(squeeze(20*log10(Ic)),[-180 -90]);

Imean=mean(linearVolumes(1:ascanLength,:,:,:),4);
figure(6);imshow(squeeze(20*log10(Imean)),[-180 -90]);

%for v=1:6
%    figure(v*10);
%    imshow(squeeze(log(linearVolumes(:,:,1,v))),[]);
%end

ascanSI=20*log10(mean(Is,2));
ascanOrig=20*log10(mean(Imean,2));

figure(7);
hold on;
plot(ascanSI);
plot(ascanOrig);
hold off;
