#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:18:13 2020

@author: ryan
"""
# Doc setup
import datapane as dp

from all_particles import particle_df
from all_particles import particle_stb
from comparison_funcs import div_six_かや
from comparison_funcs import div_six_とって
from comparison_funcs import div_six_とも
from comparison_funcs import div_six_はが
from comparison_funcs import grpd_coi3_Dep_chart
from comparison_funcs import grpd_coi3_HeadDep_chart
from comparison_funcs import grpd_coi3_HeadPOS_chart
from comparison_funcs import grpd_coi3_HeadTag_chart
from comparison_funcs import grpd_coi3_POS_chart
from comparison_funcs import grpd_coi3_Tag_chart
from comparison_funcs import grpd_coi4_Dep_chart
from comparison_funcs import grpd_coi4_HeadDep_chart
from comparison_funcs import grpd_coi4_HeadPOS_chart
from comparison_funcs import grpd_coi4_HeadTag_chart
from comparison_funcs import grpd_coi4_POS_chart
from comparison_funcs import grpd_coi4_Tag_chart

# Reports
rprt = dp.Report(dp.Markdown("""
# The Numbers on は, が,  & Co.
> ##### Contextual particle frequency in written Japanese, taking a swing at the age old question of は vs が

Particles are one of the trickiest things for Japanese learners to pick up, and this project seeks to approach the question of when and where to use some of the more common particles by looking at a little data! I took a couple corpora of Japanese text, annotated them with linguistic features, and narrowed the dataset to the particles and the words they're related to in their respective sentences. From there, I compiled the dependency and part of speech for each token as well as its syntactic head and compared particles that get commonly mixed up by Japanese learners. Alongside each comparison, I gathered some common rules of thumb used to help people distinguish which particles are appropriate in which contexts, for reference. 

