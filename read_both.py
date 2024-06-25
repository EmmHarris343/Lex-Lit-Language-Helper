import csv
import time
import re # Regex bleh bleh
import numpy as np

from colorama import init, Fore, Back, Style

class fr_words():
    def __init__(self) -> None:
        self.freq_threshold = 100                       # Min frequence *score words must be to be added to list
        self.max_lex_word = 250                         # when reached, stops finding words from the lexicon dataset
        self.max_wrd_sentnce_match = 50                 # when reached, stops matching sentences with words
        self.limit_sentence_search = 10000              # mostly for testing. Don't go through FULL list of sentences. Limit for speed.
        self.detailed_word_list = None
        self.simplifed_word_list = None
        self.excluded_word_list = ['a', 'ai', 'ce', 'de', 'dans']
        
        self.lexi_dtst_word_filename = "fr_lexique-383-.tsv"      ## configure for .env to remove these being hard-coded
        self.sentence_dtst_filename = "fr_sentences.tsv"

        
        ## STARTUP BEGUN!
        print(Fore.LIGHTGREEN_EX, "Yo / Wesh - Startup!", Fore.RESET)
        print('This Classs pulls FR words based on commonality/ frequency seen. (Based on Books (les livres) / Movies (les films))')
        time.sleep(1)        

        print(Fore.LIGHTGREEN_EX, "Starting to Pull FR Words! ", Fore.RESET)

        self.read_lex()       
        
        self.simplify_word_list()
        if self.simplifed_word_list is not None and len(self.simplifed_word_list) > 1:
            self.test_wrdInSentence(self.simplifed_word_list) ## 


        print(Fore.LIGHTGREEN_EX + "Woa - Appears to have reached end! ===:: Exiting, Bye!; Au-revoir ! ::===", Fore.RESET)
        pass

    def read_lex(self):
        arr_words = []      # Temp storage of found words
        word_seen = set()   # For duplicate checking

        with open(self.lexi_dtst_word_filename) as fd:
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

                if found_count >= self.max_lex_word:
                    break
                if word not in self.excluded_word_list:     ## For the love of god who cares about "a" (have)
                    if float(frq_film) >= self.freq_threshold:
                        individual_word = {"Word": word, "Details":{"Genre": genre, "Infinitive": lemme, "WordType": cgram, "Other_WordType": cgram_all, "FreqFilm": frq_film, "FreqLivre": frq_livre}}
                        if word not in word_seen:       
                            word_seen.add(word)         ## (THIS STOPS ANY DUPLICATE WORDS) - It will supress the noun / verb / adj versions of words. (Not currently used, but be aware for future)
                            arr_words.append(individual_word)
                        else:
                            print('Already seen word, ignoring', word)
                        found_count += 1

            self.detailed_word_list = arr_words     ## Pass off from the temp arr_words to the easily accessable one.
  


    def simplify_word_list(self): 
        try:
            for entry in self.detailed_word_list:
                if self.simplifed_word_list is None:
                    self.simplifed_word_list = []
                isolate_word = entry.get('Word', 'NULL')        ## Strips all the extra data/ details of word. Supplies **ONLY the word and nothing else.
                
                self.simplifed_word_list.append(entry.get('Word', 'NULL'))
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: warn:err], [Message to say], [pass exception]



    def test_wrdInSentence(self, input_words):
        loop_count = 0
        found_cnt = 0

        print(f'Total words loop go through:{len(input_words)}')
        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:
                if loop_count >= self.limit_sentence_search:
                    print(Fore.LIGHTYELLOW_EX, 'Reached max matched sentence search, exiting...', Fore.RESET)
                    break
                if found_cnt >= self.max_wrd_sentnce_match:
                    print(Fore.LIGHTYELLOW_EX, 'Reached max matched words, exiting...', Fore.RESET)
                    break
                for current_word in input_words:
                    regx_word_pattern = re.compile(r'\b({0})\b'.format(re.escape(current_word)), flags=re.IGNORECASE)                  
                    matched_word = regx_word_pattern.findall(sentence[2])
                    if len(matched_word) > 0:
                        islate_word_pattern = r'(!!)\1(&&)'   ## Add these special characters around the {{Matched Word}}, so it's easy to replace with ASCII later
                        added_chrcts = re.sub(regx_word_pattern, islate_word_pattern, sentence[2])
                        
                        ascii_1 = added_chrcts.replace('(!!)', Fore.LIGHTMAGENTA_EX)        ## LIGHTMAGENTA ASCII = \x1b[95m
                        ascii_2 = ascii_1.replace('(&&)', Fore.RESET)                       ## RESET ASCII = \x1b[39m
                        hghlt_ = ascii_2

                        print('----------------------------------')
                        # print(Fore.YELLOW + '-- DEBUG -- SPCL-CHRT STRING ===' + Fore.RESET, '"' + added_chrcts + '"')
                        # print(Fore.YELLOW + '-- DEBUG -- Final ASCII Output ===' + Fore.RESET, hghlt_.encode("utf8"))

                        # print(Fore.YELLOW + '-- DEBUG -- Word Matching Details',\
                        #     '\n :: Original Sentence? ==', sentence[2],\
                        #     '\n :: Which Word was Matched? ==', matched_word,\
                        #     f'\n :: This word ""{current_word}"" occured howmanytimes? ', len(matched_word),\
                        #     Fore.RESET)
                        
                        print('CURRENT SENTENCE:', hghlt_)
                        print('Word to Match (CURRENT WORD):', Fore.LIGHTMAGENTA_EX + current_word + Fore.RESET)
                        print('----------------------------------')
                        found_cnt += 1
                loop_count +=1
        print(f'Finished running through sentence & words; Total sentences:{loop_count}')

    ## Advanced (DO LATER!!)
    # Look at the sentence, see if it matched two or more times - if yes, upgrade it's rank

    # Each sentence should be ranked by how many times the word is seen in the phrase. 
    # Print out a phrase for each word say 3 times. - But don't print out more than 3 at a time. 
    # Maybe don't stop at only finding 3 sentences. Because if it matches more than 1 word. It should be ranked up.
    ## POSSIBLY::
    ## {"SentenceID": row[0], "MatchedWord": {"dernier", "depuis", "vue"}, "Sentence": "Je ne l'ai pas vue depuis le mois dernier."}




    def find_sentence_manually(self):
        # Meant for mostly testing. 
        # This matches badly, will find the word inside other words!
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

    def excption_handling(self, problem_type, excptn, message):
        if problem_type == 1:
            # Error
            print(Fore.LIGHTRED_EX + '-- ERORR -- Exception Occured -- \n' + Fore.RESET, f'Message: {message}\n', f'Exception: {excptn}')
        if problem_type == 0:
            # Warning
            print(Fore.LIGHTRED_EX + '-- Warning -- Exception Occured -- \n' + Fore.RESET, f'Encountered: {message}\n', f'Exception: {excptn}')

fr_words().__init__ 