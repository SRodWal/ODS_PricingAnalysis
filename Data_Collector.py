import os 
import pandas as pd

filedir = os.getcwd()+"\\Data"
filelist = [f for f in os.listdir(filedir) if "CM" in f]

masterdf = pd.DataFrame()
for file in filelist:
    df = pd.read_excel(filedir+"\\"+file)
    cols = df.columns[0]
    df = df.rename(columns=({cols:"Date/Time"}))
    if (df["Date/Time"][0]=="Día y hora")or (df["Date/Time"][0]=="Día y Hora"):
        df = df.drop(index = 0)
    masterdf = masterdf.append(df)

masterdf = masterdf.reset_index().drop(columns=("index"),axis =1)
masterdf.to_excel(os.getcwd()+"\\ODS_CM_Prices.xlsx")