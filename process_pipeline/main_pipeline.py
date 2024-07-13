# process_pipeline/main_pipeline.py

# Load extra Modules:
from app_conf import Configuration

# Pipeline Modules:
from .data_reader import data_tsv_read
from .data_lex_transform import LexTransform
from .compile_data import CompileData
from .output_save import write_json

# Outside App Imports
import os
from datetime import datetime
from colorama import init, Fore, Back, Style


class MainPipeline():
    
    def __init__(self):
        print('Initiating pipeline function')

        conf = Configuration()      # Pull configs from class, and allow to be locally accessable
        self.conf = conf

        self.tsv_loader = data_tsv_read()
        self.lex_transform = LexTransform()       
        self.sentence_compilier = CompileData()
        
        self.loaded_lexique:list[dict] = None
        self.loaded_sentences:list[str] = None
        self.refined_lexique:list[dict] = None
        self.final_compiled_sentences:list[dict] = None

    '''
    Entry point into Pipeline
    '''        
    def _RUN(self, mode:int = 0):
             
        config = self.conf  # Add readability. to know what is being called.

        check = self.check_list(config.lexique_path, config.lexique_path, 0)
        if check:
            print('Pre-run Checklist, passed, continue with pipeline RUN')

            ## Execute each code block
            self.pipeline_load_data()
            self.pipeline_refine_lexique()
            self.pipeline_compile_lexique()
            self.pipeline_save_output()

    '''
    Simple checklist. So far only checks files exist
    '''
    def check_list(self, sentence_path, lex_path, other)-> bool:
        print('Running checklist..')
        passed:bool = True # Default is true, if anything triggers a false flag, checklist will have failed.

        if not os.path.isfile(sentence_path):
            passed = False
        if not os.path.isfile(lex_path):
            passed = False
        return passed

    '''
    TSV file loading
    '''
    def pipeline_load_data(self):
        config = self.conf  # Add readability. to know what is being called.
        load_lex = self.tsv_loader.lexique_loader_tsv(
            config.lexique_path,
            config.excluded_word_list,
            config.lexique_read_limit,
            )
        self.loaded_lexique = load_lex
              
        load_sentences = self.tsv_loader.sentence_loader_tsv(
            config.sentence_path
            )
        self.loaded_sentences = load_sentences

    '''
    Lexique Refinery
    '''
    def pipeline_refine_lexique(self):
       # --- Refine Lexique Wordlist --- (Notice, if both are True, one will overwrite other!)

        config = self.conf  # Add readability. to know what is being called.
        if config.lexique_search_by_freq is True:
            print('Lexique Refinery; Mode Frequency')
            refined_words = self.lex_transform.refine_wordlex_frequency(
                self.loaded_lexique,
                config.frequency_threshold,
                config.freq_search_type,
                config.frequency_limit_words,
                config.excluded_word_list
                )
            self.refined_lexique = refined_words
            print('Finished refinery, total:', len(refined_words))

            
        if config.lexique_search_by_keyword is True:
            print('Lexique Refinery; Mode Keyword')
            refined_words = self.lex_transform.refine_wordlex_search(
                self.loaded_lexique,
                config.lexique_search_keyword,
                config.lexique_keyword_type,
                config.lexique_search_keyword_limit       ## Honestly feel, this is only going to find 10-30 words tops. Not like 7000. Likely not needed
                )
            self.refined_lexique = refined_words
            print('Finished refinery, total:', len(refined_words))



    '''
    Compile sentences
    '''
    def pipeline_compile_lexique(self):
        config = self.conf  # Add readability. to know what is being called.
        if self.refined_lexique is not None:
            # Make sure this isn't empty.
            compiled_sentences = self.sentence_compilier.match_words_sentence(
                self.refined_lexique, 
                self.loaded_sentences,
                config.sentence_loop_limit,
                config.found_sentence_cap
                )
            self.final_compiled_sentences = compiled_sentences
            print('Finished Compiling sentences, total:', len(compiled_sentences))
            
        

    def pipeline_save_output(self):
        print('Saving file output')
        
        # not best way to do this. but ONLY using function to save output.
        write_json.save_to_output(self, self.final_compiled_sentences)












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


if __name__ == '__main__':
    MainPipeline()