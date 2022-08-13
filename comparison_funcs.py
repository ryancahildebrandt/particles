#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:18:42 2020

@author: ryan
"""
# Doc setup
import altair as alt
import numpy as np
import pandas as pd
import re
import spacy

from all_particles import ht_dict
from all_particles import particle_df
from all_particles import pdt_dict
from all_particles import tag_dict

# lists & notes
alt.themes.enable('dark')

coi=["は","が","に","へ","で","と","も","か","や","ね","よ","わ","さ","な","ん","と","って"]
coi1=["は","と","か","と"]
coi2=["が","も","や","って"]
coi_div=[[str(i),str(j)] for i,j in zip(coi1,coi2)]
coi3=["に","へ","で"]
coi4=["ね","よ","わ","さ","な","ん"]

ht_list=["","Head"]
pdt_list=["POS","Tag","Dep"]
df_list=[
    'div_HeadDep',
 'div_HeadPOS',
 'div_HeadTag',
 'div_Dep',
 'div_POS',
 'div_Tag',
 'grpd_HeadDep',
 'grpd_HeadPOS',
 'grpd_HeadTag',
 'grpd_Dep',
 'grpd_POS',
 'grpd_Tag']

#'Token', 'Head', 'HeadPOS', 'HeadTag', 'HeadDep', 'Lemma', 'Norm', 'Stop', 'POS', 'Tag', 'Dep', 'Children'


# comp dfs

def div_dfs (particle1, particle2, head_token, pos_tag_dep):
    
    #seed_df
    seed1=particle_df[particle_df.Token==particle1].stb.freq([(str(head_token)+str(pos_tag_dep))])[[(str(head_token)+str(pos_tag_dep)),"percent"]]
    seed2=particle_df[particle_df.Token==particle2].stb.freq([(str(head_token)+str(pos_tag_dep))])[[(str(head_token)+str(pos_tag_dep)),"percent"]]
    seed_comb=pd.merge(seed1, seed2, on=(str(head_token)+str(pos_tag_dep)), how="outer", suffixes=("_"+particle1,"_"+particle2)).sort_values(by=(str(head_token)+str(pos_tag_dep))).fillna(0) 
    
    if pos_tag_dep=="Tag": seed_comb["Explain"]=[tag_dict[i] for i in seed_comb[(str(head_token)+str(pos_tag_dep))]]
    else: seed_comb["Explain"]=[spacy.explain(i) for i in seed_comb[(str(head_token)+str(pos_tag_dep))]]
    
    seed_comb.Explain.replace(to_replace=np.nan, value="Root", inplace=True)
    seed_comb.Explain=[i.capitalize() for i in seed_comb.Explain]
    
    #diverging
    div=seed_comb[(seed_comb[("percent_"+str(particle1))]>2) | (seed_comb[("percent_"+str(particle2))]>2)]
    div[str(("percent_"+str(particle1)))]=-div[str(("percent_"+str(particle1)))]
    div["zero"]=0
    
    return div


def div_dict_func ():
    
    particle_df_list=[]  
    for a,b,c,d in [[w,x,y,z] for w in coi1 for x in coi2 for y in ht_list for z in pdt_list]:
            particle_df_list.append(a+b+c+d)
            exec(f"div_{a+b+c+d} = div_dfs(a,b,c,d)")
            
    div_dict={}
    for i in particle_df_list:
        div_dict[i]=pd.DataFrame(eval("div_"+i))
        
    return div_dict


div_df_dict = div_dict_func()

# diverging

def diverging_single (df_key):
    
    alt.themes.enable('dark')
    
    df_match=pd.DataFrame(div_df_dict[df_key])
    ht=re.sub(r"[\[\]\'あ-ん]","",str(df_key)).replace("div_","")[:-3]
    pdt=re.sub(r"[\[\]\'あ-ん]","",str(df_key)).replace("div_","").replace("Head","")
    p1=df_match.columns[1].replace("percent_","")
    p2=df_match.columns[2].replace("percent_","")
    
    df_match.columns=['a', 'b', 'c', 'Explain', 'zero']
    
    basechart = alt.Chart(df_match).mark_bar().encode(
        x=alt.X("threshold:Q",scale=alt.Scale(domain=(-100,100)),title="% of Occurences"),
        y=alt.Y('Explain:N',
                axis=alt.Axis(title=ht_dict[ht]+" "+pdt_dict[pdt],
                              titlePadding=20,
                              offset=15,
                              ticks=False,
                              minExtent=60,
                              labelLimit=100,
                              domain=False)))
    d1 = alt.Chart(df_match).mark_bar().encode(
        x='b:Q',
        x2='zero:Q',
        y=alt.Y('Explain:N', axis=alt.Axis(offset=5,ticks=False,minExtent=60,domain=False)),
        color=alt.Color("b:Q",
            scale=alt.Scale(scheme="inferno",domain=[-100, 0]),
            legend=None),
        tooltip=['Explain'])
    d2 = alt.Chart(df_match).mark_bar().encode(
        x='zero:Q',
        x2='c:Q',
        y=alt.Y('Explain:N', axis=alt.Axis(offset=5,ticks=False,minExtent=60,domain=False)),
        color=alt.Color("c:Q",
            scale=alt.Scale(scheme="inferno",domain=[0, 100]),
            legend=None),
        tooltip=['Explain'])     
    zeroaxis = alt.Chart(df_match).mark_rule().encode(x='zero:Q')

    d=(basechart+d1+d2+zeroaxis).properties(
        width=725,
        height=300)
    #d.save(str("outputs/diverging_"+p1+p2+ht+pdt+".html"))
    return d


# div
def diverging_six (p1,p2):
    
    six_list=[
        str(p1+p2+"Dep"),
        str(p1+p2+"POS"),
        str(p1+p2+"Tag"),
        str(p1+p2+"HeadDep"),
        str(p1+p2+"HeadPOS"),
        str(p1+p2+"HeadTag"),
        ]
    
    v=alt.vconcat(
                  diverging_single(six_list[0]),
                  diverging_single(six_list[1]),
                  diverging_single(six_list[2]),
                  diverging_single(six_list[3]),
                  diverging_single(six_list[4]),
                  diverging_single(six_list[5]),
            title=str(p1+" "*4+"|"+" "*4+p2),
            center=True,
            bounds="full").configure(
                        padding={"left": 15, "top": 25, "right": 50, "bottom": 25}
                        ).configure_axisX(
            labelFontSize=15,
            titleFontSize=20).configure_axisY(
                labelFontSize=12,
                titleFontSize=20).configure_title(
                    align="center",
                    anchor="middle",
                    dx=80,
                    fontSize=125)

    v.save(str("outputs/diverging_six"+p1+p2+".html"))
    return v

for a,b in coi_div:
    exec(f"div_six_{a+b} = diverging_six(a,b)")
# grpd dfs

coi3=["に","へ","で"]
coi4=["ね","よ","わ","さ","な","ん"]
  
def grpd_dfs (coi_list, head_token, pos_tag_dep):
    
    #seed_df
    grpd_seed=pd.DataFrame(columns=[(str(head_token)+str(pos_tag_dep))])
    for i in coi_list:
        seed=particle_df[particle_df.Token==i].stb.freq([(str(head_token)+str(pos_tag_dep))])[[(str(head_token)+str(pos_tag_dep)),"percent"]]
        grpd_seed=pd.merge(grpd_seed, seed, on=(str(head_token)+str(pos_tag_dep)), how="outer").sort_values(by=(str(head_token)+str(pos_tag_dep))).fillna(0) 
    grpd_seed.columns=[(str(head_token)+str(pos_tag_dep))]+["percent_"+i for i in coi_list]

    if pos_tag_dep=="Tag": grpd_seed["Explain"]=[tag_dict[i] for i in grpd_seed[(str(head_token)+str(pos_tag_dep))]]
    else: grpd_seed["Explain"]=[spacy.explain(i) for i in grpd_seed[(str(head_token)+str(pos_tag_dep))]]
    
    grpd_seed.Explain.replace(to_replace=np.nan, value="Root", inplace=True)
    grpd_seed.Explain=[i.capitalize() for i in grpd_seed.Explain]
   
    #grouped
    grpd=grpd_seed.melt(id_vars=[(str(head_token)+str(pos_tag_dep)),"Explain"])
    grpd=grpd[grpd["value"]>2]
    
    return grpd
 
    
coi3_df_list=[]
for a,b in [[x,y] for x in ht_list for y in pdt_list]:
    coi3_df_list.append("grpd_coi3_"+a+b)
    exec(f"grpd_coi3_{a+b} = grpd_dfs(coi3,a,b)")


coi4_df_list=[]
for a,b in [[x,y] for x in ht_list for y in pdt_list]:
    coi4_df_list.append("grpd_coi4_"+a+b)
    exec(f"grpd_coi4_{a+b} = grpd_dfs(coi4,a,b)")

    
# grouped 


def grouped_single (df_name):
    
    alt.themes.enable('dark')
    
    df_match=pd.DataFrame(eval(df_name))
    ht=re.sub(r"[\[\]\']","",str(df_name)).replace("grpd_","").replace("coi3_","").replace("coi4_","")[:-3]
    pdt=re.sub(r"[\[\]\']","",str(df_name)).replace("grpd_","").replace("coi3_","").replace("coi4_","").replace("Head","")
    pn=re.sub(r"[\[\]\'_]","",str(df_name)).replace("grpd","").replace(ht,"").replace(pdt,"")
    pn=str(eval(pn))
    
    df_match.columns=['a', 'Explain', 'variable', 'value']
    df_match.variable= [i.replace("percent_","") for i in df_match.variable]
    
    g=alt.Chart(df_match).mark_bar().encode(
        x=alt.X('value:Q',title="% of Occurences"),
        y=alt.Y('variable:O', 
                axis=alt.Axis(title=None,
                              titlePadding=20,
                              offset=15,
                              ticks=False,
                              minExtent=60,
                              labelLimit=100,
                              domain=False)),
    color=alt.Color("variable:N", scale=alt.Scale(scheme="inferno"), legend=None),
    row=alt.Row("a:N", 
        title=ht_dict[ht]+" "+pdt_dict[pdt]),
    tooltip=["Explain"]).configure(
                        padding={"left": 15, "top": 25, "right": 75, "bottom": 25}
                        ).configure_axisX(
            labelFontSize=15,
            titleFontSize=20).configure_axisY(
                labelFontSize=15,
                titleFontSize=20).configure_title(
                    align="center",
                    anchor="middle",
                    dx=50,
                    fontSize=50).properties(title=re.sub(r"[\[\]\']","",str(pn)).replace(",","    "),
                                            width=725)
    g.save(str("outputs/grouped_"+ht+pdt+re.sub(r"[\[\]\' ]","",str(pn)).replace(",","")+".html"))
    return g


for i in coi3_df_list:
    exec(f"{i}_chart = grouped_single(i)")
    
    
for i in coi4_df_list:
    exec(f"{i}_chart = grouped_single(i)")