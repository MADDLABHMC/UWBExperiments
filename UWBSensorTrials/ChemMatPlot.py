import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

ListTime = np.array([0,20,50,100,200,300,400,500,700,1000])
NO2Conc = np.array([0.200,0.091,0.050,0.029,0.015,0.010,0.008,0.006,0.005,0.003])


df = pd.DataFrame({"Time" : ListTime, "[NO2]" : NO2Conc})

lnNO2 = []
for element in NO2Conc:
    lnNO2.append(round(math.log(element),2))

lnNO2 = np.array(lnNO2)
df['[NO2]^-1'] = round(1/df['[NO2]'], 2)
df['ln[NO2]'] = lnNO2

   

print(df)
fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = (40, 7))

ax[0].plot(df['Time'], df['[NO2]'])
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("[NO2] (mM)")
ax[0].set_title("Concentration of NO2 vs Time")

ax[1].plot(df['Time'], df['ln[NO2]'])
ax[1].set_xlabel("Time (s)")
ax[1].set_ylabel("ln[NO2] (no Unit)")
ax[1].set_title("Concentration of ln(NO2) vs Time")

ax[2].plot(df['Time'], df['[NO2]^-1'])
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("[NO2]^-1 (mM)^-1")
ax[2].set_title("Concentration of 1/NO2 vs Time")



plt.show()