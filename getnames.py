# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 17:58:40 2021

@author: serw1
"""

import os

folderdir = "C:\\Users\\serw1\\Desktop\\Documents\\Work\\ODS Price analysis\\Data"
filetype = ".xlsx"
files = [f for f in os.listdir(folderdir) if "CM" in f]

names = []
for f in files:
    if filetype in f:
        names.append(f)

#### Ordenamos la lista por fecha
def monthNum(num):
    return {1 : "Ene", 2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",7:"Jul",8:"Ago",9:"Sep",10: "Oct",11:"Nov",12:"Dic"}[num]

filenames = []
yrs = [20,21]
for y in yrs:
    bag = [f for f in names if str(y) in f]
    for i in range(1,13):
        filenames.extend([f for f in bag if monthNum(i) in f])