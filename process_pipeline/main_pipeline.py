# process_pipeline/main_pipeline.py

# Modules
from data_reader import data_tsv_read
from data_transform import DataTransformations


# Require Imports
import os
from datetime import datetime
from colorama import init, Fore, Back, Style


class MainPipeline():
    
    def __init__(self):
        print('Initiating pipeline function')
        self.full_detail_word_list = None
        self.trim_detail_word_list = None
        self.sentence_matched_words = None
        self.loaded_lexique = None
        self.loaded_sentences = None
        self.excluded_word_list = ['a', 'ai', 'ce', 'de', 'dans']

        self.dir_path = os.path()
        self.lexique_path = self.dir_path + '/fr_lexique-383-.tsv'      ## Linux / (Maybe change for other OS)
        self.sentence_path = self.dir_path + '/fr_sentences.tsv'      ## Linux / (Maybe change for other OS)



    def _RUN(self):

        self.loaded_lexique = data_tsv_read.lexique_loader_tsv(self, self.lexique_path, self.excluded_word_list, 0)     # 0, Do not limit what it loads into Memory.
        self.loaded_sentences = data_tsv_read.sentence_loader_tsv(self, self.sentence_path)













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