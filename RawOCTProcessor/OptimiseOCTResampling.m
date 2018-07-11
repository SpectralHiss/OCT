function [fittedParams,resamplingTable,bscanContrast] = OptimiseOCTResampling(bscanSpectra,referenceSpectrum,referenceAScan,strayLight, window, Order, startParams)
%
% Modified from help example for curve fitting using optimization
%
% Call fminsearch with a random starting point.
%start_point = rand(1, 2);

model = @fun;
squaredError = 0;
k_OptimOptions = optimset('Display','off','TolFun',1e-3,'TolX',1e-3);
fittedParams = fminsearch(model, startParams, k_OptimOptions);
%
% The error and model function
%  
    function [sse] = fun(params)
        % params represent the coefficients of a polynomial
        % y=params(1)+params(2)*x + params(3)*x^2 + ... + params(Order+1)
        % * x^(Order)
        %
        spectrumLength=size(bscanSpectra,1);
        resamplingTable=zeros(spectrumLength,2);
        for i=1:spectrumLength
            resamplingTable(i,1)=i-1;
            for o=1:Order+1
                resamplingTable(i,2)=resamplingTable(i,2)+params(o)* resamplingTable(i,1)^(o-1);
            end
        end
        %
        % Scale the resampling table such that its end points are at 1023
        % and 0
        %
        vec=resamplingTable(:,2);
        minVec=min(vec);
        maxVec=max(vec);
        
        if (vec(end) > minVec)
            vec=flipud((0:1023)');
        else
        
            vec=(vec-minVec)/(maxVec-minVec) * 1023;
        end
        resamplingTable(:,2)=vec;
        
        
        
        
        bscan=ProcessOCTBScan(bscanSpectra,resamplingTable,referenceSpectrum,referenceAScan,strayLight, window);
        bscan=bscan(50:end,:);
        
        minVal=min(min(bscan));
        maxVal=max(max(bscan));
        normBScan=(bscan-minVal)/(maxVal-minVal);
        
        bscanContrast=GetImageContrast(normBScan);
        sse=-bscanContrast;
        disp(num2str(sse));
        
    end
end