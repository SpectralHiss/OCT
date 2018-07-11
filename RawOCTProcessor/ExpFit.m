%
% Simple exponential fit
% Pete Tomlins, QMUL, 19 April 2016
%
function [fittedParams,squaredError,FittedCurve] = ExpFit(xdata,ydata, startParams)
%
% Modified from help example for curve fitting using optimization
%
% Call fminsearch with a random starting point.
%start_point = rand(1, 2);

model = @fun;
squaredError = 0;
k_OptimOptions = optimset('Display','off');
fittedParams = fminsearch(model, startParams, k_OptimOptions);
%
% The error and model function
%  
    function [sse] = fun(params)
        %A = params(1);
        %x0 = params(2);
        %wx = params(3);
        %z0 = params(4);
        %wz = params(5);
        %k = params(6);
        A=params(1);
        mu=params(2);
        %
        FittedCurve = A .* exp(-mu * xdata);
        ErrorVector = FittedCurve - ydata;
        sse = sum(ErrorVector .^ 2);
        squaredError = sse;
    end
end