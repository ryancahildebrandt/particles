#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:18:42 2020

@author: ryan
"""
# Doc setup
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sidetable as stb

from PIL import Image
from wordcloud import WordCloud

# read in att and chunk dfs from csv
att_df_read=pd.read_csv("att_df.csv", encoding="utf-8")
att_df_read.Tag=att_df_read.Tag.replace("\-","_",regex=True)
att_df_read.HeadTag=att_df_read.HeadTag.replace("\-","_",regex=True)

#  dicts & translation functions

pdt_dict={
    'POS':'Part of Speech (Simple)',
    'Dep':'Syntactic Dependency',
    'Tag':'Part of Speech (Detailed)'
    }
ht_dict={
    '':'Token',
    'Head':'Syntatctic Head'
    }
tag_dict={
    u'名詞_普通名詞_副詞可能':'Noun; Common Noun; Adverb Possible',
    u'動詞_一般':'Verb; General',
    u'動詞_非自立可能':'Verb; Dependent Possible',
    u'名詞_普通名詞_サ変可能':'Noun; Common Noun; Irregular Conjugation Possible',
    u'名詞_普通名詞_一般':'Noun; Common Noun; General',
    u'代名詞':'Pronoun',
    u'名詞_固有名詞_一般':'Noun; Proper Noun; General',
    u'副詞':'Adverb ',
    u'形状詞_一般':'Adjectival Noun; General',
    u'名詞_普通名詞_形状詞可能':'Noun; Common Noun; Adjectival Noun Possible',
    u'形状詞_助動詞語幹':'Adjectival Noun; Auxiliary Verb Stem',
    u'形容詞_非自立可能':'Adjective; Dependent Possible',
    u'接尾辞_名詞的_一般':'Suffix; Nominal; General',
    u'助詞_接続助詞':'Particle; Conjunction Particle',
    u'名詞_普通名詞_助数詞可能':'Noun; Common Noun; Counter Possible',
    u'助詞_格助詞':'Particle; Case Marking Particle',
    u'名詞_普通名詞_サ変形状詞可能':'Noun; Common Noun; Irregular Conjugation Adjectival Noun Possible',
    u'形容詞_一般':'Adjective; General',
    u'連体詞':'Adnominal Adjective',
    u'接続詞':'Conjunction',
    u'名詞_固有名詞_人名_一般':'Noun; Proper Noun; Person Name; General',
    u'名詞_固有名詞_人名_名':'Noun; Proper Noun; Person Name; Given Name',
    u'助詞_係助詞':'Particle; Linking Particle',
    u'助詞_副助詞':'Particle; Adverbial Particle',
    u'感動詞_フィラー':'Interjection; Filler',
    u'名詞_固有名詞_人名_姓':'Noun; Proper Noun; Person Name; Surname',
    u'名詞_固有名詞_地名_一般':'Noun; Proper Noun; Place Name; General',
    u'接尾辞_名詞的_副詞可能':'Suffix; Nominal; Adverb  Possible',
    u'助動詞':'Auxiliary Verb',
    u'接尾辞_名詞的_助数詞':'Suffix; Nominal; Counter',
    u'接尾辞_形状詞的':'Suffix; Adjectival Nominal',
    u'名詞_数詞':'Noun; Number',
    u'形状詞_タリ':'Adjectival Noun; Tari',
    u'助詞_終助詞':'Particle; Sentence Ending Particle',
    u'感動詞_一般':'Interjection; General',
    u'名詞_固有名詞_地名_国':'Noun; Proper Noun; Place Name; Country',
    u'接尾辞_動詞的':'Suffix; Verbal',
    u'接頭辞':'Prefix',
    u'記号_一般':'Symbol; General',
    u'接尾辞_形容詞的':'Suffix; Adjectival',
    u'名詞_助動詞語幹':'Noun; Auxiliary Verb Stem',
    u'接尾辞_名詞的_サ変可能':'Suffix; Nominal; Irregular Conjugation Possible',
    u'補助記号_句点':'Supplementary Symbol; Period',
    u'補助記号_一般':'Supplementary Symbol; General',
    u'補助記号_読点':'Supplementary Symbol; Comma',
    u'助詞_準体助詞':'Particle; Phrasal Particle'
    }




# particle dfs & eda
particle_df=att_df_read[att_df_read.Tag.str.contains("助詞")]
particle_stb = particle_df.stb.freq(["Token"])[:]
particle_stb_ext = particle_df.stb.freq(["Token","POS","Tag","Dep","HeadPOS","HeadTag","HeadDep"])[:]

print(particle_df.head())
print(particle_stb.head())

# split
def particledf_split (particle):
    data = particle_df[particle_df.Token==particle]
    df = pd.DataFrame(data)
    side = pd.DataFrame(particle_df[particle_df.Token==particle].stb.freq(["POS","Tag","Dep","HeadPOS","HeadTag","HeadDep"]))
    df.to_csv("outputs/"+particle+"_df.csv")
    side.to_csv("outputs/"+particle+"_stb.csv")
    return df,side


# cloud
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
plt.show()
#particle_cloud.to_file("outputs/particle_cloud.png")
