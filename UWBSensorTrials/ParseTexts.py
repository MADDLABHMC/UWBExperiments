import os
import re 

#filenameR = "Mar7/BaselineMar7Update2.txt"

#filenameW = "Mar7/BaselineTransMar7Update2.csv"




# What should Pure csv's look like: time, x, y ,z, confidence


Time=[]
x=[]
y=[]
z=[]
conf = []

Line1 = ""
line2 = ""

FirstComma = SecondComma = ThirdComma = FourthComma = False

def __main__():
    global FirstComma, SecondComma, ThirdComma, FourthComma
    global Line1, line2
    global Time,x,y,z,conf
    
    FOLDERINPUT = input("Make sure there is a folder with a Note txt file and all your txt outputs. \n The program will automatically take away any extra folders and note files as long as 'Note' is in the file name. \n Input exact folder for processing of text files: ")
    file_names = os.listdir(FOLDERINPUT)
    # at this point we need to parse for "Note"
    if(f'{FOLDERINPUT}_Translated_To_CSV' in file_names):
        raise Exception("You already have a Translated Folder, please figure out the situation.")
    file_names = [x for x in file_names if (".txt" in x.lower()) and ("note" not in x.lower())]
    print(file_names)
    os.mkdirs(f'{FOLDERINPUT}/{FOLDERINPUT}_Translated_To_CSV', mode = 0o755, exist_ok = False)
    print("Directory properly created.")
    for FILENAME in file_names:
        with open(f'{FOLDERINPUT}/{FILENAME}', 'r') as file:
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
    
        with open(f'{FOLDERINPUT}/{FOLDERINPUT}_Translated_To_CSV/{FILENAME[0:-4]}.csv', 'w') as file:
            file.write("#Time,X,Y,Z,CONF\n") 
            for h in range(len(Time)):
                StringPrint = f"{Time[h]},{x[h]},{y[h]},{z[h]},{conf[h]}\n"
                file.write(StringPrint);
                
            Time=[]
            x=[]
            y=[]
            z=[]
            conf = []

            Line1 = ""
            line2 = ""

            FirstComma = SecondComma = ThirdComma = FourthComma = False
            
        





__main__()