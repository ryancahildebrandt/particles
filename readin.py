#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 16:23:43 2020

@author: ryan
"""
# %% Doc setup
import glob, re, string
import numpy as np
import pandas as pd


# %% Read in single speaker
jsss = pd.read_csv("data/japanese-single-speaker-speech-dataset/transcript.txt",
                     header=None,
                     sep="|",
                     names=["file","JA","RJ","duration"]).JA




# %% Read in knb
knb_gourmet = pd.read_csv("data/knb-corpus/knbc/knbc/corpus2/Gourmet.tsv",
                        header=None,
                        sep="\t",
                        names=["ID","JA1","JA2","JA3","JA4","JA5"])
knb_keitai = pd.read_csv("data/knb-corpus/knbc/knbc/corpus2/Keitai.tsv",
                        header=None,
                        sep="\t",
                        names=["ID","JA1","JA2","JA3","JA4","JA5"])
knb_kyoto = pd.read_csv("data/knb-corpus/knbc/knbc/corpus2/Kyoto.tsv",
                        header=None,
                        sep="\t",
                        names=["ID","JA1","JA2","JA3","JA4","JA5"])
knb_sports = pd.read_csv("data/knb-corpus/knbc/knbc/corpus2/Sports.tsv",
                        header=None,
                        sep="\t",
                        names=["ID","JA1","JA2","JA3","JA4","JA5"])

knb_full = knb_gourmet.append(knb_keitai).append(knb_kyoto).append(knb_sports).fillna(" ")
knb_full["JA"] = knb_full.JA1 + knb_full.JA2 + knb_full.JA3 + knb_full.JA4 + knb_full.JA5
knb = knb_full.JA

# %% Read in tatoeba
tatoeba = pd.read_csv("data/tatoeba.txt",
                      header=None,
                      sep=";;",
                      names=["EN", "JP", "Source"]).JP

# %% All together now
raw_text = jsss.append(knb).append(tatoeba).astype("unicode").str.strip()
raw_str = raw_text.str.cat(sep=" ").strip()
raw_str = re.sub(r"[^一-龯ぁ-ゞァ-ヶ０-９。、？！]","", raw_str)
raw_str = re.sub(r"[。]","。;", raw_str)
#print(raw_str[:1000])
raw_text = raw_str.split(sep=";")
#print(raw_text[:100])
print(raw_str,  file = open("raw_str.txt", 'w'))
