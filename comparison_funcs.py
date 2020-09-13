#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:18:42 2020

@author: ryan
"""
# %% Doc setup
import altair as alt
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sidetable as stb
import spacy, matplotlib, wordcloud, vega, portpicker, plotly, altair_viewer, chart_studio

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from all_particles import particle_df
from all_particles import particle_stb
from all_particles import particle_stb_ext
from all_particles import particledf_split
from itertools import chain
from spacy import displacy
from wordcloud import WordCloud

#%%
alt.themes.enable('dark')

#//TODO: MAKE EACH PART A WORKING FUNCTION
#//TODO: KEEP DFS UNIVERSAL UNTIL GENERALIZING

"""
p1, p2,...pn  /// 4
v
head | token  /// 3
v
pos | tag | dep  /// 2
v
grouped | diverging  /// 1
v
final report  /// 5
"""

"""
#targeted comparisons: 
#ha/ga 
#ni/he/de 
#to/mo 
#ka/ya 
#ne/yo/wa/sa/na/n
#to/tte
#headpos, tag, dep
"""
"""
#%% header images
p_header = Image.new('RGB', (800, 500), color = (255, 255, 255))
fnt = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", 350)
d = ImageDraw.Draw(p_header)
d.text((10,10), "- が -", font=fnt, fill=(0, 0, 0))
p_header.save('outputs/p_header.png')

"""

"""
# coi 
coi=["は","が","に","へ","で","と","も","か","や","ね","よ","わ","さ","な","ん","と","って"]
print(coi)

#for i in top25:
#    exec(f"{i}_df,{i}_stb = particledf_split(i)")
"""

# %% comp dfs

test3=particle_df[particle_df.Token=="が"].stb.freq(["HeadDep"])[["HeadDep","percent"]]
test3a=particle_df[particle_df.Token=="は"].stb.freq(["HeadDep"])[["HeadDep","percent"]]
test3_comb=pd.merge(test3, test3a, on="HeadDep", how="outer", suffixes=("_p1","_p2")).sort_values(by="HeadDep").fillna(0)
test3_comb["Explain"]=[spacy.explain(i) for i in test3_comb.HeadDep]
    
mlt=test3_comb.melt(id_vars=["HeadDep","Explain"])
mlt=mlt[mlt["value"]>1]
    
test3_div=test3_comb[(test3_comb["percent_p1"]>2) | (test3_comb["percent_p2"]>2)]
test3_div["percent_p1"]=-test3_div["percent_p1"]
test3_div["zero"]=0

"""
# %% diverging
#alt.vconcat((basechart+p1+p2+zeroaxis), (basechart+p1+p2+zeroaxis), (basechart+p1+p2+zeroaxis)).save("outputs/diverging.html")

def diverging_single (df_d=test3_div):
    y_axis = alt.Axis(
        title='HeadDep',
        offset=5,
        ticks=False,
        minExtent=60,
        domain=False
        )
    basechart = alt.Chart(df_d).mark_bar().encode(
        x=alt.X("threshold:Q",
            scale=alt.Scale(
                domain=(
                    min(df_d["percent_p1"].append(df_d["percent_p2"]))-5,
                    max(df_d["percent_p1"].append(df_d["percent_p2"]))+5))),
        y=alt.Y('HeadDep:N', axis=alt.Axis(title='HeadDep',offset=5,ticks=False,minExtent=60,domain=False)))
    p1 = alt.Chart(df_d).mark_bar().encode(
        x='percent_p1:Q',
        x2='zero:Q',
        y=alt.Y('HeadDep:N', axis=alt.Axis(title='HeadDep',offset=5,ticks=False,minExtent=60,domain=False)),
        color=alt.Color("percent_p1:Q",
            scale=alt.Scale(scheme="inferno",domain=[-100, 0])))
    p2 = alt.Chart(df_d).mark_bar().encode(
        x='zero:Q',
        x2='percent_p2:Q',
        y=alt.Y('HeadDep:N', axis=alt.Axis(title='HeadDep',offset=5,ticks=False,minExtent=60,domain=False)),
        color=alt.Color("percent_p2:Q",
            scale=alt.Scale(scheme="inferno",domain=[0, 100])))       
    zeroaxis = alt.Chart(df_d).mark_rule().encode(x='zero:Q')

    d=(basechart+p1+p2+zeroaxis)

    return d
"""


"""
#%% grouped horizontal
#//NOTE: concat dont work on these lmao
#.save("outputs/grouped_pos.html")

def grouped_single (df_g=mlt):

    g=alt.Chart(df_g).mark_bar().encode(
        x='value:Q',
        y='variable:O',
        color=alt.Color("variable:N", scale=alt.Scale(scheme="inferno")),
        row="HeadPOS:N")

    return g

#//TODO:consider an interactive particle picker report
#//TODO:need to limit scope of certain multipurpose particles for comparisons
"""
