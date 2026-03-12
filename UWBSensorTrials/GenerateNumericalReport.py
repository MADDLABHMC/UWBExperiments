import pandas as pd

import numpy as np


filename1 = "RealTests/BaseProg15_896Hz.csv"
filename2 = "RealTests/SecondProg13_672Hz.csv"
filename3 = "RealTests/ThirdProg35_400Hz.csv"
filename4 =  "RealTests/MediumBaselineFourth44_189Hz.csv"
filename5 = "RealTests/Fifth3_906Hz.csv"

TrueLocationXInches = 24.0
TrueLocationYInches = 28.0


#Conversion source from google to 4 decimal numbers --> 4 sig figs
TrueLocationXMeters = round(float(TrueLocationXInches/39.37),4)
TrueLocationYMeters = round(float(TrueLocationYInches/39.37), 4)

DFBase = pd.read_csv(filename1)
DFSecond = pd.read_csv(filename2)
DFThird = pd.read_csv(filename3)
DFFourth = pd.read_csv(filename4)
DFFifth = pd.read_csv(filename5)

DataFrames = [DFBase, DFSecond, DFThird, DFFourth, DFFifth]

# sig figs in this case (Residual should be to 2 decimal points)
DFBase['XResidualE'] = DFBase['X'] - TrueLocationXMeters
DFBase['YResidualE'] = DFBase['Y'] - TrueLocationYMeters
DFBase['XResidualE2'] = np.power((DFBase['XResidualE']),2) 
DFBase['YResidualE2'] = np.power((DFBase['YResidualE']),2) 


DFSecond['XResidualE'] = DFSecond['X'] - TrueLocationXMeters
DFSecond['YResidualE'] = DFSecond['Y'] - TrueLocationYMeters
DFSecond['XResidualE2'] = np.power((DFSecond['XResidualE']),2) 
DFSecond['YResidualE2'] = np.power((DFSecond['YResidualE']),2) 

DFThird['XResidualE'] = DFThird['X'] - TrueLocationXMeters
DFThird['YResidualE'] = DFThird['Y'] - TrueLocationYMeters
DFThird['XResidualE2'] = np.power((DFThird['XResidualE']),2)
DFThird['YResidualE2'] = np.power((DFThird['YResidualE']),2)

DFFourth['XResidualE'] = DFFourth['X'] - TrueLocationXMeters
DFFourth['YResidualE'] = DFFourth['Y'] - TrueLocationYMeters
DFFourth['XResidualE2'] = np.power((DFFourth['XResidualE']),2)
DFFourth['YResidualE2'] = np.power((DFFourth['YResidualE']),2) 

DFFifth['XResidualE'] = DFFifth['X'] - TrueLocationXMeters
DFFifth['YResidualE'] = DFFifth['Y'] - TrueLocationYMeters
DFFifth['XResidualE2'] = np.power((DFFifth['XResidualE']),2) 
DFFifth['YResidualE2'] = np.power((DFFifth['YResidualE']), 2)

SumSquares = [] # in form [x, y] for each DF

SumSquaresX = 0
SumSquaresY = 0


for i in range(len(DataFrames)):
    SumSquaresX = DataFrames[i]['XResidualE2'].sum()
    SumSquaresY = DataFrames[i]['YResidualE2'].sum()
    SumSquares.append([SumSquaresX, SumSquaresY])
    

AveragedSumSquares = []

SQRTAveragedSumSquares = []

AverageSumSquaresX = 0
AverageSumSquaresY = 0

SQRTAveragedSumSquaresX = 0 
SQRTAveragedSumSquaresY = 0

for i in range(len(DataFrames)):
    AverageSumSquaresX = SumSquares[i][0] / len(DataFrames[i]['X'])
    AverageSumSquaresY = SumSquares[i][1] / len(DataFrames[i]['Y'])
    
    SQRTAveragedSumSquaresX = np.sqrt(AverageSumSquaresX)
    SQRTAveragedSumSquaresY = np.sqrt(AverageSumSquaresY)
    
    
    
    AveragedSumSquares.append([AverageSumSquaresX,AverageSumSquaresY])
    SQRTAveragedSumSquares.append([SQRTAveragedSumSquaresX, SQRTAveragedSumSquaresY])

print(f'RME Report in sequence of Base to Highest Prog')
for i in range(len(AveragedSumSquares)):
    print(f'Dataframe: {i + 1}')
    print(f'X: {round(AveragedSumSquares[i][0],6)}')
    print(f'Y: {round(AveragedSumSquares[i][1],6)}')

print("\n\n")



print(f'RMSE Report in sequence of Base to Highest Prog')
for i in range(len(SQRTAveragedSumSquares)):
    print(f'Dataframe: {i + 1 }')
    print(f'X: {round(SQRTAveragedSumSquares[i][0],6)}')
    print(f'Y: {round(SQRTAveragedSumSquares[i][1],6)}')



#Ask about Equal Time interval sampling with Prof. Mohanty

    
    
    
    
    
    


