#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:18:42 2020

@author: ryan
"""
# %% Doc setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sidetable as stb

from PIL import Image
from itertools import chain
from wordcloud import WordCloud

# %% read in att and chunk dfs from csv
att_df_read=pd.read_csv("att_df.csv", encoding="utf-8")

# %% shifts df
shifts_list=["Token","Head","HeadPOS","HeadTag","HeadDep","Lemma","Norm","Stop","POS","Tag"]

shifts_df=pd.concat([att_df_read,
                     att_df_read[shifts_list].shift(1),
                     att_df_read[shifts_list].shift(2),
                     att_df_read[shifts_list].shift(3),
                     att_df_read[shifts_list].shift(-1),
                     att_df_read[shifts_list].shift(-2),
                     att_df_read[shifts_list].shift(-3)],
                    axis=1,
                    ignore_index=True).reset_index(drop=True)
shifts_df.columns=list(chain(att_df_read.columns,
                             [i + "_prev1" for i in shifts_list],
                             [i + "_prev2" for i in shifts_list],
                             [i + "_prev3" for i in shifts_list],
                             [i + "_post1" for i in shifts_list],
                             [i + "_post2" for i in shifts_list],
                             [i + "_post3" for i in shifts_list]))
print(shifts_df.head())

# %% particle dfs & eda
particle_df=shifts_df[shifts_df.Tag.str.contains("助詞")]
particle_stb = particle_df.stb.freq(["Token"])[:]
particle_stb_ext = particle_df.stb.freq(["Token","POS","Tag","Dep","HeadPOS","HeadTag","HeadDep"])[:]

print(particle_df.head())
print(particle_stb.head())

# %% split
def particledf_split (particle):
    data = particle_df[particle_df.Token==particle]
    df = pd.DataFrame(data)
    side = pd.DataFrame(particle_df[particle_df.Token==particle].stb.freq(["POS","Tag","Dep","HeadPOS","HeadTag","HeadDep"]))
    df.to_csv("outputs/"+particle+"_df.csv")
    side.to_csv("outputs/"+particle+"_stb.csv")
    return df,side

# %% cloud
bubble_mask=np.array(Image.open("data/mask.png"))
def transform_format(val):
    if val == 0:
        return 255
    else:
        return val
bubble_mask = np.ndarray((bubble_mask.shape[0],bubble_mask.shape[1]), np.int32)

for i in range(len(bubble_mask)):
    bubble_mask[i] = list(map(transform_format, bubble_mask[i]))

print(bubble_mask)
particle_cloud = WordCloud(width=2400,
                           height=1600,
                           min_font_size=40,
                           max_font_size=800,
                           prefer_horizontal=.7,
                           relative_scaling=0,
                           font_path="data/corp_round_v1.ttf",
                           background_color="black",
                           collocations = False,
                           mask=bubble_mask,
                           contour_width=3,
                           contour_color='firebrick'
                           ).generate_from_frequencies(dict(particle_stb[["Token","count"]].values.tolist()))
plt.imshow(particle_cloud, interpolation='bilinear')
plt.axis("off")
#plt.show()
particle_cloud.to_file("outputs/particle_cloud.png")



    