---

  * [Dataset](#dataset)
    + [Full NLP for All Particles](#full-nlp-for-all-particles)
    + [Relative Frequency for All Particles](#relative-frequency-for-all-particles)
  * [Particle Comparisons](#particle-comparisons)
    + [は & が](#-----)
        * [Common Heuristics](#common-heuristics)
        * [Insights](#insights)
    + [と & も](#-----)
        * [Common Heuristics](#common-heuristics-1)
        * [Insights](#insights-1)
    + [か & や](#-----)
        * [Common Heuristics](#common-heuristics-2)
        * [Insights](#insights-2)
    + [と & って](#------)
        * [Common Heuristics](#common-heuristics-3)
        * [Insights](#insights-3)
    + [に、へ、で](#-----)
        * [Common Heuristics](#common-heuristics-4)
        * [Insights](#insights-4)
    + [ね、よ、わ、さ、な、ん](#-----------)
        * [Common Heuristics](#common-heuristics-5)
        * [Insights](#insights-5)


                 """),
                 dp.Markdown("""
## Dataset
The corpora used for the current project can be found [here](https://www.kaggle.com/bryanpark/japanese-single-speaker-speech-dataset), [here](https://www.kaggle.com/alvations/tatoeba), and [here](https://www.kaggle.com/nltkdata/knb-corpus). They've been processed via the [Ginza](https://github.com/megagonlabs/ginza) library, which is based on [SudachiPy](https://github.com/WorksApplications/SudachiPy) and [spaCy](https://spacy.io/). These corpora represent a mix of transcribed speech, translated example sentences, and blog articles.

### Full NLP for All Particles
>*Linguistic attributes for all tokens tagged as any sort of particle*
                 """),
                 dp.Table(particle_df),
                 dp.Markdown("""
### Relative Frequency for All Particles
>*Frequency table for all particles, including counts, percentages, and cumulative statistics*
                 """),
                 dp.Table(particle_stb),
                 dp.Markdown("""
---

## Particle Comparisons
>*Here, we can look at the contexts in which different particles appear most frequently, and see how these contexts compare to conventional wisdom/rules about how the particles are used*

### は & が
#### Common Heuristics
+ One common way to differentiate は and が is that は marks the *topic* of a sentence, where が marks the grammatical *subject* in a sentence. 
+ In this sense, は can lend more emphasis to the subject it marks as compared to が
+ が tends to be used more in noun and subordinate clauses, and if は is used in these contexts, it tends to be for emphasis

#### Insights
+ **Token**
    * は and が are used in much the same contexts, with the main area of divergence occurring in the detailed part of speech
    * は functions exclusively as a linking particle, while が functions mostly as a case marking particle
+ **Syntactic Head**
    * Whereas が occurs largely with subjects of sentences, は is more evenly split between subjects and indirect objects
    * This trend shows across dependencies and part of speech distributions, with は appearing in a wider range of contexts
                 """),
                 dp.Plot(div_six_はが),
                 dp.Markdown("""
### と & も
#### Common Heuristics
+ と and も are both used to talk about more than one thing in a sentence
+ と is used to list things (very similar to "and" in English)
+　も takes a previous statement or context and applies it to a new subject (similar to "as well" or "also")
+ も can replace subject/topic markers は and が

#### Insights
+ **Token**
    * と and も occur almost entirely in the same contexts when looking at dependencies
    * When looking at the tags, と functions as a case marker, while も functions as a linking particle
+ **Syntactic Head**
    * The largest difference between と and も syntactic heads occurs in the dependencies, with と occurring alongside nominal and adverbial clause modifiers, and も occurring with oblique nominals and indirect objects

                 """),
                 dp.Plot(div_six_とも),
                 dp.Markdown("""
### か & や
#### Common Heuristics
+ か and や have a number of functions, but share the role of listing options or alternatives (similar to "or")
+ compared to か, や carries with it the implication that the list being given is not exhaustive
+ か has more uses across different sentence structures than や, but や can be more common in different dialects of Japanese

#### Insights
+ **Token**
    * や occurs mostly as a case marker, while か (as might be expected from the different functions of the particle) is split between case marking and auxiliary particle roles
    * This pattern is seen for part of speech and tags as well, with や occurring mostly as an adposition and か split between adposition and particle
+ **Syntactic Head**
    * The main contrast between these particles shows across dependencies, part of speech, and tags, with か occurring primarily with roots & verbs, and や occurring alongside nouns
                 """),
                 dp.Plot(div_six_かや),
                 dp.Markdown("""
### と & って
#### Common Heuristics
+ Both と and って are used as quotation particles
+ って is used as a more casual version of と, especially in speech
+ って can also indicate the subject of a sentence depending on context and formality

#### Insights
+ **Token**
    * Similar to other particle pairs, these two occur in much the same roles, with the main difference being that と occurs primarily as a case marker and って showing up as an adverbial particle
    * As expected, と also functions as a conjunction in ways that って does not
+ **Syntactic Head**
    * Differences between と and tte are much less pronounced than the other particle pairs, the only significant deviation being that where syntactic head dependencies for と are split between adverbial clause and nominal modifiers, って is spread between these two as well as indirect objects

                 """),
                 dp.Plot(div_six_とって),
                 dp.Markdown("""
### に、へ、で
#### Common Heuristics
+ に, へ, and で are all used in contexts relating to location (spatial or temporal)
+ で has the additional function of indicating the means by which an action is accomplished, or how a target is reached
+ に defines where or when something *is*, and often accompanies motion verbs to describe the origin or destination
+ で defines where or when something *is done*
+ へ is more commonly used in set phrases or expressions, as it carries a more refined/formal connotation than に, even though it shares many functions with に
+ へ is　therefore more closely associated with motion verbs and more limited in its usage

#### Insights
+ **Token**
    * に, へ, and で all show up in largely the same roles, mainly as case marking and adposition particles
    * で also appears as an auxiliary and conjunctive particle given its other functions
+ **Syntactic Head**
    * へ appears alongside compound and nominal modifiers only, while に appears with a much wider range of nominal and other syntactic heads
    * で appears in many contexts similar to に, with additional appearances alongside adverbial syntactic heads
    * notably, へ almost never occurs alongside a verb and is much more common with proper nouns than に or で
                 """),
                 dp.Plot(grpd_coi3_Dep_chart),
                 dp.Plot(grpd_coi3_POS_chart),
                 dp.Plot(grpd_coi3_Tag_chart),
                 dp.Plot(grpd_coi3_HeadDep_chart),
                 dp.Plot(grpd_coi3_HeadPOS_chart),
                 dp.Plot(grpd_coi3_HeadTag_chart),
                 dp.Markdown("""
### ね、よ、わ、さ、な、ん
#### Common Heuristics
+ All of these particles come at the end of a sentence (or a word, in some cases), each adding a different nuance to the utterance
+ ね is used to seek agreement or confirmation at the end of a statement without explicitly asking a question
+ よ is used to add emphasis to a statement, and is a more forward/assertive ending than ね
+ わ is used to make an assertion or express an opinion, often with a softer feel than other similar particles
+ さ can be used similarly to な, ね, and よ, functioning to add emphasis or express an opinion (with the possibility for confirmation) in a more gruff manner
+ な is used very similarly to ね in that it asserts something and opens the statement to confirmation/agreement, albeit with a more rough feel to it 
+ ん takes an assertion or factual statement (when combined with です) and puts it into a more explanatory or sometimes apologetic context 

#### Insights
+ **Token**
    * ん stands apart from the rest of the group, functioning almost exclusively as a marking particle and subordinating conjunction
    * さ has a wider range of functions, including compound and nominal modifier, that the other particles don't share
    * the rest of the particles in this group function largely as auxiliary, sentence ending particles
+ **Syntactic Head**
    * These particles occur mostly with Roots, adverbial clauses, adjectival modifiers, and nominal modifiers
    * さ occurs with pronouns and particles where other particles do not
    * ね shows up with adverbs and adjectives in ways that other particles do not

                 """),
                 dp.Plot(grpd_coi4_Dep_chart),
                 dp.Plot(grpd_coi4_POS_chart),
                 dp.Plot(grpd_coi4_Tag_chart),
                 dp.Plot(grpd_coi4_HeadDep_chart),
                 dp.Plot(grpd_coi4_HeadPOS_chart),
                 dp.Plot(grpd_coi4_HeadTag_chart),
                 dp.Markdown("""
# 完了
                 """)
                 )
rprt.save(path='outputs/particles_rprt.html', open=False)
rprt.publish(name='The_Numbers_on_Particles', open=True, visibility='PUBLIC')
#https://datapane.com/ryancahildebrandt/reports/The_Numbers_on_Particles/?accesstoken=88050a78fe9e93296933b540aba600969cd63b84
