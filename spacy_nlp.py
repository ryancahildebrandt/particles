#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 18:29:47 2020

@author: ryan
"""
# %% Doc setup
import spacy, time, pickle, ginza, ja_ginza, ja_ginza_dict

from itertools import chain
from readin import raw_text


# %% Model & Docs Spec
start = time.time()

nlp = spacy.load("ja_ginza")
docs= list(nlp.pipe(raw_text, batch_size=100, disable=["ner","textcat"]))

end = time.time()

pickle.dump(docs, open("docs.p", "wb" ))
print(f"NLP Runtime : {end - start} seconds")




