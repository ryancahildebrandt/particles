#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:18:42 2020

@author: ryan
"""
# Doc setup
import altair as alt
import pandas as pd
import plotly

from all_particles import particle_df
from all_particles import particle_stb_ext

alt.themes.enable('dark')

top25=particle_df.Token.value_counts()[:25].index.tolist()
print(top25)

top10=particle_df.Token.value_counts()[:10].index.tolist()
print(top10)

coi=["は","が","に","へ","で","と","も","か","や","ね","よ","わ","さ","な","ん","と","って"]
print(coi)

#for i in top10:
#    exec(f"{i}_df,{i}_stb = particledf_split(i)")
#alt.Color("HeadPOS", scale=alt.Scale(scheme="inferno"))



stacked_headpos=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="HeadPOS")
stacked_headtag=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="HeadTag")
stacked_headdep=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="HeadDep")

top10_head_stacked=alt.vconcat(stacked_headpos, stacked_headtag, stacked_headdep).resolve_scale(
    color='independent')
top10_head_stacked.save(
    "outputs/top10_head_stacked.html")
top10_head_stacked.show()


# stacked
stacked_pos=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="POS")
stacked_tag=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="Tag")
stacked_dep=alt.Chart(particle_stb_ext[particle_stb_ext["Token"].isin(top10)]).mark_bar().encode(
    x=alt.X('sum(percent)', stack="normalize"),
    y='Token',
    color="Dep")

top10_stacked=alt.vconcat(stacked_pos, stacked_tag, stacked_dep).resolve_scale(
    color='independent')
top10_stacked.save(
    "outputs/top10_stacked.html")
top10_stacked.show()

# sankey 
#https://gist.github.com/ken333135/09f8793fff5a6df28558b17e516f91ab#file-gensankey
sankey_df = particle_stb_ext[["Token","POS","Tag","Dep","count"]][particle_stb_ext["Token"].isin(top10)]
sankey_Head_df = particle_stb_ext[["Token","HeadPOS","HeadTag","HeadDep","count"]][particle_stb_ext["Token"].isin(top10)]


def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#000003', '#410967', '#932567', '#DC5039', '#FBA40A', '#FCFEA4']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 25,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 15
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

sankey_dict = genSankey(sankey_df,
          cat_cols=["Token","Dep","POS","Tag"],
          value_cols='count',
          title='Top 10 Particles: Sankey (Token)')
sankey_Head_dict = genSankey(sankey_Head_df,
          cat_cols=["Token","HeadDep","HeadPOS","HeadTag"],
          value_cols='count',
          title='Top 10 Particles: Sankey (Syntactic Head)')


sankey=plotly.offline.plot(sankey_dict,
                           filename="outputs/sankey.html",
                           validate=False,
                           auto_open=False)
sankey_Head=plotly.offline.plot(sankey_Head_dict,
                           filename="outputs/sankey_Head.html",
                           validate=False,
                           auto_open=False)