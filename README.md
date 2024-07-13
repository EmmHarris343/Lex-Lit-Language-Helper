## 🗯️ TL;DR

For now - Take common words found in books / films. To provide sentences to help in language learning (In my Case, FR)

-------
## Longer Version:
Uses Language Lexicons, Datasets, and Wordlists. To find sentences and Commonly seen words in Phrases.
It uses the commonly seen words based on Frequency (In dataset). Which is based on Films / Books.

It uses the common words that are ranked. To find those words inside Sentences.

This uses lexicons / datasets from: http://www.lexique.org/ (Not included)
- To find which words are most commonly seen
- This dataset includes very useful data, including the gender of the word (Romantic languages), the infinitive version of the word, if its a noun / verb etc.
- Also includes some pronounciation data, and other useful data I hope to use later.
  
This uses datasets from https://tatoeba.org/en (Not included)
- To provide a list of sentences which the words will be searched through
- This site also has datasets with translations of these sentences in English (Later I may try and leverage this as well)

### 🛠️ Howto Use (Ish):
 - [X] Download a sentence set from https://tatoeba.org/en
 - [X] Download the word list from http://www.lexique.org/
 - [X] Rename file names. Or change configuration naming (app_conf)
 - [X] Adjust to your liking config settings in app_conf. Search mode, how much to process etc
 - [X] run `python3 app.py` | use VS code debugger
 - [x] Hope windows doesn't break it somehow (Was built on linux)



#### 🏆 GOAL:
- To help somewhat with the language learning process
- To help learn more words, understand the gender of word, or learn it's other forms.
- Maybe build a user profile, tracks what's known and won't show the same words again and again.
- [X] Build a word search option. Or search for infinitif word function
- Speed improvements (maybe clustered stuff etc)
- Add some level of UI (maybe more web-based similar to automatic 1111 method)
- Be a challenge to create in python, that is fun to do


#### 💣 To note 💣

- This is entirely a side project, not intended for people to use in this state
- Might be be useful for somebody out there, and they could get it working
- Code is very much so alpha purely testing state
- Names, variables, comments are a mash of Eng/Fr
- Finally, I do hope to add more functionality and continue to contribe to this repo (Time permitting)


This is based on a rough idea from a German Discord user: Bisak