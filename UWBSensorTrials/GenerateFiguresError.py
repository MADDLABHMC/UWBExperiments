#From NoteFeb23.txt, we saw that the recorded true location was 28 inches from the bottom, 24 inches from the side (24,28) in inches
import pandas as pd
import matplotlib.pyplot as plt

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

#print(f'True Location X (m): {TrueLocationXMeters}')
#print(f'True Location Y (m): {TrueLocationYMeters}')

DFBase = pd.read_csv(filename1)
DFSecond = pd.read_csv(filename2)
DFThird = pd.read_csv(filename3)
DFFourth = pd.read_csv(filename4)
DFFifth = pd.read_csv(filename5)

DFBase['XResidualE'] = DFBase['X'] - TrueLocationXMeters
DFBase['YResidualE'] = DFBase['Y'] - TrueLocationYMeters

DFSecond['XResidualE'] = DFSecond['X'] - TrueLocationXMeters
DFSecond['YResidualE'] = DFSecond['Y'] - TrueLocationYMeters

DFThird['XResidualE'] = DFThird['X'] - TrueLocationXMeters
DFThird['YResidualE'] = DFThird['Y'] - TrueLocationYMeters

DFFourth['XResidualE'] = DFFourth['X'] - TrueLocationXMeters
DFFourth['YResidualE'] = DFFourth['Y'] - TrueLocationYMeters

DFFifth['XResidualE'] = DFFifth['X'] - TrueLocationXMeters
DFFifth['YResidualE'] = DFFifth['Y'] - TrueLocationYMeters

fig, ax = plt.subplots(nrows =2, ncols = 5, figsize=(20,10))

ax[0][0].plot(DFBase['#Time'], DFBase['XResidualE'])
ax[0][0].set_title("X Resid. B")

ax[0][1].plot(DFSecond['#Time'], DFSecond['XResidualE'])
ax[0][1].set_title("X Resid. 2")

ax[0][2].plot(DFThird['#Time'], DFThird['XResidualE'])
ax[0][2].set_title("X Resid. 3")

ax[0][3].plot(DFFourth['#Time'], DFFourth['XResidualE'])
ax[0][3].set_title("X Resid. 4")

ax[0][4].plot(DFFifth['#Time'], DFFifth['XResidualE'])
ax[0][4].set_title("X Resid. 5")

# Sep Top row from bottom row

ax[1][0].plot(DFBase['#Time'], DFBase['YResidualE'])
ax[1][0].set_title("Y Resid. B")

ax[1][1].plot(DFSecond['#Time'], DFSecond['YResidualE'])
ax[1][1].set_title("Y Resid. 2")

ax[1][2].plot(DFThird['#Time'], DFThird['YResidualE'])
ax[1][2].set_title("Y Resid. 3")

ax[1][3].plot(DFFourth['#Time'], DFFourth['YResidualE'])
ax[1][3].set_title("Y Resid. 4")

ax[1][4].plot(DFFifth['#Time'], DFFifth['YResidualE'])
ax[1][4].set_title("Y Resid. 5")

plt.show()






