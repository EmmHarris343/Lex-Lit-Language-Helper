import csv
from datetime import datetime
import time
import re # Regex bleh bleh
import numpy as np


from colorama import init, Fore, Back, Style

class fr_words():
    def __init__(self) -> None:
        ## Simple configurations:
        self.freq_threshold = 100                       # Min frequence *score words must be to be added to list
        self.max_lex_word = 500                         # when reached, stops finding words from the lexicon dataset
        self.max_found_words = 1000                     # when reached, stop searching (How many matched words found in sentences)
        self.max_found_sentences = 100000                 # When reached, stop searching (How many sentences with matched words)
        self.limit_sentence_search = 300000              # mostly for testing. Don't go through FULL list of sentences. Limit for speed.
        self.excluded_word_list = ['a', 'ai', 'ce', 'de', 'dans']
        
        ## Additional configurations:
        self.lexi_dtst_word_filename = "fr_lexique-383-.tsv"      ## configure for .env to remove these being hard-coded
        self.sentence_dtst_filename = "fr_sentences.tsv"

        self.detailed_word_list = None
        self.reduce_detail_word_list = None
        self.simplifed_word_list = None

        self.sentence_saved = None      ## List of sentences saved with found words



        
        ## STARTUP BEGUN!
        print(Fore.LIGHTGREEN_EX + "Yo / Wesh - Startup!" + Fore.RESET)
        print('This Classs pulls FR words based on commonality/ frequency seen. (Based on Books (les livres) / Movies (les films))')

        print(Fore.LIGHTGREEN_EX + "Starting to Pull FR Words! " + Fore.RESET)
        self.process_datetime_start = datetime.now()
        self.process_datetime_end = None
        print(Fore.LIGHTBLUE_EX + f"Processed Started at:{self.process_datetime_start}" + Fore.RESET)


        ## Read/ Get words from Lexique
        fnct_dt_start = datetime.now()
        self.read_lex()
        fnct_dt_end = datetime.now()
        time_diff = fnct_dt_end - fnct_dt_start
        print(f'Function Get Lexique took: {time_diff.total_seconds()} sec')

        ## Trim details of words
        fnct_dt_start = datetime.now()
        self.reduce_detail_wordlist(self.detailed_word_list)
        fnct_dt_end = datetime.now()
        time_diff = fnct_dt_end - fnct_dt_start
        print(f'Function Trim Details Took: {time_diff.total_seconds()} sec')


        ## Run the slow function. 
        if self.reduce_detail_word_list is not None and len(self.reduce_detail_word_list) > 1:            
            fnct_dt_start= datetime.now()
            self.find_sntcn_save(self.reduce_detail_word_list)  ## Function
            fnct_dt_end = datetime.now()
            time_diff = fnct_dt_end - fnct_dt_start

            print(f'Function FindWords in sentence Took: {time_diff.total_seconds()} sec')
            

        #NORMAL MODE:
        #self.simplify_word_list()
        #if self.simplifed_word_list is not None and len(self.simplifed_word_list) > 1:
        #    self.test_wrdInSentence(self.simplifed_word_list) ## 


        self.process_datetime_end = datetime.now()
        process_time_diff = self.process_datetime_end - self.process_datetime_start
        print(f'Processed has finished - Took {process_time_diff} sec')

        print(Fore.LIGHTGREEN_EX + "Woa - Appears to have reached end! ===:: Exiting, Bye!; Au-revoir ! ::===" + Fore.RESET)
        pass

    def read_lex(self):
        print('::Beginning Function:: - Pull words from Lexique')
        arr_words = []      # Temp storage of found words
        word_seen = set()   # For duplicate checking
        ignored_words = set()

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
                            found_count += 1
                        else:
                            #print('Already seen word, ignoring', word)
                            ignored_words.add(word)
            print(f'{len(ignored_words)} words already been seen and were not added to list.')
            print(f'Ignored words', ignored_words)
            print('::DONE::')
            self.detailed_word_list = arr_words     ## Pass off from the temp arr_words to the easily accessable one.
  


    def simplify_word_list(self): 
        try:
            if self.simplifed_word_list is None:
                self.simplifed_word_list = []
            for entry in self.detailed_word_list:
                isolate_word = entry.get('Word', 'NULL')        ## Strips all the extra data/ details of word. Supplies **ONLY the word and nothing else.
                
                self.simplifed_word_list.append(entry.get('Word', 'NULL'))
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: warn:err], [Message to say], [pass exception]



    def print_wrdInSentence(self, input_words):
        loop_count = 0
        found_cnt = 0

        print(f'Total words loop go through:{len(input_words)}')
        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:
                if loop_count >= self.limit_sentence_search:
                    print(Fore.LIGHTYELLOW_EX, 'Reached max matched sentence search, exiting...', Fore.RESET)
                    break
                if found_cnt >= self.max_found_words:
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


    def reduce_detail_wordlist(self, wordlist):         ## Maybe call this Trim details (becaues it's not reducing it to nothing)
        print(f'::Beginning Function:: Trim Wordlist details')
        try:
            if self.reduce_detail_word_list is None:
                self.reduce_detail_word_list = []
            for entry in wordlist:
                isolate_word = entry.get('Word', 'NULL')        ## Strips down to more basic form.
                sub_details = entry.get('Details')              ## Points to the Sub (Or nested) details in each Dict
                genre = sub_details.get('Genre')
                infinitive = sub_details.get('Infinitive')
                word_type = sub_details.get('WordType')

                ## Not super safe, if the sub category Details doesn't exist. Will throw error / exception. (Try to catch properly/ send to exception handling!!)


                final_detail_wordlist = {"Word": isolate_word, "Genre": genre, "Infinitive": infinitive, "WordType": word_type}
                self.reduce_detail_word_list.append(final_detail_wordlist)
            print("::DONE::")
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: warn:err], [Message to say], [pass exception]



    def find_sntcn_save(self, input_words):
        print(f'::Beginning Function:: To Find words in sentences, and save :: Total words: {len(input_words)}')

        sentence_loop_count = 0
        individual_found_words_count = 0

        found_sentence_with_words = 0
        sentence_has_word = False
        
        working_sentence = None

        full_list_sentences = []
        

        # for dict_words in input_words:
        #     print(dict_words)
        #     current_word = dict_words.get('Word', 'Null')       ## Not safe, doesn't check if word returned is valid.
        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:                
                # Interupt Checks:
                if sentence_loop_count >= self.limit_sentence_search:
                    print(Fore.LIGHTYELLOW_EX + 'Reached max matched sentence search, exiting...' + Fore.RESET)
                    break
                # if individual_found_words_count >= self.max_found_words:
                #     print(Fore.LIGHTYELLOW_EX, f'Reached max matched words {individual_found_words_count}, exiting...', Fore.RESET)
                #     break
                if found_sentence_with_words >= self.max_found_sentences:
                    print(Fore.LIGHTYELLOW_EX + f'Reached max sentences with matched words {found_sentence_with_words}, exiting...' + Fore.RESET)
                    break

                # Progress updates:
                interval = self.max_found_sentences // 4 ## double slash round down
                if found_sentence_with_words == interval:
                    print(Fore.LIGHTGREEN_EX + 'Process around 25%' + Fore.RESET)
                if found_sentence_with_words == interval *2:
                    print(Fore.LIGHTGREEN_EX + 'Process around 50%' + Fore.RESET)
                if found_sentence_with_words == interval *3:
                    print(Fore.LIGHTGREEN_EX + 'Process around 75%' + Fore.RESET)                


                sentence_has_word = False
                working_sentence = sentence[2] ## The same sentence might be updated multiple times with different words
                found_words = []

                ## Word Processing:

                matched_word_count = 0          ## Reset how many words it found in sentence
                for word_details in input_words:
                    current_word = word_details.get('Word', 'Null')     # Pull just the word for now, out of the dictionary
                    regx_word_pattern = re.compile(r'\b({0})\b'.format(re.escape(current_word)), flags=re.IGNORECASE)
                    matched_word = regx_word_pattern.findall(working_sentence)
                    if len(matched_word) > 0:
                        sentence_has_word = True
                        ##print('Think found')
                        islate_word_pattern = r'(!!)\1(&&)'   
                        added_chrcts = re.sub(regx_word_pattern, islate_word_pattern, working_sentence)      ## Add the speical characters around each word
                        working_sentence = added_chrcts ## Just to be clear, set working sentence back to itself, to add more than 1 word
                        ## Dict, of found words:
                        found_words.append(word_details)
                        individual_found_words_count += 1
                        matched_word_count += 1

                if sentence_has_word is True:
                    found_sentence_with_words += 1


                if matched_word_count > 0:          ## Don't add sentence to list, unless there was actually words in the sentence
                    combine_stnc_words = {"Sentence": working_sentence, "WordDetails": found_words}
                    full_list_sentences.append(combine_stnc_words)
                    #print('Total Sentences with 1 or more Match Words so far? --:', len(full_list_sentences))
            
                sentence_loop_count += 1

        # ----- Finished ---------
        #self.datetime_end = datetime.now()
        #time_dif = self.datetime_end - self.datetime_start


        #print(Fore.LIGHTBLUE_EX + f"Processed Finished at:{self.datetime_end}", Fore.RESET)
        #print(Fore.LIGHTBLUE_EX + f"Processing time took: {time_dif.total_seconds()}", Fore.RESET)

        print('::DONE::')
        print(f'=================\
              \nStats: \
              \n--- Processed:{sentence_loop_count} sentences. \
              \n--- Found:{found_sentence_with_words} sentences with at least 1 word that matched. \
              \n--- Matched:{individual_found_words_count} words total\
              \n--- Used:{len(input_words)} common words in search \
              \n=================')




    def found_sentnce_save(self, sentence, word, word_details):
        print('Split this up later, so it is more easy to read later')





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