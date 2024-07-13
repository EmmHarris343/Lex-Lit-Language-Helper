import os

class Configuration:

    def __init__(self):
        print('Configuration Startup')

        self.dir_path = os.curdir
        self.lexique_path = self.dir_path + '/fr_lexique-383-.tsv'      # Linux " / "(Maybe change for other OS)
        self.sentence_path = self.dir_path + '/fr_sentences.tsv'        # Linux " / "(Maybe change for other OS)

        self.json_output_file = self.dir_path + '/saved_sentences.json'

        self.lexique_read_limit = 0                 # 0 = No limit; Otherwise limit how many rows it reads (mostly for testing, doesn't really speed things up)

        # Pipeline Lexique Config (Frequency Settings)
        self.lexique_search_by_freq:bool = False
        self.frequency_limit_words:int = 400            # When searching by frequency, Limit how many found words. (10 Fast, 50 bit longer. 400+ takes a while)
        self.frequency_threshold:float = 100            # 0.1 = Really anything, 100 = Very Common, 200+ = Extremely Common (IE: Avoir)
        self.freq_search_type:int = 0                   # 0 = Film / 1 = Livre
        self.excluded_word_list:list = ['a', 'ai', 'ce', 'de', 'dans']

        # Pipeline Lexique Configs (Keyword Settings)
        self.lexique_search_by_keyword:bool = True
        self.lexique_search_keyword:str = 'chat'
        self.lexique_keyword_type:int = 0           # 0 = Current Word / 1 = Infinitif Word
        self.lexique_search_keyword_limit:int = 0   # 0 = no limit; Or limit how many found


        # Pipeline Regx Search/ Match Settings
        self.sentence_loop_limit:int = 100000             # Combien sentences it will loop through
        self.found_sentence_cap:int = 10000                # When it stops searching for more sentences

        



    def load_config(self, value):
        print('Loading config file')
        

if __name__ == '__main__':
    Configuration()