import csv
import time
import re # Regex bleh bleh
import numpy as np

from colorama import init, Fore, Back, Style





# All headers: ['ortho', 'phon', 'lemme', 'cgram', 'genre', 'nombre', 'freqlemfilms2', 'freqlemlivres', 'freqfilms2', 'freqlivres', 'infover', 'nbhomogr', 'nbhomoph', 'islem', 'nblettres', 'nbphons', 'cvcv', 'p_cvcv', 'voisorth', 'voisphon', 'puorth', 'puphon', 'syll', 'nbsyll', 'cv-cv', 'orthrenv', 'phonrenv', 'orthosyll', 'cgramortho', 'deflem', 'defobs', 'old20', 'pld20', 'morphoder', 'nbmorph']


class fr_words():

    # Step 1:
    # Put all the desired words into one object (list/ dict).
    # Step 2:
    # Check to see if any of those words exist in any of the sentences (Do this a good way and not a bad way - for speed)

    # Step 3:
    # If words match. Print / Send to the function to print / format it.



    def __init__(self) -> None:
        self.Freq_Threshold = 100       ## Min Frequence words must be to be added to list
        self.Max_Limit_Matched_Word = 250    ## Grab Popular Words Limit (Only pull X amount of words)
        #self.Max_Limit_Sentence = 12
        self.detailed_word_list = None
        self.simplifed_word_list = None
        self.excluded_word_list = ['a', 'ai']

        
        ## STARTUP BEGUN!
        print(Fore.LIGHTGREEN_EX, "Yo / Wesh - Startup!", Fore.RESET)
        print('This Classs pulls FR words based on commonality/ frequency seen. (Based on Books (Les Livres) / Movies (Du Films))')
        time.sleep(.5)        
        print(Fore.LIGHTGREEN_EX, "Starting to Pull FR Words! ", Fore.RESET)
        time.sleep(1)
        self.read_lex()
        #print('That was done.. but is there anything in the dict?', self.word_list)
        
        
        self.simplify_word_list()
        if self.simplifed_word_list is not None and len(self.simplifed_word_list) > 1:
            self.test_wrdInSentence(self.simplifed_word_list) ## 


        print(Fore.LIGHTGREEN_EX + "Woa - Appears to have reached end! ===:: Exiting, Bye!; Au-revoir ! ::===", Fore.RESET)
        pass

    def read_lex(self):      
        arr_words = []      # Temp storage of found words
        word_seen = set()   # For duplicates

        with open("fr_lexique-383-.tsv") as fd:     
            rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
            found_count = 0     # Outside of for loop so it counts up. When it reaches self.Max_word
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

                if word not in self.excluded_word_list:     ## For the love of god who cares about "a" (have)
                    if float(frq_film) >= self.Freq_Threshold:
                        individual_word = {"Word": word, "Details":{"Genre": genre, "Infinitive": lemme, "WordType": cgram, "Other_WordType": cgram_all, "FreqFilm": frq_film, "FreqLivre": frq_livre}}
                        if word not in word_seen:       
                            word_seen.add(word)         ## (THIS STOPS ANY DUPLICATE WORDS) - However, it will supress The Verb, or Noun as well. (It only cares what the exact word is!
                            arr_words.append(individual_word)   ## Add to array
                        else:
                            print('Already seen word, ignoring', word)
                        found_count += 1      ## Adds to word limit count (ONLY WHEN IT FINDS WORDS)
                    if found_count >= self.Max_Limit_Matched_Word:
                        break
            self.detailed_word_list = arr_words     ## Match the temp arr_words to the Easily accessable one.
  
    def simplify_word_list(self): 
        try:
            #print('.... Test', self.word_list)
            for entry in self.detailed_word_list:
                if self.simplifed_word_list is None:
                    self.simplifed_word_list = []
                print(entry.get('Word', 'NULL'))
                isolate_word = entry.get('Word', 'NULL')        ## Strips all the extra data. Supplies **ONLY the word and nothing else.
                
                self.simplifed_word_list.append(entry.get('Word', 'NULL'))

        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to process Json dict, Entry Missing? Type-Mismatch?')       ## [0-1: warn:err], [Message to say], [pass exception]


    def test_wrdInSentence(self, input_words):

        print(input_words)

        Max_Sentences = 10000
        loop_count = 0
        found_max = 5
        found_cnt = 0

        test_text = f'Here is a {Fore.LIGHTCYAN_EX}list{Fore.RESET} of text!'
        print(test_text.encode("utf8")) ## RAW OUTPUT: b'Here is a \x1b[96mlist\x1b[37m of text!'

        print(f'Total words loop go through:{len(input_words)}')

        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:          ## Loop through sentences
                # NOW!! Loop through sentences.
                # Now, For each sentence. Loop through the list of Popular* words, and see if any of them match in THIS sentence

                if loop_count >= Max_Sentences:
                    break
                if found_cnt >= found_max:
                    print(Fore.LIGHTYELLOW_EX, 'Reached max matched words, exiting.', Fore.RESET)
                    break

                for current_word in input_words:    ## Check if each word in the input Matches any in the current Sentence!
                    
                    ## Regex that hopefully works: (?i)\A|[^a-z]ai\b
                    #if re.match(r'(?i)\A|[^a-z](ai)\b', sentence[2]):
                    #if re.match(r'(?i)\a|\b('+ current_word +')\b', sentence[2]):


                    ## Working Regex 
                    # Step one, generate a Regex pattern to find the words needed
                    # Step two, see if it can find the word ANYWHERE in the sentence (Keyword being "word", not characters in word)
                    
                    # Step three - Highlight the word(s) found in the string.
                        # Step 1, use the previously defined regx pattern
                        # Step 2, Generate a replacement pattern. Which Finds, and Adds Raw Ascii to a string
                        # Step 3, using re.sub specify the original pattern, the replacement "pattern", and the sentence it's found in.

                    # Step four, Print out and enjoy highlited text. Maybe cry?

                    regx_word_pattern = re.compile(r'\b({0})\b'.format(re.escape(current_word)), flags=re.IGNORECASE)   ## Build the Regex Pattern (specifying the current word (Escaped to avoid weird regex matches))
                    
                    matched_word = regx_word_pattern.findall(sentence[2]) # This builds a list of the words found (IE [a, ai]) in the current sentence)

                    ## Fore.LIGHTMAGENTA_EX + current_word + Fore.RESET

                    if len(matched_word) > 0:  ## THIS ONLY MATCHES 1 WORD AT A TIME!
                        ## Technically the word is found and it's done. BUT, lets add highting.. (THIS TOOK FOR EVER!!!)

                        islate_word_pattern = r'(!!)\1(&&)'   ## Add these special characters around the {{Matched Word}}, so it's easy to replace with ASCII later
                        added_chrcts = re.sub(regx_word_pattern, islate_word_pattern, sentence[2])
                        
                        ascii_1 = added_chrcts.replace('(!!)', Fore.LIGHTMAGENTA_EX)        ## LIGHTMAGENTA ASCII = \x1b[95m
                        ascii_2 = ascii_1.replace('(&&)', Fore.RESET)                       ## RESET ASCII = \x1b[39m
                        hghlt_ = ascii_2

                        print('----------------------------------')
                        print(Fore.YELLOW + '-- DEBUG -- SPCL-CHRT STRING ===' + Fore.RESET, '"' + added_chrcts + '"')
                        print(Fore.YELLOW + '-- DEBUG -- Final ASCII Output ===' + Fore.RESET, hghlt_.encode("utf8"))

                        print(Fore.YELLOW + '-- DEBUG -- Word Matching Details',\
                            '\n :: Original Sentence? ==', sentence[2],\
                            '\n :: Which Word was Matched? ==', matched_word,\
                            f'\n :: This word ""{current_word}"" occured howmanytimes? ', len(matched_word),\
                            Fore.RESET)
                        
                        print('CURRENT SENTENCE:', hghlt_)
                        print('Word to Match (CURRENT WORD):', Fore.LIGHTMAGENTA_EX + current_word + Fore.RESET)
                        print('----------------------------------')
                        found_cnt += 1




                    #     print('Match.....', found_cnt)
                    #     print(sentence[2])
                    #     #print('YES! Found Match --->', current_word)
                    #     #print('Sentence: ', sentence[2].replace(current_word,  Fore.LIGHTMAGENTA_EX + current_word + Fore.RESET))
                    #     found_cnt += 1
                    # if current_word in sentence[2]:
                    #     print('YES! Found Match --->', current_word)
                    #     print('Sentence: ', sentence[2].replace(current_word,  Fore.LIGHTMAGENTA_EX + current_word + Fore.RESET))
                    #     found_cnt += 1
                        
            loop_count +=1
        print(f'Finished running through sentence & words; Total sentences:{loop_count}')




                # if loop_count >= Max_Sentences:
                #     break
                # if found_cnt >= found_max:
                #     print(Fore.LIGHTYELLOW_EX, 'Reached max matched words, exiting.', Fore.RESET)
                #     break
                # if list_of_words in sentence[2]:                ## k, can't do a list for an IN command.
                #     hghlt_ = sentence[2].replace(find_word,  Fore.LIGHTMAGENTA_EX + find_word + Fore.RESET)
                #     print('NEAT! Found --->', hghlt_)
                #     found_cnt += 1
                # loop_count +=1




    def find_sentence(self):
    
        ## DON'T USE!!
    
        Max_Sentences = 10000
        loop_count = 0
        find_word = "vue"
        found_max = 10
        found_cnt = 0

        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:          ## Loop through sentences
                if loop_count >= Max_Sentences:
                    break
                if found_cnt >= found_max:
                    print(Fore.LIGHTYELLOW_EX, 'Reached max matched words, exiting.', Fore.RESET)
                    break
                if find_word in row[2]:
                    hghlt_ = row[2].replace(find_word,  Fore.LIGHTMAGENTA_EX + find_word + Fore.RESET)
                    print('Found --->', hghlt_)
                    found_cnt += 1
                loop_count +=1


    ## Advanced (DO LATER!!)
    # Look at the sentence, see if it matched two or more times - if yes, upgrade it's rank

    # Each sentence should be ranked by how many times the word is seen in the phrase. 
    # Print out a phrase for each word say 3 times. - But don't print out more than 3 at a time. 
    # Maybe don't stop at only finding 3 sentences. Because if it matches more than 1 word. It should be ranked up.
    ## POSSIBLY::
    ## {"SentenceID": row[0], "MatchedWord": {"dernier", "depuis", "vue"}, "Sentence": "Je ne l'ai pas vue depuis le mois dernier."}



    def excption_handling(self, problem_type, excptn, message):
        if problem_type == 1:
            # Error
            print(Fore.LIGHTRED_EX + '-- ERORR -- Exception Occured -- \n' + Fore.RESET, f'Message: {message}\n', f'Exception: {excptn}')
        if problem_type == 0:
            # Warning
            print(Fore.LIGHTRED_EX + '-- Warning -- Exception Occured -- \n' + Fore.RESET, f'Encountered: {message}\n', f'Exception: {excptn}')

fr_words().__init__ 