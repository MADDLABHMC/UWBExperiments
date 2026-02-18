import os
import re 

filenameR = "LogTest16.txt"

filenameW = "LogTest16Translated.csv"


# What should Pure csv's look like: time, x, y ,z, confidence

Time=[]
x=[]
y=[]
z=[]
conf = []

Line1 = ""
line2 = ""

FirstComma = SecondComma = ThirdComma = FourthComma = False
Counter = 0

def __main__():
    global StatusBegin
    global FirstComma, SecondComma, ThirdComma, FourthComma
    with open(filenameR, 'r') as file:
        while(True):
            Line1 = file.readline();
            if Line1 == "":
                break
            if"loc_data" in Line1:
                    
                for j in range(len(Line1)): 
                    if Line1[j] == "[":
                        index1 = j
                    if Line1[j] == "]":
                        index2 = j-4
                        break
                
                Time.append(Line1[index1 + 1:index2])
                    
                Line2 = file.readline()
                    
                
                for i in range(len(Line2)):
                    if Line2[i] == "[":
                        FDigitID = i
                    elif Line2[i] == "," and FirstComma == False:
                        SDigitID = i
                        FirstComma = True
                    elif Line2[i] == "," and SecondComma == False:
                        TDigitID = i 
                        SecondComma = True
                    elif Line2[i] == "," and ThirdComma == False:
                        FoDigitID = i
                        ThirdComma = True
                    elif Line2[i] == "," and FourthComma == False:
                        FiDigitID = i
                        FourthComma = True         
                    elif Line2[i] == "]":
                        break
                    
                x.append(Line2[FDigitID + 1:SDigitID])
                y.append(Line2[SDigitID + 1:TDigitID])  
                z.append(Line2[TDigitID + 1:FoDigitID])
                conf.append(Line2[FoDigitID + 1:FiDigitID])
                
                FirstComma = SecondComma = ThirdComma = FourthComma = False
               
                        

    
    with open(filenameW, 'w') as file:
        file.write("#Time,X,Y,Z,CONF\n") 
        for h in range(len(Time)):
            StringPrint = f"{Time[h]},{x[h]},{y[h]},{z[h]},{conf[h]}\n"
            file.write(StringPrint);
        





__main__()