# The Numbers on は, が,  & Co.

---

---

![Obligatory Word Cloud](https://github.com/ryancahildebrandt/particles/blob/master/outputs/particle_cloud.png)

---

---
[*Open*](https://gitpod.io/#https://github.com/ryancahildebrandt/particles) *in gitpod*

## *Purpose*

A project to look at the contexts in which different particles appear most frequently, and see how these contexts compare to conventional wisdom/rules about how the particles are used

---

## *Introduction*
Particles are one of the trickiest things for Japanese learners to pick up, and this project seeks to approach the question of when and where to use some of the more common particles by looking at a little data! I took a couple corpora of Japanese text, annotated them with linguistic features, and narrowed the dataset to the particles and the words they're related to in their respective sentences. From there, I compiled the dependency and part of speech for each token as well as its syntactic head and compared particles that get commonly mixed up by Japanese learners. Alongside each comparison, I gathered some common rules of thumb used to help people distinguish which particles are appropriate in which contexts, for reference. 

---

## *Dataset*
The corpora used for the current project can be found [here](https://www.kaggle.com/bryanpark/japanese-single-speaker-speech-dataset), [here](https://www.kaggle.com/alvations/tatoeba), and [here](https://www.kaggle.com/nltkdata/knb-corpus). They've been processed via the [Ginza](https://github.com/megagonlabs/ginza) library, which is based on [SudachiPy](https://github.com/WorksApplications/SudachiPy) and [spaCy](https://spacy.io/). These corpora represent a mix of transcribed speech, translated example sentences, and blog articles.

---

## *Outputs*

+ The main [report](https://datapane.com/ryancahildebrandt/reports/The_Numbers_on_Particles/?accesstoken=88050a78fe9e93296933b540aba600969cd63b84), compiled with datapane and also in [html](outputs/particles_rprt.html) format
+ The [png](https://github.com/ryancahildebrandt/particles/blob/master/outputs/particle_cloud.png) for the wordcloud used at the top of the page
+ Interactive [sankey](http://htmlpreview.github.io/?https://github.com/ryancahildebrandt/particles/blob/master/outputs/sankey.html) plot for the particles and their attributes
+ Another [sankey](http://htmlpreview.github.io/?https://github.com/ryancahildebrandt/particles/blob/master/outputs/sankey_Head.html), this time for the syntactic heads
+ A comparison of the [top 10](outputs/top10_stacked.html) most commonly used particles
+ Another comparison [chart](outputs/top10_head_stacked.html), this time for syntactic heads
+ The [notebook](NLP.ipynb) for the NLP analyses (NOTE: this takes a very time long to run, I'd avoid it if possible as the remainder of the code runs just fine without having to run this every time)
+ The [notebook](particles_nb.ipynb) for the analyses and viz generated *after* the NLP
