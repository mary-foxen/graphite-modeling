temps = KResultsUncertainty95CI2.Temperature_C;
temps = temps+273;
specheat = KResultsUncertainty95CI2.AvgSpeciHeat_J_gK;
temps_cut = temps(1:25);
% temps_cut = 20+temps_cut;
specheat_cut = specheat(1:25);
plot(temps_cut, specheat_cut)
alpha = KResultsUncertainty95CI2.AvgThermDiff_mm2_s;
figure(2)
plot(temps, alpha)
% General model:
%      f(x) = a+b*x+c*1/x+d*1/x^2+e*1/x^3+f*1/x^4
% Coefficients (with 95% confidence bounds):
%        a =       1.597
%        b =   0.0002746
%        c =      -117.8
%        d =     -0.2472
%        e =      0.7528
%        f =       0.276
% 
% Goodness of fit:
%   SSE: 0.0002543
%   R-square: 0.9974
%   Adjusted R-square: 0.9956
%   RMSE: 0.006027

General model:
     f(x) = a+c*x^-1+d*x^-2+e*x^-3+f*x^-4+g*x^-5
Coefficients (with 95% confidence bounds):
       a =       2.126
       c =      -481.5
       d =     -0.6239
       e =      0.9443
       f =      0.4909
       g =      0.4893

Goodness of fit:
  SSE: 0.0003139
  R-square: 0.9968
  Adjusted R-square: 0.9945
  RMSE: 0.006696




% General model:
%      f(x) = a+b*x+c*1/x+d*1/x^2+e*1/x^3+f*1/x^4
% Coefficients (with 95% confidence bounds):
%        a =       4.226  (4.015, 4.436)
%        b =  -0.0006108  (-0.000768, -0.0004536)
%        c =        1149  (1074, 1223)
%        d =  -8.437e+04  (-9.311e+04, -7.563e+04)
%        e =    2.72e+06  (2.352e+06, 3.087e+06)
%        f =  -3.053e+07  (-3.536e+07, -2.57e+07)
% 
% Goodness of fit:
%   SSE: 0.2029
%   R-square: 0.9989
%   Adjusted R-square: 0.9988
%   RMSE: 0.06188

% General model:
%      f(x) = a+c*x^-1+d*x^-2+e*x^-3+f*x^-4+g*x^-5
% Coefficients (with 95% confidence bounds):
%        a =       2.645
%        c =        2550
%        d =       9.768
%        e =       1.029
%        f =     0.07818
%        g =      0.4427
% 
% Goodness of fit:
%   SSE: 0.2187
%   R-square: 0.9988
%   Adjusted R-square: 0.9987
%   RMSE: 0.06423

General model:
     f(x) = a+b*x+c*x^-1+d*x^-2+e*x^-3+f*x^-4+g*x^-5
Coefficients (with 95% confidence bounds):
       a =       2.187
       b =   0.0003048
       c =        2688
       d =       13.66
       e =      0.1724
       f =      0.9421
       g =      0.9561

Goodness of fit:
  SSE: 0.1172
  R-square: 0.9994
  Adjusted R-square: 0.9993
  RMSE: 0.04748



