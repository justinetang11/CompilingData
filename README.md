# CompilingData

Attached is a Python Script that takes data from the L/D Box, Open Field, and Fear Conditioning software and compiles it into a concatenated .csv file for you. The code should be as nicely commented as I can possibly make it without it being too messy. I’ve attached a sample file of the Ind-Genotype-List.csv that is called in the code. This is a list that is called when you are trying to parse through the Fear Conditioning files that gives the code the identities and phenotype/genotype/viral injection relations for parsing. It’s based off of Pandas DataFrames and Python Dictionaries.

You should open the code and edit it to fit your file naming format. I put all my folders into C:/Users/Justine Tang/PythonScripts. So the “./” that I’m calling when I write “./MaguireLab/AnalyzeData” and “./MaguireLab/RawData” is “C:/Users/Justine Tang/PythonScripts”. This is because I have Anaconda directed into my C:/Users/Justine Tang” folder.

Also be sure to pay attention to how you’re naming your folders and filenames. The code looks for specific key words in the folder/filenames. You can completely change what the code looks for as well since it’s just a list of keywords. Just add more! 😊
