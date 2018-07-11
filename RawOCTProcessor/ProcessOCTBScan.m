%
% Process an OCT B-Scan
%
function [bscan]=ProcessOCTBScan(spectra,resamplingTable,referenceSpectrum,referenceAScan,strayLight, window)

    numAScans=size(spectra,2);
    
    
    for a=1:numAScans
        spectrum=spectra(:,a);
        [linAScanEnvelope,logAScanEnvelope,ascan]=ProcessOCTAScan(spectrum,resamplingTable,referenceSpectrum,referenceAScan,strayLight, window);
        if (a==1)
            bscan=zeros(max(size(linAScanEnvelope)),numAScans);
        end
        bscan(:,a)=linAScanEnvelope;
    end
end