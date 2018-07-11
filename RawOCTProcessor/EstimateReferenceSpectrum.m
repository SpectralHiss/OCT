%
% Estimate the source spectrum by averaging and smoothing the OCT spectral
% data - useful when the raw spectrum is unavailable
%
function [referenceSpectrum]=EstimateReferenceSpectrum(spectra, smoothingKernelSize)
            %
            % Assume spectra is a 3D matrix
            %
            meanSpec3=mean(spectra,3);
            meanSpec2=mean(meanSpec3,2);
            referenceSpectrum=medfilt1(meanSpec2,smoothingKernelSize);
end