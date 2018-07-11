%
% Process a raw OCT data from new and old OCT systems
% Process multiple repeats and positions
% Output SUM, SAM images and numeric results
% Find multiple interfaces
%
% Modified by PT, 22 April 2016 to process Huda's caries-like demin data
% Modified from below by Pete Tomlins, QMUL, 18 April 2016
%
% Process a sequence of en face BIN files from QMUL OCT System
% Pete Tomlins, QMUL
% 22 October 2012
%
% Modified from...
% SAM/OCT PNG Data Processor
% Pete Tomlins, QMUL
% 2 May 2012
%
clear all;
%
% OCT Version (1 = Pre-Crash systm <2012/13, 2 = Post-Crash system 2012/13 onwards)
octVersion=2;
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
rootInputFolder='O:\Pete\pt mouth\Papilla 7';
%'N:\Abdi\15. Erosion_Oct_2014_flow\3. Main_Experiment_Sequence_Scans_citric_pH3,8_30092014';
rootInputFolder=strrep(rootInputFolder,'\','/');

rootOutputFolder=rootInputFolder;
rootOutputFolder=strrep(rootOutputFolder,'\','/');

outSAMFolderTitle='SAM';
outSUMFolderTitle='SUM';
outADFolderTitle='AD';
outMeanBScanFolderTitle='Mean BScan';
outMeanAScanFolderTitle='Mean AScan';



if (~exist(rootOutputFolder))
    mkdir(rootOutputFolder);
end


calibrationFolder='N:\Abdi\15. Erosion_Oct_2014_flow\3. Main_Experiment_Sequence_Scans_citric_pH3,8_30092014\Calibration';
calibrationFolder=strrep(calibrationFolder,'\','/');
globalResamplingTablePath=[calibrationFolder '/optimisedResamplingTable.csv'];  % backup resampling table if one isn't available with raw data
globalResamplingTable=dlmread(globalResamplingTablePath);

repeatFolderTitle='.';
positionFolderTitle='.';
bscanFolderTitle='B-Scans';
%
spectraFileName='Spectra.bin';
%
% System version dependent raw data files
%
if (octVersion==1)
    parametersFileName='parameters.csv';
    spectraFileName='Spectra.bin';
    resamplingTableFileName='optimisedResamplingTable.csv';
    referenceSpectrumFileName='SpectralTable.bin';
    referenceAScanFileName='Background.bin';
elseif (octVersion==2)
    parametersFileName='parameters.csv';
    spectraFileName='Spectra.bin';
    resamplingTableFileName='resamplingTable.csv';
    referenceSpectrumFileName='referenceSpectrum.csv';
    referenceAScanFileName='referenceAScan.csv';
end
%
% Manually set the number of repetitions and positions
%
startRepeat=1;
endRepeat=1;
skipRepeat=1;
rCount=startRepeat;
%
startPosition=0;
endPosition=0;
skipPosition=1;
%
topOffset=10;
%
% In this order, loop through, repeats, positions
%
for r=startRepeat:skipRepeat:endRepeat
    rCount=rCount+1;
    %
    % Set the repeat sub folder
    %
    repeatString='';%num2str(r); %sprintf('%0.4i',r);
    repeatSubFolder=[repeatFolderTitle repeatString];
    %
    % Loop through positions
    %
    pCount=0;
    for p=startPosition:skipPosition:endPosition
        
        
        
        pCount=pCount+1;
        %
        % Set the position sub-folder
        %
        %positionSubFolder=[positionFolderTitle sprintf('%0.4i', p)];
        positionSubFolder=positionFolderTitle;  % Not numbered!!!
        octFolder=[rootInputFolder '/' repeatSubFolder '/' positionSubFolder];
        
        outPositionFolder=[rootOutputFolder '/' positionSubFolder];
        if (~exist(outPositionFolder))
            mkdir(outPositionFolder);
        end
        %
        % Make sure that the output folders exist
        %
        outSAMFolder=[outPositionFolder '/' outSAMFolderTitle];
        outSUMFolder=[outPositionFolder '/' outSUMFolderTitle];
        outADFolder = [outPositionFolder '/' outADFolderTitle];
        outMeanBScanFolder = [outPositionFolder '/' outMeanBScanFolderTitle];
        outMeanAScanFolder = [outPositionFolder '/' outMeanAScanFolderTitle];
        %
        if (~exist(outSAMFolder))
            mkdir(outSAMFolder);
        end

        if (~exist(outSUMFolder))
            mkdir(outSUMFolder);
        end

        if (~exist(outADFolder))
            mkdir(outADFolder);
        end
        if (~exist(outMeanBScanFolder))
            mkdir(outMeanBScanFolder);
        end

        if (~exist(outMeanAScanFolder))
            mkdir(outMeanAScanFolder);
        end


        %
        % Load the OCT helper files
        %
        parameters=readtable([octFolder '/' parametersFileName],'ReadVariableNames',false);
        %
        % Get the OCT image dimensions
        %
        numBScans=str2double(parameters{2,2});
        numAScansPerBScan=str2double(parameters{3,2});
        spectrumLength=1024;
        ascanLength=floor(spectrumLength/2);
        %
        % Define window function
        %
        window=blackman(spectrumLength);
        %
        % Load the OCT volume data
        %
        disp('Loading raw spectra...');
        fidSpectra=fopen([octFolder '/' spectraFileName]);
        spectra=fread(fidSpectra,[spectrumLength*numAScansPerBScan*numBScans],'uint16');
        fclose(fidSpectra);
        disp('Done.');
        spectra=reshape(spectra,[spectrumLength,numAScansPerBScan,numBScans]);
        %
        disp('Loading support files...');
        if (octVersion==1)
            spectrumLength=1024;
            %
            % Read the resampling table
            %
            try
                resamplingTable=dlmread(['N:/NAS1_Backup_20141008/OCT_Data/Calibration/Old System Resampling Table/' resamplingTableFileName]);
                resamplingTable=[(1:spectrumLength)',resamplingTable'];
            catch
                disp('Unable to load resampling table for this sample, falling back to global calibration');
                resamplingTable=globalResamplingTable;
            end
            %
            % Read the stray light
            %
            fidStrayLight=fopen([octFolder '/StrayLight.bin']);
            strayLight=fread(fidStrayLight,[spectrumLength,1],'int16');
            fclose(fidStrayLight);
            %
            % Read the reference spectrum
            %
            fidReferenceSpectrum=fopen([octFolder '/' referenceSpectrumFileName]);
            referenceSpectrum=fread(fidReferenceSpectrum,[spectrumLength,1],'float32');
            fclose(fidReferenceSpectrum);
            
            %
            % Read the reference A-Scan
            %
            fidReferenceAScan=fopen([octFolder '/' referenceAScanFileName]);
            referenceAScan=fread(fidReferenceAScan,'float32');
            fclose(fidReferenceAScan);
            %
        elseif (octVersion==2)
            spectrumLength=str2double(parameters{6,2});
            %
            % Read in the resampling table
            %
            try
                resamplingTable=dlmread([octFolder '/' resamplingTableFileName]);
            catch
                disp('Unable to load resampling table for this sample, falling back to global calibration');
                resamplingTable=globalResamplingTable;
            end
                
            %
            % Read in the reference spectrum
            %
            try
                referenceSpectrum=dlmread([octFolder '/' referenceSpectrumFileName]);
                referenceSpectrum=referenceSpectrum(:,2);
            catch
                disp('Unable to load reference spectrum for this sample, estimating from raw spectra...');
                referenceSpectrum=EstimateReferenceSpectrum(spectra,1);
            end
            %
            % No stray light data for version 2 files
            %
            strayLight=zeros(spectrumLength,1);
            %
            % Read in the reference A-Scan
            %
            try
                referenceAScan=dlmread([octFolder '/' referenceAScanFileName]);
                referenceAScan=referenceAScan(:,2);
            catch
                disp('Unable to load reference A-Scan for this sample, assuming zero');
                referenceAScan=zeros(floor(spectrumLength/2),1);
            end
        end
        disp('Done.');
        %
        % Now create the OCT image volume A-Scan by A-Scan- this allows us
        % to compute SAM and AD data and images
        %
        linearVolume=zeros(ascanLength,numAScansPerBScan,numBScans);
        logVolume=zeros(ascanLength,numAScansPerBScan,numBScans);
        for b=1:numBScans
           disp(['Processing B-Scan ' num2str(b) ' of ' num2str(numBScans) '...']);
           for a=1:numAScansPerBScan
               [linAScanEnvelope,logAScanEnvelope,ascan]=ProcessOCTAScan(spectra(:,a,b),resamplingTable,referenceSpectrum,referenceAScan,strayLight, window);
               linearVolume(:,a,b)=linAScanEnvelope;
               logVolume(:,a,b)=logAScanEnvelope;
               
               
           end
        end
        meanBScan=mean(linearVolume(:,:,240:260),3);
        logMeanBScan=20*log10(meanBScan);
        
        meanAScan=mean(meanBScan(:,240:260),2);
        %
        % Estimate the surface position by finding the location of the
        % maximum
        %
        [maximum,maxInd]=max(meanAScan(topOffset:end));
        maxInd=maxInd+topOffset;
        %
        % Compute the projection image
        %
        SUM=squeeze(sum(linearVolume(maxInd-topOffset:floor(ascanLength/4),:,:),1));
        %
        % Offset by 20 pixels and extract the exponential decay over 30
        % pixels
        %
        scatterStart=maxInd+5;
        scatterEnd=scatterStart+10;
        %
        scatterSlope=meanAScan(scatterStart:scatterEnd);
        vx=(0:scatterEnd-scatterStart)';
        [fittedParams,squaredError,FittedCurve] = ExpFit(vx,scatterSlope, [scatterSlope(1),1]);
        %
        meanScatteringCoefficient(rCount,pCount)=fittedParams(2);
        meanScatteringAmplitude(rCount,pCount)=fittedParams(1);
        %
        for z=maxInd:ascanLength
           ratio=ascan(z)/maximum;
           if (ratio<1/exp(1)^2)
               break;
           end
        end
        dz=z-maxInd;
        meanAttenuationDepth(rCount,pCount)=dz;
        %
        % Loop over volume again and map the attenuation coefficient
        %
        SAM=zeros(numAScansPerBScan,numBScans);
        AD=SAM;
        for b=1:numBScans
            disp(['Computing row ' num2str(b) ' of SAM image...']);
            for a=1:numAScansPerBScan
                scatterSlope=linearVolume(scatterStart:scatterEnd,a,b);
                vx=(0:scatterEnd-scatterStart)';
                [fittedParams,squaredError,FittedCurve] = ExpFit(vx,scatterSlope, [meanScatteringAmplitude(rCount,pCount),meanScatteringCoefficient(rCount,pCount)]);
                SAM(a,b)=fittedParams(2);
                %
                % Find the depth at which the OCT intensity falls to 1/e^2 of
                % maximum
                %
                ascan=linearVolume(:,a,b);
                [ascanMax,ascanMaxInd]=max(ascan(topOffset:end));
                zz=ascanMaxInd+topOffset;    % Make sure z is set
                for z=ascanMaxInd+topOffset:ascanLength-topOffset
                   ratio=ascan(z)/maximum;
                   if (ratio<1/exp(1)^2)
                       zz=z;
                       break;
                   end
                end
                dz=zz-ascanMaxInd;
                AD(a,b)=dz;
            end
        end
        
        minSAM=0;
        maxSAM=0.05;  % attenuation in pixel^-1
        
        minAD=0;
        maxAD=30;  % depth in pixels
        
        minSUM=0;
        maxSUM=50;   %intensity 
        
        minBScan=-40;   % dB
        maxBScan=20;
        
        %samImg=(SAM-minSAM)/(maxSAM-minSAM) * 255;
        %samImg(samImg<0)=0;
        %samImg(samImg>255)=255;
        SaveImage([outSAMFolder '/' 'SAM' repeatString '.png'],SAM,minSAM,maxSAM);
        SaveImage([outSUMFolder '/' 'SUM' repeatString '.png'],SUM,minSUM,maxSUM);
        SaveImage([outADFolder '/' 'attenuationDepth' repeatString '.png'],AD,minAD,maxAD);
        SaveImage([outMeanBScanFolder '/' 'meanBScan' repeatString '.png'],20*log10(meanBScan),minBScan,maxBScan);
        %minSUM
        %outSAMFolder=[outPositionFolder '/' outSAMFolderTitle];
        %outSUMFolder=[outPositionFolder '/' outSUMFolderTitle];
        %outADFolder = [outPositionFolder '/' outADFolderTitle];
        %outMeanBScanFolder = [outPositionFolder '/' outMeanBScanFolderTitle];
        %outMeanAScanFolder = [outPositionFolder '/' outMeanAScanFolderTitle];
        %
        % Use the volume data to find the noise threshold and estimate the
        % surface location... maybe Gaussian fit to the linear plot?
        %
        dlmwrite([outADFolder '/' 'attenuationDepth' repeatString '.csv'],AD);
        dlmwrite([outSAMFolder '/' 'SAM' repeatString '.csv'],SAM);
        dlmwrite([outSUMFolder '/' 'SUM' repeatString '.csv'],SUM);
        dlmwrite([outMeanBScanFolder '/' 'meanBScan' repeatString '.csv'],meanBScan);
        dlmwrite([outMeanAScanFolder '/' 'meanAScan' repeatString '.csv'],meanAScan);
        fid=fopen([octFolder '/' 'reprocessedLinearVolume.bin'],'w');
        fwrite(fid,linearVolume,'float32');
        fclose(fid);
        disp('Volume complete.');
    end
    
    
end

break;

