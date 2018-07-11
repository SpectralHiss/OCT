%
% Function to process a single raw spcetrum into an OCT A-Scan
% Pete Tomlins, QMUL, 19 April 2016
%
function [linAScanEnvelope,logAScanEnvelope,ascan]=ProcessOCTAScan(spectrum,resamplingTable,referenceSpectrum,referenceAScan,strayLight, window)

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
        ft=fft(windowed);

        ascan=ft(1:ascanLength);
        
        linAScanEnvelope=abs(ascan) - referenceAScan(1:ascanLength);
        %linAScanEnvelope=linAScanEnvelope-mean( linAScanEnvelope( floor(0.75*ascanLength):end ) );
        logAScanEnvelope=20*log10(linAScanEnvelope);% - referenceAScan(1:ascanLength);;

end