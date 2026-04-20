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
import pyarrow











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
        df = pd.read_csv(f'{InputSelection}/{InputSelection}_Translated_To_CSV/{files}', dtype = {'#Time': float}, float_precision = 'round_trip') # round trip ensures that we whenwe convert the float back to the a string, we get the string back - so it imagines my values to be strings, turns it into a float, and then turns it back into a string to check if it matches the og string
        ListDfDict[int(files[files.index("_")+1:re.search(r'Hz', files).start()])] = df
    print("Data Frames Created")
    #print(ListDfDict[0]["#Time"]) dtype is float64 
    print(f'Dict status in Hz: {ListDfDict.keys()}')
    OrderedKeys = list(ListDfDict.keys()) 
        

#dfBase = pd.read_csv(filename1)
#dfSecond = pd.read_csv(filename2)
#dfThird = pd.read_csv(filename3)
#dfFourth = pd.read_csv(filename4)
#dfFifth = pd.read_csv(filename5)


    #fig, ax = plt.subplots(nrows = 2, ncols = len(csvs), figsize = (20,10))
    DictionaryHzToTimeRange = {}
    
    try:
        GlobalX = float(input("Please enter your True X position in meters (ex = 3.12): "))
        GlobalY = float(input("Please enter your True Y position in meters (ex = 3.12): "))
    except Exception as e:
        raise ValueError(f'Invalid Input: {e}') 
    if(len(str(GlobalX).split(".")[1]) > 2):
        GlobalX = round(GlobalX, 2)
    if(len(str(GlobalY).split(".")[1]) > 2):
        GlobalY = round(GlobalY, 2)
            
            
    print("\n")
    
     
    print("\n")
    print("You will now select time ranges for plots. By default graphs will keep their usual time record if you do not specify a range for a graph.\n A query loop will follow allowing you to edit different plots.")
    StringTimeRanges = {}
    for element in OrderedKeys:
        StringTimeRanges[element] = [ListDfDict[element]["#Time"].iloc[0], ListDfDict[element]["#Time"].iloc[-1]]
        print(f'{element} - Start: {StringTimeRanges[element][0]:.3f} & End: {StringTimeRanges[element][1]:.3f}')
            
    CommonStartTimeIndex = max(StringTimeRanges, key = lambda k: StringTimeRanges[k][0])
    CommonEndTimeIndex = min(StringTimeRanges, key = lambda k: StringTimeRanges[k][1])
    ValueStartTime = StringTimeRanges[CommonStartTimeIndex][0]
    ValueEndTime = StringTimeRanges[CommonEndTimeIndex][1]
    Gap = ValueEndTime - ValueStartTime
            
            
    print(f'Common Start Time: {ValueStartTime:.3f}, Common End Time: {ValueEndTime:.3f}, Difference Time Gap: {Gap:.3f}')
    while(True):
        GraphsInput = str(input("Please specify hz plots you would like to edit timeranges by Hz in the form example of '3,9,11,60,120'. \nOr, press empty enter for default. You will have the option to edit different plots at a time: "))
        if(GraphsInput.lower() == ""):
            break
        
            
        try:
            reObject = re.split(r'\s*,\s*', GraphsInput)
            reObject = [int(x) for x in reObject]
            for el in reObject:
                if el not in OrderedKeys:
                    raise ValueError(f'You entered a Hz input {el} that is not provided in the data you have.')
        except ValueError:
            raise
        except Exception:
            raise ValueError("Unable to parse the Hz inputs, please try again.")
       
        try:
            
            
            TimeNot = round(float(input("For these plots, please enter the beginning time you would like to plot for (ex = 30.290):")), 3)
            print(f'Entered initial time: {TimeNot}')
            TimeFinal = round(float(input("Please enter the final time you would like to plot for (ex = 30.290):")), 3)
            print(f'Entered final time: {TimeFinal}')
            if (TimeNot >= TimeFinal):
                raise ValueError(f'Bad bound selection of Not {TimeNot} and {TimeFinal} timenot selection must be strictly less than time final final.')
            print(f'Range of {str(TimeFinal - TimeNot)}')
            
            
            
            for elem in reObject:
                ListDfDict[elem]["Str(TIME)"] = ListDfDict[elem]["#Time"].map(lambda x: f'{x:.3f}')
                BeginningIndex = ListDfDict[elem]["#Time"].searchsorted(TimeNot, side = "left")
                LastIndex =  ListDfDict[elem]["#Time"].searchsorted(TimeFinal, side = "right") # one to the right, so if value is at index 554, 555 is the side = right cuz you want to use that value
                if (LastIndex > len(ListDfDict[elem]["#Time"]) or BeginningIndex >= len(ListDfDict[elem]["#Time"])):
                    raise ValueError(f'{TimeNot} or {TimeFinal} is out of the alloted time range. Pleast try again.')
                DictionaryHzToTimeRange[elem] = [BeginningIndex,LastIndex] # side = False means exact index, side = right means right the value.
                    
        except ValueError:
            raise 

    for element in OrderedKeys:
        if element not in DictionaryHzToTimeRange:
            DictionaryHzToTimeRange[element] = [0,len(ListDfDict[element]['#Time'])]
    
    
    OfficialNow = str(datetime.now().strftime("D%Y_%m_%d-T%H-%M-%S"))
    #str is redundant but whatever

        
    if(f'OutputReports' not in os.listdir()): 
        os.makedirs(f'OutputReports', mode=0o777, exist_ok=False)
        
    if(f'{OfficialNow}-{InputSelection}' not in os.listdir('OutputReports')): 
        os.makedirs(f'OutputReports/{OfficialNow}-{InputSelection}', mode=0o777, exist_ok=False)
        

    
    
       
    
    FullNumPages = math.floor(len(OrderedKeys)/2)
    RemainderGraphs = len(OrderedKeys) % 2
    #if int(FullNumPages) < 1:
        #raise ValueError("You don't have enough data to generate a solid report.")
    
    Counter = 0
    PageCounter = 1
    
    with pdf(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_Raw.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5), squeeze=False)
                for i in range(0, 2):
                    ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['X'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                    ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                    ax[0][i].set_xlabel('Time (s)')
                    ax[0][i].set_ylabel('X (m)')
                    ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([GlobalX, GlobalX]),color = 'red')
                        ## switch from x on first row to Y on bottom row
                    ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['Y'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                    ax[1][i].set_xlabel('Time (s)')
                    ax[1][i].set_ylabel('Y (m)')
                    ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([GlobalY, GlobalY]),color = 'red')
                        # Grid settings
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter += 2
                fig.suptitle(f'Page {PageCounter}')
                PageCounter += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5), squeeze = False)
            for i in range(int(RemainderGraphs)):
                ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['X'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                ax[0][i].set_xlabel('time (s)')
                ax[0][i].set_ylabel('X (m)')
                ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([GlobalX, GlobalX]),color = 'red')
                        ## switch from x on first row to Y on bottom row
                ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['Y'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                ax[1][i].set_xlabel('time (s)')
                ax[1][i].set_ylabel('Y (m)')
                ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([GlobalY, GlobalY]),color = 'red')
                
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter += RemainderGraphs
            fig.suptitle(f'Page {PageCounter}')
            PageCounter += 1
            file.savefig(fig)
            plt.close(fig)
                
                
      
    print(f'Succesful pdf Write of {PageCounter-1} pages and {Counter} graphs.')
    
    
    
    
    
    
    ##Error graphs next
    
    # Need to make properedicts to each Dataframe to provide what's necessary
    Counter1 = 0 
    PageCounter1 = 1
    
    RMSE = {} # Accuracy measurement
    
    ME = {} # Bias measurement
    
    MAE = {}
    
    MaxRE = {}
    
    FinalRE = {}
    
    InitialRE = {}
    
    MEAdjustedAve = {}
    
    MEAdjRMSE = {}
    MEAdjMAE = {}
    MEAdjMaxRE = {}
    #Following are not deemed relavent statistics as lots of oscillation won't allow for a valid comparisonsince we go up and down.
    #MEAdjInitialRE = {}
    #MEAdjFinalRE = {}
    
    #Consider a minumum statistic?
    
    
    ### Error calculations
    for element in OrderedKeys:
        ListDfDict[element]['X Resid.'] = (ListDfDict[element]['X'] - GlobalX).round(2)
        ListDfDict[element]['Y Resid.'] = (ListDfDict[element]['Y'] - GlobalY).round(2)
        
        
        
        
        
        
        ListDfDict[element]['X Resid. abs'] = (ListDfDict[element]['X Resid.'].abs()).round(2)
        ListDfDict[element]['Y Resid. abs'] = (ListDfDict[element]['Y Resid.'].abs()).round(2)
        
        #Max euclidean error report in index 2 of Max RE
        #Structure, X,Y, Max Euclidean
        XAbsMaxErrorIndex = ListDfDict[element]['X Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        YAbsMaxErrorIndex = ListDfDict[element]['Y Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        #XAbsMaxErrorValue = ListDfDict[element]['X Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].max()
        #YAbsMaxErrorValue = ListDfDict[element]['Y Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].max()
        
        
        ListDfDict[element]['X Resid. abs sq'] = np.power(ListDfDict[element]['X Resid. abs'],2).round(7)
        ListDfDict[element]['Y Resid. abs sq'] = np.power(ListDfDict[element]['Y Resid. abs'],2).round(7)
        
        
        #ME section at this point
        
        
        
        if (len(ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]) != len(ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])):
            raise ValueError("You're lengths for X and Y do not match which means errors for calculations. Please Retry.")
        
        XME = round((ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        YME = round((ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        
        
        
        
        
        
        
        ##MAE section
        
        XMAE = round((ListDfDict[element]['X Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['X Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        YMAE = round((ListDfDict[element]['Y Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['X Resid. abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        
        
        
        ListDfDict[element]['X Resid. sq'] = np.power(ListDfDict[element]['X Resid.'], 2)
        ListDfDict[element]['Y Resid. sq'] = np.power(ListDfDict[element]['Y Resid.'], 2)
        
        ListDfDict[element]['TotalEuclideanDistanceError'] = (np.sqrt(ListDfDict[element]['X Resid. sq'] + ListDfDict[element]['Y Resid. sq'])).round(3)
        
        IndexMaxEuclideanDistanceError = ListDfDict[element]['TotalEuclideanDistanceError'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        # follows X indivudually, Y indivisdually, and then given info about total euclidean error max wise, all within the correct time period
        MaxRE[element] = [[XAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[XAbsMaxErrorIndex] ,ListDfDict[element]['X Resid.'].iloc[XAbsMaxErrorIndex]],[YAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[YAbsMaxErrorIndex],ListDfDict[element]['Y Resid.'].iloc[YAbsMaxErrorIndex]],[IndexMaxEuclideanDistanceError, ListDfDict[element]['TotalEuclideanDistanceError'].iloc[IndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid.'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid.'].iloc[IndexMaxEuclideanDistanceError]]]
        
        MAGME = round(np.sqrt(np.power(XME,2) + np.power(YME,2)),3)
    
        
        
    
        SumResidSqXTimeRAware = ListDfDict[element]['X Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum()
        SumResidSqYTimeRAware = ListDfDict[element]['Y Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum()
        
        TotalSumResidSq = SumResidSqXTimeRAware + SumResidSqYTimeRAware
        TotalSumResidSqAve = TotalSumResidSq / int(len(ListDfDict[element]['X Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        
        
        SumResidSqXAverage = SumResidSqXTimeRAware / int(len(ListDfDict[element]['X Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        SumResidSqYAverage = SumResidSqYTimeRAware / int(len(ListDfDict[element]['Y Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        
        RMSEX = round(np.sqrt(SumResidSqXAverage), 3)
        RMSEY = round(np.sqrt(SumResidSqYAverage), 3)
        
        TwoDRMSE = round(np.sqrt(TotalSumResidSqAve), 3)
        
        #TDMAE will rely on euclidean distance error
        TDMAE = round((np.sqrt(ListDfDict[element]['X Resid. abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]] + ListDfDict[element]['Y Resid. abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]).sum())/int(len(ListDfDict[element]['Y Resid. abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        
        FinalRE_Euclidean = round(np.sqrt(ListDfDict[element]['X Resid. sq'].iloc[DictionaryHzToTimeRange[element][1] - 1] + ListDfDict[element]['Y Resid. sq'].iloc[DictionaryHzToTimeRange[element][1] - 1]),3)
        #standard euclidean distance error
        FinalRE[element] = [DictionaryHzToTimeRange[element][1] - 1, ListDfDict[element]['#Time'].iloc[DictionaryHzToTimeRange[element][1] - 1], ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][1] - 1], ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][1] - 1], FinalRE_Euclidean]
        
        InitialRE_Euclidean = round(np.sqrt(ListDfDict[element]['X Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]] + ListDfDict[element]['Y Resid. sq'].iloc[DictionaryHzToTimeRange[element][0]]),3)
        #standard euclidean distance error
        InitialRE[element] = [DictionaryHzToTimeRange[element][0], ListDfDict[element]['#Time'].iloc[DictionaryHzToTimeRange[element][0]], ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]], ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]],InitialRE_Euclidean]
        
        RMSE[element] = [RMSEX, RMSEY, TwoDRMSE] #RMSE assumes Gaussian noise, penalize outliers more heavily
        ME[element] = [XME, YME, MAGME]
        MAE[element] = [XMAE, YMAE, TDMAE]
        
        # organized by x, y
        ############# INSERT SECTION FOR UPDATE BASED OFF OF ME. 
        MEAdjustedAve[element] = [round(GlobalX + ME[element][0],3), round(GlobalY + ME[element][1],3)]
        
        ListDfDict[element]['X Resid. MEAdjusted'] = (ListDfDict[element]['X'] - MEAdjustedAve[element][0]).round(2)
        ListDfDict[element]['Y Resid. MEAdjusted'] = (ListDfDict[element]['Y'] - MEAdjustedAve[element][1]).round(2)
        
        ListDfDict[element]['X Resid. MEAdj abs'] = (ListDfDict[element]['X Resid. MEAdjusted'].abs()).round(2)
        ListDfDict[element]['Y Resid. MEAdj abs'] = (ListDfDict[element]['Y Resid. MEAdjusted'].abs()).round(2)
        
        
        
        
        
        ## ROund two of adjusted report essentially, ME ADJ
        
        ListDfDict[element]['X Resid. MEAdj abs sq'] = np.power(ListDfDict[element]['X Resid. MEAdj abs'],2).round(7)
        ListDfDict[element]['Y Resid. MEAdj abs sq'] = np.power(ListDfDict[element]['Y Resid. MEAdj abs'],2).round(7)
        
        MEADJXMAE = round((ListDfDict[element]['X Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['X Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        MEADJYMAE = round((ListDfDict[element]['Y Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum())/int(len(ListDfDict[element]['Y Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        
        MEADJMAEMAG = round((np.sqrt(ListDfDict[element]['X Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]] + ListDfDict[element]['Y Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]).sum())/int(len(ListDfDict[element]['Y Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        MEAdjMAE[element] = [MEADJXMAE, MEADJYMAE, MEADJMAEMAG]
        
        
        ### Start of RMSE Portion
        MEADJSumResidSqXTimeRAware = ListDfDict[element]['X Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum()
        MEADJSumResidSqYTimeRAware = ListDfDict[element]['Y Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].sum()
        
        MEADJSumResidSqXAverage = MEADJSumResidSqXTimeRAware / int(len(ListDfDict[element]['X Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        MEADJSumResidSqYAverage = MEADJSumResidSqYTimeRAware / int(len(ListDfDict[element]['Y Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        
        
        
        MEADJRMSEX = round(np.sqrt(MEADJSumResidSqXAverage), 3)
        MEADJRMSEY = round(np.sqrt(MEADJSumResidSqYAverage), 3)
        
        MEADJTotalSumResidSq = MEADJSumResidSqXTimeRAware + MEADJSumResidSqYTimeRAware
        MEADJTotalSumResidSqAve = MEADJTotalSumResidSq / int(len(ListDfDict[element]['X Resid. MEAdj abs sq'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]]))
        
        MEADJTwoDRMSE = round(np.sqrt(MEADJTotalSumResidSqAve), 3)
        
        MEAdjRMSE[element] = [MEADJRMSEX, MEADJRMSEY, MEADJTwoDRMSE]
        
        ###
        
        ListDfDict[element]['MEADJTotalEuclideanDistanceError'] = (np.sqrt(ListDfDict[element]['X Resid. MEAdj abs sq'] + ListDfDict[element]['Y Resid. MEAdj abs sq'])).round(3)   
        MEAdjIndexMaxEuclideanDistanceError = ListDfDict[element]['MEADJTotalEuclideanDistanceError'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        
        MEAdjXAbsMaxErrorIndex = ListDfDict[element]['X Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        MEAdjYAbsMaxErrorIndex = ListDfDict[element]['Y Resid. MEAdj abs'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].idxmax()
        # follows X indivudually, Y indivisdually, and then given info about total euclidean error max wise, all within the correct time period
        MEAdjMaxRE[element] = [[MEAdjXAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[MEAdjXAbsMaxErrorIndex] ,ListDfDict[element]['X Resid. MEAdjusted'].iloc[MEAdjXAbsMaxErrorIndex]],[MEAdjYAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[MEAdjYAbsMaxErrorIndex],ListDfDict[element]['Y Resid. MEAdjusted'].iloc[MEAdjYAbsMaxErrorIndex]],[MEAdjIndexMaxEuclideanDistanceError, ListDfDict[element]['MEADJTotalEuclideanDistanceError'].iloc[MEAdjIndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[MEAdjIndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid. MEAdjusted'].iloc[MEAdjIndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid. MEAdjusted'].iloc[MEAdjIndexMaxEuclideanDistanceError]]]
        
        
        
        
        
        
        
          
    Counter = 0
    PageCounter = 1
    
    with pdf(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_MEADJRaw.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5), squeeze=False)
                for i in range(0, 2):
                    ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['X'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                    ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                    ax[0][i].set_xlabel('Time (s)')
                    ax[0][i].set_ylabel('X (m)')
                    ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([MEAdjustedAve[OrderedKeys[Counter+i]][0], MEAdjustedAve[OrderedKeys[Counter+i]][0]]),color = 'red')
                        ## switch from x on first row to Y on bottom row
                    ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['Y'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                    ax[1][i].set_xlabel('Time (s)')
                    ax[1][i].set_ylabel('Y (m)')
                    ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([MEAdjustedAve[OrderedKeys[Counter+i]][1], MEAdjustedAve[OrderedKeys[Counter+i]][1]]),color = 'red')
                        # Grid settings
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter += 2
                fig.suptitle(f'Page {PageCounter}')
                PageCounter += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5), squeeze = False)
            for i in range(int(RemainderGraphs)):
                ax[0][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['X'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                ax[0][i].set_title(f'{OrderedKeys[Counter + i]} Hz')
                ax[0][i].set_xlabel('time (s)')
                ax[0][i].set_ylabel('X (m)')
                ax[0][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([MEAdjustedAve[element][0], MEAdjustedAve[element][0]]),color = 'red')
                        ## switch from x on first row to Y on bottom row
                ax[1][i].plot(ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]],ListDfDict[OrderedKeys[Counter + i]]['Y'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]], color = 'blue')
                ax[1][i].set_xlabel('time (s)')
                ax[1][i].set_ylabel('Y (m)')
                ax[1][i].plot(np.array([ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter + i]][0]],ListDfDict[OrderedKeys[Counter + i]]['#Time'].iloc[(DictionaryHzToTimeRange[OrderedKeys[Counter + i]][1]-1)]]),np.array([MEAdjustedAve[element][1], MEAdjustedAve[element][1]]),color = 'red')
                
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter += RemainderGraphs
            fig.suptitle(f'Page {PageCounter}')
            PageCounter += 1
            file.savefig(fig)
            plt.close(fig)  
        
    print("Raw ME adj plots succesfully constructed as MEADJRaw.pdf")
        
        
        
    
        
        
        
    
    with pdf(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_Error.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5), squeeze = False)
                for i in range(0, 2):
                    ax[0][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['X Resid.'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                    ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                    ax[0][i].set_xlabel('Time (s)')
                    ax[0][i].set_ylabel('X Resid. (m)')
                    
                        ## switch from x on first row to Y on bottom row
                    ax[1][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['Y Resid.'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                    ax[1][i].set_xlabel('Time (s)')
                    ax[1][i].set_ylabel('Y Resid. (m)')
                
                        # Grid settings
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter1 += 2
                fig.suptitle(f'Page {PageCounter1}')
                PageCounter1 += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5), squeeze=False)
            for i in range(int(RemainderGraphs)):
                ax[0][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['X Resid.'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                ax[0][i].set_xlabel('Time (s)')
                ax[0][i].set_ylabel('X Resid. (m)')
                        ## switch from x on first row to Y on bottom row
                ax[1][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['Y Resid.'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                ax[1][i].set_xlabel('Time (s)')
                ax[1][i].set_ylabel('Y Resid. (m)')
                
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter1 += RemainderGraphs
            fig.suptitle(f'Page {PageCounter1}')
            PageCounter1 += 1
            file.savefig(fig)
            plt.close(fig)
            
    
    Counter1 = 0
    PageCounter = 1
    #ME adjusted error plots
    
    
    with pdf(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_MEADJError.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5), squeeze = False)
                for i in range(0, 2):
                    ax[0][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['X Resid. MEAdjusted'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                    ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                    ax[0][i].set_xlabel('Time (s)')
                    ax[0][i].set_ylabel('X Resid. MEADJ (m)')
                    
                        ## switch from x on first row to Y on bottom row
                    ax[1][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['Y Resid. MEAdjusted'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                    ax[1][i].set_xlabel('Time (s)')
                    ax[1][i].set_ylabel('Y Resid. MEADJH (m)')
                
                        # Grid settings
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter1 += 2
                fig.suptitle(f'Page {PageCounter1}')
                PageCounter1 += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5), squeeze=False)
            for i in range(int(RemainderGraphs)):
                ax[0][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['X Resid. MEAdjusted'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                ax[0][i].set_xlabel('Time (s)')
                ax[0][i].set_ylabel('X Resid. MEADJ (m)')
                        ## switch from x on first row to Y on bottom row
                ax[1][i].plot(ListDfDict[OrderedKeys[Counter1 + i]]['#Time'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]],ListDfDict[OrderedKeys[Counter1 + i]]['Y Resid. MEAdjusted'].iloc[DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][0]:DictionaryHzToTimeRange[OrderedKeys[Counter1 + i]][1]], color = 'blue')
                ax[1][i].set_xlabel('Time (s)')
                ax[1][i].set_ylabel('Y Resid. ME ADJ (m)')
                
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter1 += RemainderGraphs
            fig.suptitle(f'Page {PageCounter1}')
            PageCounter1 += 1
            file.savefig(fig)
            plt.close(fig)
            
    print("Succusfully constructed ME ADJUSTED base line graphs as MEADJERROR.pdf")

    
    with open(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_Raw.info', 'w') as file:
        file.write(f'Chosen true X position in meters: {GlobalX}\n')
        file.write(f'Chosen true Y position in meters: {GlobalY}\n')
        file.write(f'files analyzed {" ".join(csvs)}\n')
        file.write(f'Frequencies in impact Hz: {" ".join([str(strings) for strings in OrderedKeys])}\n')
        file.write(f'{Counter} graphs and {PageCounter - 1} pages succesfully written')
    
    print(f'Raw Info file succesfully written')
    
    ###### Hitting error report
    
    ##RMSE calculations
    
    
    
    with open(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_Error.info', 'w') as file:
        file.write(f'Chosen true X position in meters: {GlobalX}\n')
        file.write(f'Chosen true Y position in meters: {GlobalY}\n')
        file.write(f'files analyzed {" ".join(csvs)}\n')
        file.write(f'Frequencies in impact Hz: {" ".join([str(strings) for strings in OrderedKeys])}\n')
        file.write(f'{Counter1} graphs and {PageCounter1 - 1} pages succesfully written\n')
        # at this point we want to start to add some reports file.write()
        
        #RMSE[element] = [RMSEX, RMSEY, TwoDRMSE] #RMSE assumes Gaussian noise, penalize outliers more heavily
        #ME[element] = [XME, YME, TDME]
        #MAE[element] = [XMAE, YMAE, TDMAE]
        file.write("Calculations are written with time bounds selected by users.\n\n")
        
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        
        file.write("RMSE Report by Hz:\n") # Outlier detection
        for element in OrderedKeys:
            file.write(f'{element} Hz: X component - {RMSE[element][0]}, Y component - {RMSE[element][1]}, 2D RMSE - {RMSE[element][2]} \n')
            file.write("\n")
        
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        file.write("ME bias report by Hz:\n") # bias detection
        for element in OrderedKeys:
            file.write(f'{element} Hz: X component - {ME[element][0]}, Y component - {ME[element][1]}, Total 2D ME Bias (Magnitude func.) - {ME[element][2]} \n')
            file.write("\n")
            
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        file.write("MAE report by Hz:\n") #euclidean distance error
        for element in OrderedKeys:
            file.write(f'{element} Hz: X component - {MAE[element][0]}, Y component - {MAE[element][1]}, Total 2D MAE Error (averaged sum of euclidean distance error) - {MAE[element][2]} \n')
            file.write("\n")
            
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write("Max Residual Error report by Hz in user specified time range:\n")
        
        #MaxRE[element] = [[XAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[XAbsMaxErrorIndex] ,ListDfDict[element]['X Resid.'].iloc[XAbsMaxErrorIndex]],[YAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[YAbsMaxErrorIndex],ListDfDict[element]['Y Resid.'].iloc[YAbsMaxErrorIndex]],[IndexMaxEuclideanDistanceError, ListDfDict[element]['TotalEuclideanDistanceError'].iloc[IndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid.'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid.'].iloc[IndexMaxEuclideanDistanceError]]]
        for element in OrderedKeys:
            file.write(f'{element} Hz: Max X error component --> Access Index - {MaxRE[element][0][0]}, X Time log - {MaxRE[element][0][1]}, Resid. Value - {MaxRE[element][0][2]} | Max Y error component --> Access Index - {MaxRE[element][1][0]}, Y Time log - {MaxRE[element][1][1]}, Resid. Value - {MaxRE[element][1][2]}|\n')
            file.write(f'{element} Hz Continued: Max Euclidean error --> Access Index - {MaxRE[element][2][0]}, Time log - {MaxRE[element][2][2]}, Max Euclidean error - {MaxRE[element][2][1]}, X comp - {MaxRE[element][2][3]}, Y comp - {MaxRE[element][2][4]}\n')
            file.write("\n")
        #[IndexMaxEuclideanDistanceError, ListDfDict[element]['TotalEuclideanDistanceError'].iloc[IndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid.'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid.'].iloc[IndexMaxEuclideanDistanceError]
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write("Initial Point Error report by Hz:\n")
        #InitialRE[element] = [DictionaryHzToTimeRange[element][0], ListDfDict[element]['#Time'].iloc[DictionaryHzToTimeRange[element][0]], ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]], ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]],InitialRE_Euclidean]
        for element in OrderedKeys:
            file.write(f'{element} Hz: Access Index - {InitialRE[element][0]}, Time log - {InitialRE[element][1]}, X Resid. Value - {InitialRE[element][2]}, Y Resid. Value - {InitialRE[element][3]}, 2D initial recorded Euclidean distance error - {InitialRE[element][4]}\n')
            file.write("\n")
        # FinalRE[element] = [DictionaryHzToTimeRange[element][1] - 1, ListDfDict[element]['#Time'].iloc[DictionaryHzToTimeRange[element][1] - 1], ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][1] - 1], ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][1] - 1], FinalRE_Euclidean]
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write(f'Final Point Error report by Hz:\n')
        for element in OrderedKeys:
            file.write(f'{element} Hz: Access Index - {FinalRE[element][0]}, Time Log - {FinalRE[element][1]}, X component residual - {FinalRE[element][2]}, Y component residual - {FinalRE[element][3]}, 2D final recorded euclidean error - {FinalRE[element][4]}\n')
            file.write("\n")
            
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        
        file.write("End of Report")
        
    print(f'Error Info file succesfully written')
        
        #Error ME ADJUSTED
    with open(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_ErrorMEADJ.info', 'w') as file:
        file.write("NOTE! THIS REPORT IS WITH NUMBERS FOR AN ADJUSTED ME AVERAGE\n")
        file.write(f'Chosen true X position in meters: {GlobalX}\n')
        file.write(f'Chosen true Y position in meters: {GlobalY}\n')
        file.write(f'files analyzed {" ".join(csvs)}\n')
        file.write(f'Frequencies in impact Hz: {" ".join([str(strings) for strings in OrderedKeys])}\n')
        file.write(f'{Counter1} graphs and {PageCounter1 - 1} pages succesfully written\n')
        # at this point we want to start to add some reports file.write()
        
        #RMSE[element] = [RMSEX, RMSEY, TwoDRMSE] #RMSE assumes Gaussian noise, penalize outliers more heavily
        #ME[element] = [XME, YME, TDME]
        #MAE[element] = [XMAE, YMAE, TDMAE]
        file.write("Calculations are written with time bounds selected by users.\n\n")
        
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        file.write("ME Influenced Change report: \n")
        for element in OrderedKeys:
            file.write(f'{element} Hz: \n')
            file.write(f'X ME adjustment factor: {ME[element][0]} \n')
            file.write(f'Newly established X Baseline: {MEAdjustedAve[element][0]} \n')
            file.write(f'Y ME adjustment factor: {ME[element][1]} \n')
            file.write(f'Newly established Y Baseline: {MEAdjustedAve[element][1]} \n')
        
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        file.write("ME ADJ RMSE Report by Hz:\n") # Outlier detection
        for element in OrderedKeys:
            
            file.write(f'{element} Hz: X component - {MEAdjRMSE[element][0]}, Y component - {MEAdjRMSE[element][1]}, 2D RMSE - {MEAdjRMSE[element][2]} \n')
            file.write("\n")
        
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        file.write("MAE report by Hz:\n") #euclidean distance error
        for element in OrderedKeys:
            file.write(f'{element} Hz: X component - {MEAdjMAE[element][0]}, Y component - {MEAdjMAE[element][1]}, Total 2D MAE Error (averaged sum of euclidean distance error) - {MEAdjMAE[element][2]} \n')
            file.write("\n")
            
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        file.write("Max Residual Error report by Hz in user specified time range:\n")
        
        #MaxRE[element] = [[XAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[XAbsMaxErrorIndex] ,ListDfDict[element]['X Resid.'].iloc[XAbsMaxErrorIndex]],[YAbsMaxErrorIndex,  ListDfDict[element]['#Time'].iloc[YAbsMaxErrorIndex],ListDfDict[element]['Y Resid.'].iloc[YAbsMaxErrorIndex]],[IndexMaxEuclideanDistanceError, ListDfDict[element]['TotalEuclideanDistanceError'].iloc[IndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid.'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid.'].iloc[IndexMaxEuclideanDistanceError]]]
        for element in OrderedKeys:
            file.write(f'{element} Hz: Max X error component --> Access Index - {MEAdjMaxRE[element][0][0]}, X Time log - {MEAdjMaxRE[element][0][1]}, Resid. Value - {MEAdjMaxRE[element][0][2]} | Max Y error component --> Access Index - {MEAdjMaxRE[element][1][0]}, Y Time log - {MEAdjMaxRE[element][1][1]}, Resid. Value - {MEAdjMaxRE[element][1][2]}|\n')
            file.write(f'{element} Hz Continued: Max Euclidean error --> Access Index - {MEAdjMaxRE[element][2][0]}, Time log - {MEAdjMaxRE[element][2][2]}, Max Euclidean error - {MEAdjMaxRE[element][2][1]}, X comp - {MEAdjMaxRE[element][2][3]}, Y comp - {MEAdjMaxRE[element][2][4]}\n')
            file.write("\n")
        #[IndexMaxEuclideanDistanceError, ListDfDict[element]['TotalEuclideanDistanceError'].iloc[IndexMaxEuclideanDistanceError],ListDfDict[element]['#Time'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['X Resid.'].iloc[IndexMaxEuclideanDistanceError], ListDfDict[element]['Y Resid.'].iloc[IndexMaxEuclideanDistanceError]
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        
        file.write("End of Report")
        
        
    print("ME ADJUSTED Error file succesfully written!")
        
    
    
        
        
    PageCounter1 = 1
    Counter1 = 0
    
    
   
    #value_counts() and sort_index() mechanism for each Hz
    IndexCountsX = {}
    IndexCountsY = {}
    for element in OrderedKeys:
        IndexCountsX[element] = ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].value_counts().sort_index().astype(float)
        IndexCountsY[element] = ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]].value_counts().sort_index().astype(float)
        IterationCopyX = IndexCountsX[element].copy()
        IterationCopyY = IndexCountsY[element].copy()
        for index in IndexCountsX[element].index:
            IterationCopyX[index] = round(IndexCountsX[element][index]/(len(ListDfDict[element]['X Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        for index in IndexCountsY[element].index:
            IterationCopyY[index] = round(IndexCountsY[element][index]/(len(ListDfDict[element]['Y Resid.'].iloc[DictionaryHzToTimeRange[element][0]:DictionaryHzToTimeRange[element][1]])),3)
        IndexCountsX[element] = IterationCopyX
        IndexCountsY[element] = IterationCopyY
        
            
        
       
        
    
    with pdf(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_PercentileError.pdf') as file:
        plt.rcParams["figure.figsize"] = (11, 8.5)
        
        if(int(FullNumPages) > 0):
            for pagenum in range(0,int(FullNumPages)):
                fig, ax = plt.subplots(nrows = 2, ncols = 2, figsize = (11,8.5),squeeze=False)
                for i in range(0, 2):
                    bars = ax[0][i].bar(IndexCountsX[OrderedKeys[Counter1 + i]].index, IndexCountsX[OrderedKeys[Counter1 + i]].values, color = 'steelblue', edgecolor = 'red', lw = 0.4, width = 0.01)
                    ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                    ax[0][i].set_xlabel(f'X Residual Values')
                    ax[0][i].set_ylabel('X Freq. Props.')
                    ax[0][i].set_xticks(IndexCountsX[OrderedKeys[Counter1 + i]].index)
                    ax[0][i].set_xticklabels([f'{b:.2f}' for b in IndexCountsX[OrderedKeys[Counter1 + i]].index], rotation=45, fontsize=7)
                    
                    
                        ## switch from x on first row to Y on bottom row
                    bars = ax[1][i].bar(IndexCountsY[OrderedKeys[Counter1 + i]].index, IndexCountsY[OrderedKeys[Counter1 + i]].values, color = 'steelblue', edgecolor = 'red', lw = 0.4, width = 0.01)
                    ax[1][i].set_xlabel(f'Y Residual Values')
                    ax[1][i].set_ylabel('Y Freq. Props.')
                    ax[1][i].set_xticks(IndexCountsY[OrderedKeys[Counter1 + i]].index)
                    ax[1][i].set_xticklabels([f'{b:.2f}' for b in IndexCountsY[OrderedKeys[Counter1 + i]].index], rotation=45, fontsize=7)

                
                        # Grid settings
                    ax[1][i].grid(True, alpha = 0.3)
                    ax[0][i].grid(True, alpha = 0.3)
                Counter1 += 2
                fig.suptitle(f'Page {PageCounter1}')
                PageCounter1 += 1
                file.savefig(fig)
                plt.close(fig)
        if(int(RemainderGraphs) > 0):
            fig, ax = plt.subplots(nrows = 2, ncols = int(RemainderGraphs), figsize = (11,8.5),squeeze=False)
            for i in range(int(RemainderGraphs)):
                bars = ax[0][i].bar(IndexCountsX[OrderedKeys[Counter1 + i]].index, IndexCountsX[OrderedKeys[Counter1 + i]].values, color = 'steelblue', edgecolor = 'red', lw = 0.4, width = 0.01)
                ax[0][i].set_title(f'{OrderedKeys[Counter1 + i]} Hz')
                ax[0][i].set_xlabel(f'X Residual Values')
                ax[0][i].set_ylabel('X Freq. Props.')
                ax[0][i].set_xticks(IndexCountsX[OrderedKeys[Counter1 + i]].index)
                ax[0][i].set_xticklabels([f'{b:.2f}' for b in IndexCountsX[OrderedKeys[Counter1 + i]].index], rotation=45, fontsize=7)
                
                    
                        ## switch from x on first row to Y on bottom row
                bars = ax[1][i].bar(IndexCountsY[OrderedKeys[Counter1 + i]].index, IndexCountsY[OrderedKeys[Counter1 + i]].values, color = 'steelblue', edgecolor = 'red', lw = 0.4, width = 0.01)
                ax[1][i].set_xlabel(f'Y Residual Values')
                ax[1][i].set_ylabel('Y Freq. Props.')
                ax[1][i].set_xticks(IndexCountsY[OrderedKeys[Counter1 + i]].index)
                ax[1][i].set_xticklabels([f'{b:.2f}' for b in IndexCountsY[OrderedKeys[Counter1 + i]].index], rotation=45, fontsize=7)
                
                        # Grid settings
                ax[1][i].grid(True, alpha = 0.3)
                ax[0][i].grid(True, alpha = 0.3)
            Counter1 += RemainderGraphs
            fig.suptitle(f'Page {PageCounter1}')
            PageCounter1 += 1
            file.savefig(fig)
            plt.close(fig)
        print(f'Percentile Bins error file succesfully written')
            
  
    with open(f'OutputReports/{OfficialNow}-{InputSelection}/{OfficialNow}-{InputSelection}_PercentileError.info', 'w') as file:
        file.write(f'Chosen true X position in meters: {GlobalX}\n')
        file.write(f'Chosen true Y position in meters: {GlobalY}\n')
        file.write(f'files analyzed {" ".join(csvs)}\n')
        file.write(f'Frequencies in impact Hz: {" ".join([str(strings) for strings in OrderedKeys])}\n')
        file.write(f'{Counter1} graphs and {PageCounter1 - 1} pages succesfully written')
        file.write(f'\n\n Basic % Frequency Report, please reference _Error file for proper error measurements.\n\n')
        file.write("----------------------------------------------------------------\n")
        file.write(f'Binned Error Proportion values by Hz:\n')
        for element in OrderedKeys:
            file.write("----------------------------------------------------------------\n")
            file.write(f'{element} Hz --> \n')
            file.write(f'X Residual % Proportions:\n')
            for i in IndexCountsX[element].index:
                file.write(f'{i:.2f} --- {((IndexCountsX[element][i])*100):.1f}%\n')
            file.write("---------\n")
            file.write(f'Y Residual % Proportions:\n')
            for i in IndexCountsY[element].index:
                file.write(f'{i:.2f} --- {((IndexCountsY[element][i])*100):.1f}%\n')
        file.write("\n")
        file.write("----------------------------------------------------------------")
        file.write("\n")
        
        
        file.write("End of Report")
        
        
        
    print('Percentile Error report succesfully written')
    
    
    
    

    ## to parquet for future processing in a csv file:
    
    if 'GenerateReportParquetsTimeSensitive' not in os.listdir():
        os.makedirs(f'GenerateReportParquetsTimeSensitive', mode = 0o777, exist_ok = False)
    
    if f'GenerateReportParquetsTimeSensitive/{InputSelection}' not in os.listdir():
        os.makedirs(f'GenerateReportParquetsTimeSensitive/{InputSelection}', mode = 0o777, exist_ok = False)
        
    for element in OrderedKeys:
        ListDfDict[element].to_parquet(f'GenerateReportParquetsTimeSensitive/{InputSelection}/Test_{element}Hz.parquet', index = False)
        
        
    
    print('Parquet data succesfully written under GenerateReportParquetsTimeSensitive.')
    
        
    
    
    
        
    
    
    
    
    
    
    
    
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
        

        
        
        
    
__main__()