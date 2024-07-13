# process_pipeline/main_pipeline.py

# Modules
from data_reader import data_tsv_read
from data_lex_transform import LexTransform

from app_conf import Configuration


# Require Imports
import os
from datetime import datetime
from colorama import init, Fore, Back, Style


class MainPipeline():
    
    def __init__(self):
        print('Initiating pipeline function')

        
        self.loaded_lexique = None
        self.loaded_sentences = None
        

        

        # BELOW SETTINGS --> Moved to app_conf

        # # Sentencey and Lexique Load:
        # self.dir_path = os.path()
        # self.lexique_path = self.dir_path + '/fr_lexique-383-.tsv'      # Linux / (Maybe change for other OS)
        # self.sentence_path = self.dir_path + '/fr_sentences.tsv'        # Linux / (Maybe change for other OS)
        
        # self.lexique_read_limit = 0                 # 0 = No limit; Otherwise limit how many rows it reads (mostly for testing, doesn't really speed things up)


        # ## Data transformation Info
        # # By Frequency:
        # self.lexique_search_by_freq:bool = True
        # self.frequency_limit_words = 400            # When searching by frequency, Limit how many found words. (10 Fast, 50 bit longer. 400+ takes a while)
        # self.frequency_threshold:float = 100        # 0.1 = Average, 100 = Very Common
        # self.freq_search_type = 0                   # 0 = Film / 1 = Livre
        # self.excluded_word_list = ['a', 'ai', 'ce', 'de', 'dans']
        

        # # By Keyword:
        # self.lexique_search_by_keyword:bool = False
        # self.lexique_search_keyword:str = 'chat'
        # self.lexique_keyword_type:int = 0           # 0 = Current Word / 1 = Infinitif Word
        # self.lexique_search_keyword_limit:int = 0   # 0 = no limit; Or limit how many found


        

        
        


    def _RUN(self, mode:int = 0):

        # --- Load lexique + Sentences into variables / memory ---
        self.loaded_lexique = data_tsv_read.lexique_loader_tsv(
            self, 
            self.lexique_path, 
            self.excluded_word_list, 
            self.lexique_read_limit
            )
        self.loaded_sentences = data_tsv_read.sentence_loader_tsv(
            self, 
            self.sentence_path
            )



        # --- Refine Lexique Wordlist ---
        if self.lexique_search_by_freq is True:
            self.full_detail_word_list = LexTransform.refine_wordlex_frequency(
                self, 
                self.loaded_lexique, 
                self.frequency_threshold, 
                self.freq_search_type, 
                self.frequency_limit_words, 
                self.excluded_word_list
                )
        if self.lexique_search_by_keyword is True:
            self.full_detail_word_list = LexTransform.refine_wordlex_search(
                self, 
                self.loaded_lexique,
                self.lexique_search_keyword,
                self.lexique_keyword_type,
                self.lexique_search_keyword_limit       ## Honestly feel, this is only going to find 10-30 words tops. Not like 7000. Likely not needed
                )













    def _OLD_RUN(self):
        print('Data process pipeline called. Main pipeline starting..')
        
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


        print('Main pipeline - Done. Maybe did something')