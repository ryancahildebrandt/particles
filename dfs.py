#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 20:13:18 2020

@author: ryan
"""

# %% Doc setup
import numpy as np
import pandas as pd
import sidetable as stb
import spacy, time, pickle, ginza, ja_ginza, ja_ginza_dict

from itertools import chain
nlp = spacy.load("ja_ginza")
docs = pickle.load(open("docs.p", "rb"))

# %% att & chunk dfs

start = time.time()
#docs=docs[:10]
att_df = pd.DataFrame()
count=0
for doc in docs:
    data = pd.DataFrame([[i.text,i.head.text,i.head.pos_,
                        i.head.tag_,i.head.dep_,i.lemma_,i.norm_,
                        i.is_stop,i.pos_,i.tag_,i.dep_,
                        [child.text for child in i.children]] for i in doc])
    att_df=att_df.append(data)
    count +=1
    print(str((len(docs)-count))+" out of "+str(len(docs))+" remaining, "+("{:.0%}".format(count/len(docs)))+" done")
    
att_df.columns=["Token","Head","HeadPOS","HeadTag","HeadDep",
                      "Lemma","Norm","Stop","POS","Tag","Dep","Children"]    
att_df.to_csv("att_df.csv")

end = time.time()
print(f"ATT Runtime : {end - start} seconds")



