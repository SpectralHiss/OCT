%
% Function to process a single raw spcetrum into an OCT A-Scan
% Pete Tomlins, QMUL, 19 April 2016
%
% Modified by PT 9 November 2017 to use pwelch - display power spectral
% density instead of magnitude
%
function [linAScanEnvelope,logAScanEnvelope,ascan]=ProcessOCTAScanPSD(spectrum,resamplingTable,referenceSpectrum,referenceAScan,strayLight, window,psdSegmentLength)

        spectrumLength=max(size(spectrum));
        ascanLength=floor(spectrumLength/2);
        % Subtract stray light info (zeros in version 2 data files, version 1 contains a spectrometer dark reading)
        corrected=spectrum-strayLight;

        % Deconvolve
        deconv=(corrected ./ referenceSpectrum);

        meanDeconv=mean(deconv);
        %
        % Mean centre
        %
        meanCentred=deconv-meanDeconv;

        % Resample
        resampled=spline(resamplingTable(:,1),meanCentred,resamplingTable(:,2));

        % Window
        windowed=resampled .* window;

        % Fourier transform
        if (psdSegmentLength < 1)  % If zero segments are specified, then just fft
            ft=fft(windowed);
            ascan=abs(ft(1:ascanLength));
        else % Otherwise estimate the power spectral density
            overlap=int32(psdSegmentLength/2);
            psd=pwelch(windowed,psdSegmentLength,overlap,size(windowed,1)); %fft(windowed);
            ascan=psd(1:ascanLength);%ft(1:ascanLength);
        end
        %env=abs(ascan);
        
        linAScanEnvelope=ascan;%abs(ascan) - referenceAScan(1:ascanLength);
        %linAScanEnvelope=linAScanEnvelope-mean( linAScanEnvelope( floor(0.75*ascanLength):end ) );
        logAScanEnvelope=20*log10(linAScanEnvelope);% - referenceAScan(1:ascanLength);;

end