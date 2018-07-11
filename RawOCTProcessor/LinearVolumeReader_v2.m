%
% Open a linear OCT volume and attempt to apply virtual SIM
%
folder='N:\Adelene\Sample1\slow scan';
filename='reprocessedLinearVolume.bin';

ascanLength=512;
numAScansPerBScan=500;
numBScansPerVolume=500;

fid=fopen([folder '/' filename]);
vec=fread(fid,'float32');
vol=reshape(vec,[ascanLength,numAScansPerBScan,numBScansPerVolume]);

%
%Extract a modulated plane
%
modulated1=zeros(ascanLength,numAScansPerBScan,numBScansPerVolume);
modulated2=zeros(ascanLength,numAScansPerBScan,numBScansPerVolume);
modulated3=zeros(ascanLength,numAScansPerBScan,numBScansPerVolume);
numPeriods=100;
phi1=0;
phi2=2*pi/3;
phi3=4*pi/3;
maxZ=2;

for z0=maxZ+1:ascanLength-maxZ
for x=1:numAScansPerBScan
    z1=z0+maxZ*cos((x-1)/(numAScansPerBScan-1)*numPeriods*2*pi+phi1);
    z2=z0+maxZ*cos((x-1)/(numAScansPerBScan-1)*numPeriods*2*pi+phi2);
    z3=z0+maxZ*cos((x-1)/(numAScansPerBScan-1)*numPeriods*2*pi+phi3);
    modulated1(z0,x,:)=vol(round(z1),x,:);
    modulated2(z0,x,:)=vol(round(z2),x,:);
    modulated3(z0,x,:)=vol(round(z3),x,:);
end
end
Ic=(modulated1+modulated2+modulated3)/3;
Is=sqrt(2)/3*sqrt((modulated1-modulated2).^2+(modulated1-modulated3).^2+(modulated2-modulated3).^2);
figure(1);imshow(log10(mean(vol(:,:,240:260),3)),[-1.5,1.5]);
figure(2);imshow(log10(mean(Is(:,:,240:260),3)),[-2.5,1.5]);
figure(3);imshow(log10(mean(sing(:,:,240:260),3)),[-4,3]);
figure(4);imshow(log10(mean(Ic(:,:,240:260),3)),[-3,2]);
figure(5);imshow(log10(mean(Ic(:,:,240:260)-vol(:,:,240:260),3)),[-3,2]);

fclose(fid);
