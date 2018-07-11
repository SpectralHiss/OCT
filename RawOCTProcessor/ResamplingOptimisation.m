%
% OCT Resampling Optimisation based upon Image Contrast
% Pete Tomlins, QMUL, 18 April 2016
%
clear all;
%
% OCT Version (1 = Pre-Crash systm <2012/13, 2 = Post-Crash system 2012/13 onwards)
octVersion=2;
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
rootInputFolder='N:\NAS1_Backup_20141008\OCT_Data\Arthi\20130704\Bovine Sample (4,2,3,5) demin second day';
%'N:\Abdi\15. Erosion_Oct_2014_flow\3. Main_Experiment_Sequence_Scans_citric_pH3,8_30092014';
%'N:\Abdi\21. Erosion_July_2015_flow_multisample\Erosion challenge_24072015';
rootInputFolder=strrep(rootInputFolder,'\','/');

calibrationFolder='N:\Abdi\15. Erosion_Oct_2014_flow\Calibration';
calibrationFolder=strrep(calibrationFolder,'\','/');
%'N:/NAS1_Backup_20141008/OCT_Data/Arthi/20130604/Sample 2 demin';
rootOutputFolder=rootInputFolder;
repeatFolderTitle='Repeat';
positionFolderTitle='Position';
bscanFolderTitle='png';
%
spectraFileName='Spectra.bin';
%
% System version dependent raw data files
%
if (octVersion==1)
    parametersFileName='parameters.csv';
    spectraFileName='Spectra.bin';
    resamplingTableFileName='resamptable.csv';
    referenceSpectrumFileName='SpectralTable.bin';
    referenceAScanFileName='Background.bin';
elseif (octVersion==2)
    parametersFileName='parameters.csv';
    spectraFileName='Spectra.bin';
    resamplingTableFileName='reamplingTable.csv';
    referenceSpectrumFileName='referenceSpectrum.csv';
    referenceAScanFileName='referenceAScan.csv';
end
%
% Manually set the number of repetitions and positions
%
startRepeat=1;
endRepeat=1;
skipRepeat=1;
rCount=0;
%
startPosition=1;
endPosition=1;
skipPosition=1;
%
% In this order, loop through, repeats, positions
%
for r=startRepeat:skipRepeat:endRepeat
    rCount=rCount+1;
    %
    % Set the repeat sub folder
    %
    repeatSubFolder=[repeatFolderTitle sprintf('%0.4i',r)];
    %
    % Loop through positions
    %
    pCount=0;
    for p=startPosition:skipPosition:endPosition
        pCount=pCount+1;
        %
        % Set the position sub-folder
        %
        positionSubFolder=[positionFolderTitle sprintf('%0.4i', p)];
        octFolder=[rootInputFolder '/' repeatSubFolder '/' positionSubFolder];
        %
        % Load the OCT parameters
        %
        parameters=readtable([octFolder '/' parametersFileName],'ReadVariableNames',false);
        %
        % Get the OCT image dimensions
        %
        numBScans=str2double(parameters{2,2});
        numAScansPerBScan=str2double(parameters{3,2});
        spectrumLength=1024;
        %
        % Now load the OCT volume data
        %
        disp('Loading raw spectra...');
        fidSpectra=fopen([octFolder '/' spectraFileName]);
        spectra=fread(fidSpectra,[spectrumLength*numAScansPerBScan*numBScans],'uint16');
        fclose(fidSpectra);
        disp('Done.');
        %
        % Now Process a B-Scan
        %
        spectra=reshape(spectra,[spectrumLength,numAScansPerBScan,numBScans]);
        %
        % Define window function
        %
        window=blackman(spectrumLength);
        %

        %
        disp('Optimising...');
        %
        b=floor(numBScans/2);
        

        
        referenceSpectrum=EstimateReferenceSpectrum(spectra,1);
        referenceAScan=zeros(spectrumLength/2,1);
        strayLight=zeros(spectrumLength,1);
        %
        % Load an approximate resampling table from file
        %
        resamplingTable=dlmread([calibrationFolder '/resamplingTable.csv']);
        bscan=ProcessOCTBScan(spectra(:,:,b),resamplingTable,referenceSpectrum,referenceAScan,strayLight, window);
        
        logBScan=20*log10(bscan);
        %
        % Try Optimising
        %
        Order=3;
        p=polyfit(resamplingTable(:,1),resamplingTable(:,2),Order);
        [fittedParams,optimResamplingTable,bscanContrast]=OptimiseOCTResampling(spectra(:,240:260,b),referenceSpectrum,referenceAScan,strayLight,window,Order,fliplr(p));
        optimBScan=ProcessOCTBScan(spectra(:,:,b),optimResamplingTable,referenceSpectrum,referenceAScan,strayLight, window);
        figure(1);imshow(20*log10(bscan),[-40,10]);
        figure(2);imshow(20*log10(optimBScan),[-40,10]);
        
        figure(3);imshow(20*log10(bscan-optimBScan),[]);
    end
    
    
end
