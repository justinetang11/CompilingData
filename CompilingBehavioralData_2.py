# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 18:48:34 2021

@author: Justine Tang
"""
import pandas
import glob
import os

#############This section has code that takes data from the light-dark box and open field
#############experiments and puts them into a .csv file

def lightDarkOpenField(name, filename, df2):    
    if i == 0:
        df = pandas.read_csv(filename) #creating a new df and saving this df as a second version
        df2 = df
    elif i > 0:
        df = pandas.read_csv(filename) #this allows for concatenation of all dataframes to save into a .csv file for later.
        df2 = pandas.concat([df, df2])
    else:
        print("What is happening?!")
    return df2

def ldofCSVsaver(name, path, df2):
    if name != path:
        #print(df2.columns)
        df2 = df2.sort_values(by = ['Txt/Geno'], axis = 0, ascending = True, key=lambda col: col.str.lower())
        df2 = df2.drop(columns = ["Interval","Parameters","Date","Time","Session Info 0", "Session Info 1" ,"Session Info 2","Session Info 3","optional"])
        df2.insert(0,'Experiment', str(name))
        #df2.to_csv(str(name)+'Compilation.csv', index = False)
        df2.to_csv(str(savepath)+"/"+str(name)+'Compilation.csv', index = False)            
    else:
        pass
    return

##########################################################################################
##############This part of the code writes the data into a .csv file from fear conditioning

def fearConditioning(filename, tempDict, genolist, genodict, heading):
    j = 1
    heading = []
    tempdf = pandas.read_csv(filename)
    new_header = tempdf.iloc[0]
    dff = tempdf[1:2]
    dff.columns = new_header
    
    tempDict = genodict
    for columns in dff.columns:
          if type(columns) == str:
              for words in genolist:
                  if columns.startswith(words):
                      tempDict[words].append(dff.at[1,columns])
                  else:
                      pass
          else:
              pass
    
    dictLen = len(tempDict[genolist[0]])
    
    heading = ['Txt/Geno'] #This basically creates a heading array that allows for the trial #'s to be generated for labeling purposes within the .csv file.
    while j < dictLen:
        heading.append("Trial "+str(j))
        j += 1
    
    newfilename, newDF = fcBuildCSV(filename, tempDict, genolist, heading, dictLen)
    
    if "freeze" in filename.lower():
        print("This is a freeze file.")
        newfilename = str(m)+"freeze_"+newfilename+"_Compilation"
    elif "boutdur" in filename.lower():
        print("This is a bout duration file.")
        newfilename = str(m)+"boutdur_"+newfilename+"_Compilation"
    elif "interval" in filename.lower():
        print("This is an interval file.")
        newfilename = str(m)+"interval_"+newfilename+"_Compilation"
    elif "nbouts" in filename.lower():
        print("This is an nbouts file.")
        newfilename = str(m)+"nbouts_"+newfilename+"_Compilation"
    else:
        print("Unknown file.")
        
    newDF.to_csv(str(savepath)+"/"+str(newfilename)+'.csv', index_label = "Individual")       
    return

def fcBuildCSV(filename, tempDict, genolist, heading, dictLen):
    cond = ["day1", "trial1", "training", "train"]
    extinct = ["day2", "day3", "trial2", "trial3", "extinction", "ext"]
    retrieve = ["day4", "day5", "trial4", "trial5", "retrieval", "ret"]
    
    
    if any(word in filename.lower() for word in cond):
        print("This is a Conditioning file.")
        newfilename = "Conditioning"
    elif any(word in filename.lower() for word in extinct):
        print("This is a Extinction file.")
        newfilename = "Extinction"
    elif any(word in filename.lower() for word in retrieve):    
        print("This is a Retrival file.")
        newfilename = "Retrieval"
    else:
        print("Nothing here.")
        
    newDF = pandas.DataFrame.from_dict(tempDict, orient='index', columns = heading)
    newDF = newDF.sort_values(by = 'Txt/Geno' , axis = 0, ascending = True, key=lambda col: col.str.lower())
    return newfilename, newDF

###############################################################################
################################Main Code######################################

savepath = "./MaguireLab/AnalyzeData" ##this path is where you want to SAVE all of your data
##make this path anything you want. Typically it'll be where you house
##your anaconda or python packages. I have mine in C:/Users/Justine Tang/PythonScripts. That's what the ./
##part is [i.e the home path]
path = "./MaguireLab/RawData" ##this is the path that you pull your data from. Similar ./ home path.

i = 0
m = 0
###The list below you can change the words in here to match how you've named your files
expTypeLDBof = ["light", "dark", "box", "lbd", "ld", "open", "field", "of"]
expTypeEPM = ["epm", "elevated", "plus", "maze"]
expTypeFC = ["fear", "conditioning", "fc"]
expTypeFST = ["fst", "fs", "forced", "swim", "test"]
genoCSV = ["individual", "ind", "geno", "genotype", "manipulation"]


genodict = {}
tempDict = {}

genolist = []
heading = []


df2 = pandas.DataFrame()

#for the labeling of your compiled .csv files to work, make sure the folder that
#houses your data is labeled with the experiment title like LDB, LightDark, OF, or openfield
#see arrays above for the specific words used for parsing

for dirpath, dirnames, files in os.walk(path): 
    print(f'Found directory: {dirpath}')
    name = dirpath.replace(str(path)+'\\','')
    
    if "\\" in name:
        name = name.replace("\\", "_")
    else:
        pass
    
    if any(word in name.lower() for word in expTypeEPM):
        print("This is EPM. File already parsed properly.")
        continue
    elif any(word in name.lower() for word in expTypeFST):
        print("This is FST. File already parsed properly.")
        continue
    elif name != path and any(word in name.lower() for word in expTypeLDBof):
        print("We are starting with the following data: "+str(name))
        if glob.glob(os.path.join(dirpath, '*.csv')): 
            for filename in glob.glob(os.path.join(dirpath, '*.csv')): #walking through the file names in a folder...
                if any(word in name.lower() for word in expTypeLDBof):
                    df2 = lightDarkOpenField(name, filename, df2)
                    i += 1 
                else:
                    print("Do not compute.")
        else:
            print("There are no .csv files in this folder.")
            continue
    elif any(word in name.lower() for word in expTypeFC) and any(word not in name.lower() for word in expTypeLDBof):
        #print("This is FC. File already parsed properly.")
        #genoFilename = input("What is the name of the filename with the individual genotype identification? Type full name without .csv at end. ")
        ###so the two lines above, you can uncomment them and then comment the genoFilename = "Ind-Genotype-List" if you want to continually change the name.
        ###if not, I'd just say keep the Ind-Genotype-List the same and run your code through.
        genoFilename = "Ind-Genotype-List" ###This should be in the same folder as all your fear conditioning data you're parsing through. 
        genoFilename = dirpath+"//"+genoFilename+".csv"
        
        df = pandas.read_csv(genoFilename)
        
        genodict = {row[0]:[row[1]] for row in df.values}
        genolist = df["Individual"].to_list()

        if glob.glob(os.path.join(dirpath, '*.csv')): #this walks through your file
            for filename in glob.glob(os.path.join(dirpath, '*.csv')): #this calls up the files that end with .csv
                if any(word in filename.lower() for word in genoCSV): 
                    pass 
                else:
                    fearConditioning(filename, tempDict, genolist, genodict, heading) ### Calls the functions that is coded up-top
                    m += 1
                    pass
                genodict = {}
                genodict = {row[0]:[row[1]] for row in df.values}
        continue
    else:
        pass

        
    ldofCSVsaver(name, path, df2)
                
    i = 0
    m = 0
    genodict = {}