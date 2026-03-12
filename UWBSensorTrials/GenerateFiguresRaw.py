import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation
import os 
import regex as re
from matplotlib.backends.backend_pdf import PdfPages










ListDfDict = {}
GlobalX = 0
GlobalY = 0


def __main__():
    global ListDfDict
    global GlobalX, GlobalY
    
    
#filename1 = "Mar7Tests/Mar7Tests_Translated_To_CSV/Mar7_0HZ.csv"
#filename2 = "Mar7Tests/Mar7Tests_Translated_To_CSV/Mar7_94HZ.csv"
#filename2 = "RealTests/SecondProg13_672Hz.csv"
#filename3 = "RealTests/ThirdProg35_400Hz.csv"
#filename4 = "RealTests/MediumBaselineFourth44_189Hz.csv"
#filename5 = "RealTests/Fifth3_906Hz.csv"

    InputSelection = input("Please enter exactly your tests folder that contains the Translated To CSV subfolder: ")
    PossibleFilesandDs = os.listdir(f'{InputSelection}')
    
    
    if(f'{InputSelection}_Translated_To_CSV' in PossibleFilesandDs):
        print("Succesfully Found Translated Folder")
        
        
    else:
        raise NameError("Unable to find proper folder")
    
    
    csvs = os.listdir(f'{InputSelection}/{InputSelection}_Translated_To_CSV')
   
    print(f'Found {len(csvs)} files to analyze')
    #create condition and IndexError raise if there's too many files.
    #Start sort by Hz:
    csvs.sort(key = lambda x: int(x[x.index("_")+1:re.search(r'Hz', x).start()])) # re.searcg guves a natg object, and we want to start
    print(csvs)
    
    for files in csvs:
        df = pd.read_csv(f'{InputSelection}/{InputSelection}_Translated_To_CSV/{files}')
        ListDfDict[int(files[files.index("_")+1:re.search(r'Hz', files).start()])] = df
    print("Data Frames Created")
    print(f'Dict status in Hz: {ListDfDict.keys()}')
    OrderedKeys = list(ListDfDict.keys()) 
        

#dfBase = pd.read_csv(filename1)
#dfSecond = pd.read_csv(filename2)
#dfThird = pd.read_csv(filename3)
#dfFourth = pd.read_csv(filename4)
#dfFifth = pd.read_csv(filename5)


    fig, ax = plt.subplots(nrows = 2, ncols = len(csvs), figsize = (20,10))
    
    try:
        GlobalX = float(input("Please enter your True X position in meters: "))
        GlobalY = float(input("Please enter your True Y position in meters: "))
        if(len(str(GlobalX).split(".")[1]) > 2):
            GlobalX = round(GlobalX, 2)
        if(len(str(GlobalY).split(".")[1]) > 2):
            GlobalY = round(GlobalY, 2)
        
    except ValueError:
        print("You did not enter a valid input.")
    
    for i in range(len(OrderedKeys)):
        ax[0][i].plot(ListDfDict[OrderedKeys[i]]['#Time'], ListDfDict[OrderedKeys[i]]['X'])
        ax[0][i].set_title(f'{OrderedKeys[i]} Hz X')
        ax[0][i].set_xlabel("Time (s)")
        ax[0][i].set_ylabel("X pos (m)")
        ax[1][i].plot(ListDfDict[OrderedKeys[i]]['#Time'], ListDfDict[OrderedKeys[i]]['Y'])
        ax[1][i].set_title(f'{OrderedKeys[i]} Hz Y')
        ax[1][i].set_xlabel("Time (s)")
        ax[1][i].set_ylabel("Y pos (m)")
        ax[0][i].grid(True)
        ax[1][i].grid(True)
        
        
        
        
        
    plt.show()
        
        
        
        
    
        

#40 - 160
#ax[0][0].plot(dfBase['#Time'], dfBase['X'])
#ax[0][0].set_title("X 0 Hz")

#ax[0][1].plot(dfSecond['#Time'], dfSecond['X'])
#ax[0][1].set_title("X 94 Hz")

#
#ax[1][0].plot(dfBase['#Time'], dfBase['Y'])
#ax[1][0].set_title("Y 0 Hz")


#ax[1][1].plot(dfSecond['#Time'], dfSecond['Y'])
#x[1][1].set_title("Y 94 Hz")


#ax[0][3].plot(dfFourth['#Time'], dfFourth['X'])
#ax[0][3].set_title("X Fourth")


#ax[0][4].plot(dfFifth['#Time'], dfFifth['X'])
#ax[0][4].set_title("X Fifth")


# Sep Top row from bottom row

#ax[1][0].plot(dfBase['#Time'], dfBase['Y'])
#ax[1][0].set_title("Y Base")


#ax[1][1].plot(dfSecond['#Time'], dfSecond['Y'])
#ax[1][1].set_title("Y Second")


#ax[1][2].plot(dfThird['#Time'], dfThird['Y'])
#ax[1][2].set_title("Y Third")


#ax[1][3].plot(dfFourth['#Time'], dfFourth['Y'])
#ax[1][3].set_title("Y Fourth")


#ax[1][4].plot(dfFifth['#Time'], dfFifth['Y'])
#ax[1][4].set_title("Y Fifth")

#TrueLocationXInches = 26.5 # true location 25.5 - 26.5 100% confidence mar 7 update
#TrueLocationYInches = 25.5 # True locations of Mar 7 updated between 25-26 100% conf true


#TrueLocationXMeters = round(float(TrueLocationXInches/39.37),4)
#TrueLocationYMeters = round(float(TrueLocationYInches/39.37), 4)

#for i in range(len(ListOfDataFrames)):
    #ax[0][i].plot(np.array([0, ListOfDataFrames[i]['#Time'].iloc[-1]]), np.array([TrueLocationXMeters, TrueLocationXMeters]), color = 'red')
    #ax[1][i].plot(np.array([0, ListOfDataFrames[i]['#Time'].iloc[-1]]), np.array([TrueLocationYMeters, TrueLocationYMeters]), color = 'red')
    
#ax[0][0].plot(np.array([ListOfDataFrames[0]['#Time'].iloc[0], ListOfDataFrames[0]['#Time'].iloc[-1]]), np.array([TrueLocationXMeters, TrueLocationXMeters]), color = 'red')
#ax[0][1].plot(np.array([ListOfDataFrames[1]['#Time'].iloc[0], ListOfDataFrames[1]['#Time'].iloc[-1]]), np.array([TrueLocationXMeters, TrueLocationXMeters]), color = 'red')

#x[1][0].plot(np.array([ListOfDataFrames[0]['#Time'].iloc[0], ListOfDataFrames[0]['#Time'].iloc[-1]]), np.array([TrueLocationYMeters, TrueLocationYMeters]), color = 'red')
#ax[1][1].plot(np.array([ListOfDataFrames[1]['#Time'].iloc[0], ListOfDataFrames[1]['#Time'].iloc[-1]]), np.array([TrueLocationYMeters, TrueLocationYMeters]), color = 'red')


#plt.show()

__main__()