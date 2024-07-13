import csv
from datetime import datetime
import time
import sys
import re # Regex bleh bleh
import numpy as np
import json

from colorama import init, Fore, Back, Style

class fr_words():
    def __init__(self) -> None:
        ## Simple configurations:
        self.freq_threshold = 100                       # Min frequence *score words must be to be added to list
        self.max_lex_word = 100                         # How many common words to use
        self.max_found_words = 50                       # (NOT USED RIGHT NOW) when reached, stop searching (How many matched words found in sentences)
        self.max_found_sentences = 100000                 # When reached, stop searching (How many individual sentences with matched words)
        self.limit_sentence_search = 200000              # mostly for testing. Don't go through FULL list of sentences. Limit for speed.
        self.excluded_word_list:list = ['a', 'ai', 'ce', 'de', 'dans']
        
        ## Additional configurations:
        self.lexi_dtst_word_filename = "fr_lexique-383-.tsv"      ## configure for .env to remove these being hard-coded
        self.sentence_dtst_filename = "fr_sentences.tsv"
        self.json_output_file = 'saved_sentences.json'

        self.save_output = 1        ## 0 no; 1 yes


        self.loaded_sentences:list[str] = None          ## Load all the sentences into memory. Makes it easier to thread/ split into processes

        self.full_detail_word_list = None
        self.simplifed_word_list = None                 ## Only word
        self.trim_detail_word_list = None


        self.sentence_matched_words = None              ## List of sentences with found words
        
        ## STARTUP BEGUN!
        print(Fore.LIGHTGREEN_EX + "Yo / Wesh - Startup!" + Fore.RESET)
        print('This Classs pulls FR words based on commonality/ frequency seen. (Based on Books (les livres) / Movies (les films))')

        print(Fore.LIGHTGREEN_EX + "Starting to Pull FR Words! " + Fore.RESET)
        self.process_datetime_start = datetime.now()
        self.process_datetime_end = None
        print(Fore.LIGHTBLUE_EX + f"Processed Started at:{self.process_datetime_start}" + Fore.RESET)

        self.process_datetime_end = datetime.now()
        process_time_diff = self.process_datetime_end - self.process_datetime_start
        print(f'Processed has finished - Took {process_time_diff} sec')

        print(Fore.LIGHTGREEN_EX + "Woa - Appears to have reached end! ===:: Exiting, Bye!; Au-revoir ! ::===" + Fore.RESET)
        pass






    def full_detail_process(self):
        ## Read/ Get words from Lexique
        fnct_dt_start = datetime.now()
        self.read_lex()
        fnct_dt_end = datetime.now()
        time_diff = fnct_dt_end - fnct_dt_start
        print(f'Function Get Lexique took: {time_diff.total_seconds()} sec')

        ## Transform: Trim details of words
        fnct_dt_start = datetime.now()
        self.trim_details_words(self.full_detail_word_list)
        fnct_dt_end = datetime.now()
        time_diff = fnct_dt_end - fnct_dt_start
        print(f'Function Trim Details Took: {time_diff.total_seconds()} sec')

        ## Load sentences from file
        fnct_dt_start = datetime.now()
        self.load_sentences_tsv()
        fnct_dt_end = datetime.now()
        time_diff = fnct_dt_end - fnct_dt_start
        print(f'Function Load Sentences from TSV Took: {time_diff.total_seconds()} sec')

        ## Core processing - Check if words exist into sentences
        if self.trim_detail_word_list is not None and len(self.trim_detail_word_list) > 1:            
            fnct_dt_start= datetime.now()
            self.match_words_sentence(self.trim_detail_word_list)  ## Function
            fnct_dt_end = datetime.now()
            time_diff = fnct_dt_end - fnct_dt_start
            print(f'Function MatchWords in sentence Took: {time_diff.total_seconds()} sec')

        ## Save to Output file
        if self.save_output == 1 and self.sentence_matched_words:
            fnct_dt_start= datetime.now()
            self.found_sentnce_save(self.sentence_matched_words)
            fnct_dt_end = datetime.now()
            fnct_dt_end = datetime.now()
            time_diff = fnct_dt_end - fnct_dt_start
            print(f'Function Save Output to Json Took: {time_diff.total_seconds()} sec')


    '''
    --- READ LEXIQUE --- 
    Pull words based on frequency threshold from Word Lexique

    '''
    def read_lex(self)-> None:
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
            print(f'{Fore.LIGHTYELLOW_EX} - Notice - Ignored words', ignored_words, Fore.RESET)
            self.full_detail_word_list = arr_words     ## Pass off from the temp arr_words to the easily accessable one.
  
    '''
    Simply Words, reduce words down to ONLY word with no other details
    '''

    def simplify_word_list(self): 
        try:
            if self.simplifed_word_list is None:
                self.simplifed_word_list = []
            for entry in self.detailed_word_list:
                isolate_word = entry.get('Word', 'NULL')        ## Strips all the extra data/ details of word. Supplies **ONLY the word and nothing else.
                
                self.simplifed_word_list.append(entry.get('Word', 'NULL'))
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: warn:err], [Message to say], [pass exception]

    '''
    Simple version, pull words from list. Match in Sentence print out highlighted words

    Does not provide any aditional word details, will only match 1 distinct word per sentence
    
    '''
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


    ### ENDED SIMPLE VERSION

    
    
    
    ### MORE COMPLICATED VERSION:


    '''
    Trim Details of words
    Trims/ Reduces the details in the word list. Stripping out extra details not needed. IE Frequency points etc
    '''

    def trim_details_words(self, wordlist: list[dict])-> None:         ## Maybe call this Trim details (becaues it's not reducing it to nothing)
        print(f'::Beginning Function:: Trim Wordlist details')
        try:
            if self.trim_detail_word_list is None:
                self.trim_detail_word_list = []
            for entry in wordlist:
                isolate_word = entry.get('Word', 'NULL')        ## Strips down to more basic form.
                sub_details = entry.get('Details')              ## Points to the Sub (Or nested) details in each Dict
                genre = sub_details.get('Genre')
                infinitive = sub_details.get('Infinitive')
                word_type = sub_details.get('WordType')

                ## Not super safe, if the sub category Details doesn't exist. Will throw error / exception. (Try to catch properly/ send to exception handling!!)


                final_detail_wordlist = {"Word": isolate_word, "Genre": genre, "Infinitive": infinitive, "WordType": word_type}
                self.trim_detail_word_list.append(final_detail_wordlist)
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: err:warn], [Message to say], [pass exception]


    '''
    ::::Find/ Match Words in Sentences::::
    Slowest --
    1. Loop over each word in list
    2. See if word exists in sentence
    3. If yes:
        1. Add characters around word in sentence, to allow for highlight later
        2. Add entire diction of word, to the sentence

    '''

    def load_sentences_tsv(self) -> None:
        print(f'::Beginning Function:: Load Sentences from TSV')
        all_sentences:list[str] = []
        with open("fr_sentences.tsv") as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:
                all_sentences.append(sentence[2])
        self.loaded_sentences = all_sentences


    def match_words_sentence(self, input_words):
        print(f'::Beginning Function:: Find words in sentences :: Total words: {len(input_words)}')       

        sentence_loop_count:int = 0
        individual_found_words_count:int = 0
        found_sentence_with_words:int = 0
        sentence_results = None
        full_list_sentences:list = []

        ## Pull sentence into variable, and run through ---- THIS MIGHT SPLIT UP into functions later!
        local_sentences:list[str] = self.loaded_sentences
        print(f'{Fore.LIGHTYELLOW_EX}--- Total Sentences available --- {len(local_sentences)}\
               \n--- Sentence Limit --- {self.limit_sentence_search}\
               \n--- If split in 4 threads... each thread would process: {self.limit_sentence_search // 4}\
               \n--- Food for thought.. ---{Fore.RESET}')

        for sentence_line in local_sentences:
            # Interupt Checks:
            if sentence_loop_count >= self.limit_sentence_search:
                print(Fore.LIGHTYELLOW_EX + 'Reached max matched sentence search, exiting...' + Fore.RESET)
                break
            if found_sentence_with_words >= self.max_found_sentences:
                print(Fore.LIGHTYELLOW_EX + f'Reached max sentences with matched words {found_sentence_with_words}, exiting...' + Fore.RESET)
                break

            # Progress updates:
            interval = self.max_found_sentences // 4 ## double slash divide + round down
            if found_sentence_with_words == interval:
                print(Fore.LIGHTGREEN_EX + 'Process around 25%' + Fore.RESET)
            if found_sentence_with_words == interval *2:
                print(Fore.LIGHTGREEN_EX + 'Process around 50%' + Fore.RESET)
            if found_sentence_with_words == interval *3:
                print(Fore.LIGHTGREEN_EX + 'Process around 75%' + Fore.RESET)                

            # Run function to match input words in this specific sentence!
            word_match: dict = self.word_match_loop(sentence_line, input_words)

            if word_match is not None:
                ## Has matched values
                individual_found_words_count += word_match[0]
                found_sentence_with_words += 1
                sentence_results = word_match[1]
            if word_match is not None and sentence_results is not None:
                full_list_sentences.append(sentence_results)
            
            sentence_loop_count += 1

        ## Has finished entire loop. Set local variables to more global ones
        self.sentence_matched_words = full_list_sentences
        send_stats = {"SentenceTotal": sentence_loop_count, "SentenceMatch": found_sentence_with_words,\
                      "WordMatch": individual_found_words_count, "WordList": len(input_words)}
        self.finished_stats(send_stats)


    def word_match_loop(self, input_sentence: list[dict], input_word_list: list[dict]) -> list[int,dict]:
        found_words:list = []
        found_count:int = 0
        build_sentence = None
        obj_return = None
        sentence_has_word:bool = False
        working_sentence:list[dict] = input_sentence

        for word_details in input_word_list:
            ##print('---DEBUG---', 'What is words???, Why is it finding it three times', word_details)
            try:
                current_word = word_details.get('Word', 'Null')     # Pull only the word, so it can search for it in the regex pattern
            except Exception as err:
                self.excption_handling(0, err, "Unable to pull data from Dict: Missing data? Wrong variable passed?")

            regx_word_pattern = re.compile(r'\b({0})\b'.format(re.escape(current_word)), flags=re.IGNORECASE)
            matched_word = regx_word_pattern.findall(working_sentence)
            if len(matched_word) > 0:
                sentence_has_word = True
                islate_word_pattern = r'(!!)\1(&&)'
                added_chrcts = re.sub(regx_word_pattern, islate_word_pattern, working_sentence)      ## Add the speical characters around each word
                working_sentence = added_chrcts         ## Just to be clear, set working sentence back to itself, to add more than 1 word
                found_words.append(word_details)        ## Add the entire word dictionary to sentence/ list
                found_count += 1

        if sentence_has_word is True:               ## Don't add sentence to list, unless there was actually words in the sentence
            build_sentence:dict = {"Sentence": working_sentence, "WordDetails": found_words}
            obj_return:list[int, dict] = [found_count, build_sentence]

        if len(found_words) > 0: return obj_return      ## This likely can be squished into sentence has word 
        else: return None

    def finished_stats(self, completion_stats: dict) -> None:
        sentences_total = completion_stats.get('SentenceTotal', 'Null')
        sentences_match = completion_stats.get('SentenceMatch', 'Null')
        word_match = completion_stats.get('WordMatch', 'Null')
        word_list = completion_stats.get('WordList', 'Null')
        print(f'=================\
              \nStats: \
              \n--- Processed:{sentences_total} sentences. \
              \n--- Found:{sentences_match} sentences with at least 1 word that matched. \
              \n--- Matched:{word_match} words total\
              \n--- Used:{word_list} common words in search \
              \n=================')




    def excption_handling(self, problem_type: int, excptn: Exception, message: str) -> None:
        if problem_type == 0:
            # Error
            print(Fore.LIGHTRED_EX + '-- ERORR -- Exception Occured -- \n' + Fore.RESET, f'Message: {message}\n', f'Exception: {excptn}')
            #raise(excptn)
            sys.exit(1)
            
        if problem_type == 1:
            # Warning
            print(Fore.LIGHTRED_EX + '-- Warning -- Exception Occured -- \n' + Fore.RESET, f'Encountered: {message}\n', f'Exception: {excptn}')


if __name__ == '__main__':
    fr_words().__init__