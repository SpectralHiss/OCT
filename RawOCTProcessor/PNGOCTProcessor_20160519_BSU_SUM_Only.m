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
% 2 May 20162
% 19 May 2016 - Re-processing BSU data and using linear domain averaging
%24 May 2016 - Summation over Z direction from original pngs
%
clear all;
%
% OCT Version (1 = Pre-Crash systm <2012/13, 2 = Post-Crash system 2012/13 onwards)
octVersion=2;
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
rootInputFolder='C:\Users\OCT\OneDrive - Queen Mary, University of London\Shared OCT Data\BSU - November 2015\BSU 2015 - Mouse 3\Time-lapse';
%'C:\Users\OCT\OneDrive - Queen Mary, University of London\Shared OCT Data\BSU - November 2015\BSU2015 -  Day 1\Time-lapse 4';
rootInputFolder=strrep(rootInputFolder,'\','/');

rootOutputFolder=rootInputFolder;
rootOutputFolder=strrep(rootOutputFolder,'\','/');

outHyperStackFolderTitle='HyperStack';
outSUMFolderTitle='SUM';



if (~exist(rootOutputFolder))
    mkdir(rootOutputFolder);
end

repeatFolderTitle='Repeat';
positionFolderTitle='Position';
bscanFolderTitle='B-Scans';
%
% Manually set the number of repetitions and positions
%
startRepeat=0;
endRepeat=25;
skipRepeat=1;
rCount=startRepeat;
%
startPosition=0;
endPosition=1;
skipPosition=1; 

startBScan=0;
endBScan=499;
numBScans=endBScan-startBScan+1;
%
top=25;
bottom=200;
%
% In this order, loop through, repeats, positions
%
for r=startRepeat:skipRepeat:endRepeat
    rCount=rCount+1;
    %
    % Set the repeat sub folder
    %
    repeatString=sprintf('%0.4i',r);
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
        positionSubFolder=[positionFolderTitle sprintf('%0.4i', p)];
        octFolder=[rootInputFolder '/' repeatSubFolder '/' positionSubFolder '/' bscanFolderTitle];
        
        outPositionFolder=[rootOutputFolder '/' positionSubFolder];
        if (~exist(outPositionFolder))
            mkdir(outPositionFolder);
        end
        %
        % Make sure that the output folders exist
        %
       % outSAMFolder=[outPositionFolder '/' outSAMFolderTitle];
       outSUMFolder=[outPositionFolder '/' outSUMFolderTitle];
       outHyperStackFolder=[outPositionFolder '/' outHyperStackFolderTitle];
       % outADFolder = [outPositionFolder '/' outADFolderTitle];
        %outMeanBScanFolder = [outPositionFolder '/' outMeanBScanFolderTitle];
       % outMeanAScanFolder = [outPositionFolder '/' outMeanAScanFolderTitle];
        %
        if (~exist(outHyperStackFolder))
            mkdir(outHyperStackFolder);
        end
        
        if (~exist(outSUMFolder))
            mkdir(outSUMFolder);
        end



        %
        % Load pngs into a volume
        %
        
        for b=startBScan:endBScan
            bb=b-startBScan+1;
            
            
            bscanStr=sprintf('%0.4i',b);
            
            
            
            img=imread([octFolder '/' 'OCTImage' bscanStr '.png']);
            if (b==startBScan)
                ascanLength=size(img,1);
                numAScansPerBScan=size(img,2);
                volume=zeros(ascanLength,numAScansPerBScan,numBScans);
            end
            disp(['Processing B-Scan ' num2str(b) ' of ' num2str(numBScans) '...']);
            
            volume(:,:,bb)=squeeze(img(:,:,1));
            
            %
            %Out put to hyperstack folder
            %
            imwrite(img,[outHyperStackFolder  '/' 'HyperStack_t=' num2str(r) '_bscan=' num2str(b) '.png']); 
        end
       
        sum=mean(volume(top:bottom,:,:));
        
        sumImg=uint8(sum);
        imwrite(squeeze(sumImg),[outSUMFolder '/' 'sum_t=' num2str(r) '.png']);
           

           
    end
end
