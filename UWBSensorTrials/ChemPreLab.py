import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def __main__():
    ZeroOrderA = np.array([1.00,0.88,0.75,0.63,0.50,0.38])
    FirstOrderA = np.array([1.00,0.55,0.30,0.17,0.09,0.05])
    SecondOrderA = np.array([1.00,0.33,0.20,0.14,0.11,0.09])    
    Time = np.array([0,1,2,3,4,5])
    
    DFZero = pd.DataFrame({"Time": Time, "[A]": ZeroOrderA})
    DFFirst = pd.DataFrame({"Time": Time, "[A]": FirstOrderA})
    DFSecond = pd.DataFrame({"Time": Time, "[A]": SecondOrderA})
    
    ListDFs = [DFZero, DFFirst, DFSecond]
    
    for DF in ListDFs:
        DF['ln[A]'] = np.log(DF['[A]'])
        DF['1/[A]'] = 1/(DF['[A]'])
        
    fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = (17, 8))
    fig.suptitle("Second Order Reaction")
    
    ax[0].plot(ListDFs[2]["Time"], ListDFs[2]['[A]'])
    ax[0].set_title("[A] vs Time")
    ax[0].set_xlabel("Time (hr)")
    ax[0].set_ylabel("[A] (M)")
    
    ax[1].plot(ListDFs[2]["Time"], ListDFs[2]['ln[A]'])
    ax[1].set_title("ln[A] vs Time")
    ax[1].set_xlabel("Time (hr)")
    ax[1].set_ylabel("ln[A] (Unitless)")
    
    ax[2].plot(ListDFs[2]["Time"], ListDFs[2]['1/[A]'])
    ax[2].set_title("1/[A] vs Time")
    ax[2].set_xlabel("Time (hr)")
    ax[2].set_ylabel("1/[A] (M^-1)")
    
    plt.show()


    
    
__main__()