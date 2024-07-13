from os import path

class Configuration:

    ## This I think is mostly designed to make it so there can be a config that might be loaded from a file

    def __init__(self):
        print('Configuration Startup')

        self.dir_path = path()
        self.lexique_path = self.dir_path + '/fr_lexique-383-.tsv'      # Linux " / "(Maybe change for other OS)
        self.sentence_path = self.dir_path + '/fr_sentences.tsv'        # Linux " / "(Maybe change for other OS)


        self.lexique_read_limit = 0                 # 0 = No limit; Otherwise limit how many rows it reads (mostly for testing, doesn't really speed things up)

        # Pipeline Search (Frequency Settings)
        self.lexique_search_by_freq:bool = True
        self.frequency_limit_words = 400            # When searching by frequency, Limit how many found words. (10 Fast, 50 bit longer. 400+ takes a while)
        self.frequency_threshold:float = 100        # 0.1 = Average, 100 = Very Common
        self.freq_search_type = 0                   # 0 = Film / 1 = Livre
        self.excluded_word_list = ['a', 'ai', 'ce', 'de', 'dans']

        # Pipeline Search (By Keyword)
        self.lexique_search_by_keyword:bool = False
        self.lexique_search_keyword:str = 'chat'
        self.lexique_keyword_type:int = 0           # 0 = Current Word / 1 = Infinitif Word
        self.lexique_search_keyword_limit:int = 0   # 0 = no limit; Or limit how many found        


    def load_config(self, value):
        print('Loading config file')