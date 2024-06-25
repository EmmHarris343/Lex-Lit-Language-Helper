import csv
from colorama import init, Fore, Back, Style



# All headers: ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv', 'p_cvcv', 'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv-cv', 'orthrenv', 'phonrenv', 'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


Threshold = 100


print("yo")
with open("fr_lexique-383-.tsv") as fd:     
    rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
    count = 0
    for row in rd:
        word = row['ortho'] 
        phon = row['phon'] ## How pronounced?
        lemme = row['lemme'] ## Lemme (Full word) 
        cgram = row['cgram'] ## Type of word, Noun Adj
        genre = row['genre'] ## Gender of word, if any
        cgram_all = row['cgramortho'] ## all types of words
        frq_lem_film = row['freqlemfilms2']
        frq_film = row['freqfilms2']
        frq_lem_livre = row['freqlemlivres']
        frq_livre = row['freqlivres']
        morphoder = row['morphoder'] ## Full types again
        #if count >= 1000:
        #     break
        count += 1
        # Don't print word, unless common enough
        if float(frq_film) >= Threshold:
            print('[', word,\
                '] .. GENDER [', Fore.LIGHTCYAN_EX, genre, Fore.WHITE, ']',\
                'Type [', Fore.LIGHTBLUE_EX, cgram, Fore.WHITE , '] + All Possible: [', Fore.LIGHTBLUE_EX, cgram_all, Fore.WHITE , ']', \
                '\n                 ---- Seen Frequency ----', Fore.LIGHTMAGENTA_EX, frq_film, frq_livre, Fore.WHITE \
            )