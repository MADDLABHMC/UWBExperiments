import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
#from matplotlib.animation import FuncAnimation
import os 
import regex as re
from matplotlib.backends.backend_pdf import PdfPages as pdf
from datetime import datetime
import math










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


    #fig, ax = plt.subplots(nrows = 2, ncols = len(csvs), figsize = (20,10))
    
    try:
        GlobalX = float(input("Please enter your True X position in meters: "))
        GlobalY = float(input("Please enter your True Y position in meters: "))
        if(len(str(GlobalX).split(".")[1]) > 2):
            GlobalX = round(GlobalX, 2)
        if(len(str(GlobalY).split(".")[1]) > 2):
            GlobalY = round(GlobalY, 2)
        
    except ValueError:
        print("You did not enter a valid input.")
        
    OfficialNow = str(datetime.now().strftime("D%Y_%m_%d-T%H-%M-%S"))
    #str is redundant but whatever

        
    if("RawOutputReports" not in os.listdir()): 
        os.makedirs("RawOutputReports", mode=0o777, exist_ok=False)
    
    FullNumPages = math.floor(len(OrderedKeys)/2)
    RemainderGraphs = len(OrderedKeys) % 2
    #if int(FullNumPages) < 1:
        #raise ValueError("You don't have enough data to generate a solid report.")
    
    Counter = 0
    PageCounter = 1
    
    with pdf(f'RawOutputReports/{OfficialNow}-{InputSelection}.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5))
                for i in range(0, 2):
                    ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'],ListDfDict[OrderedKeys[Counter + i]]['X'], color = 'blue')
                    ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                    ax[0][i].set_xlabel('time (s)')
                    ax[0][i].set_ylabel('X (m)')
                    ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[0],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[-1]]),np.array([GlobalX, GlobalX]),color = 'red')
                        ## switch from x on first row to Y on bottom row
                    ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'],ListDfDict[OrderedKeys[Counter + i]]['Y'], color = 'blue')
                    ax[1][i].set_xlabel('time (s)')
                    ax[1][i].set_ylabel('Y (m)')
                    ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[0],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[-1]]),np.array([GlobalY, GlobalY]), color = 'red')
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter += 2
                fig.suptitle(f'Page {PageCounter}')
                PageCounter += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5))
            for i in range(int(RemainderGraphs)):
                ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'],ListDfDict[OrderedKeys[Counter + i]]['X'], color = 'blue')
                ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                ax[0][i].set_xlabel('time (s)')
                ax[0][i].set_ylabel('X (m)')
                ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[0],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[-1]]),np.array([GlobalX, GlobalX]), color = 'red')
                        ## switch from x on first row to Y on bottom row
                ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'],ListDfDict[OrderedKeys[Counter + i]]['Y'], color = 'blue')
                ax[1][i].set_xlabel('time (s)')
                ax[1][i].set_ylabel('Y (m)')
                ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[0],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[-1]]),np.array([GlobalY, GlobalY]), color = 'red')
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter += RemainderGraphs
            fig.suptitle(f'Page {PageCounter}')
            PageCounter += 1
            file.savefig(fig)
            plt.close(fig)
                
                
      
    print(f'Succesful pdf Write of {PageCounter-1} pages and {Counter} graphs.')

    
    with open(f'RawOutputReports/{OfficialNow}-{InputSelection}.info', 'w') as file:
        file.write(f'Chosen true X position in meters: {GlobalX}\n')
        file.write(f'Chosen true Y position in meters: {GlobalY}\n')
        file.write(f'files analyzed {" ".join(csvs)}\n')
        file.write(f'Frequencies in impact Hz: {" ".join([str(strings) for strings in OrderedKeys])}\n')
        file.write(f'{Counter} graphs and {PageCounter - 1} pages succesfully written')
    
    print(f'Info file succesfully written')
        
        
    
    
# Problematic becuase we want max 3 on a page
"""  for i in range(len(OrderedKeys)):
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
"""
        

        
        
        
        
    #plt.show()
        
        
        
        
    
        

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