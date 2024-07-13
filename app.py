# app.py

import os
from colorama import init, Fore, Back, Style


import app_conf
import interface_cli

from process_pipeline.main_pipeline import MainPipeline

##import read_both // OLD and bad. don't use.
##from process_pipeline.main_ import main_loop()

from process_pipeline.main_pipeline import main_pipeline        ## Pipeline Class

class lex_lit:


    def __init__(self):
        print('Initialization')

        ## All look good. Startup

    def app_main(self):
        print('Startup')
        print(Fore.LIGHTGREEN_EX + "Yo / Wesh - Startup!" + Fore.RESET)

        print(Fore.LIGHTGREEN_EX + "Reached End, for better or worse. ===:: Exiting, Bye!; Au-revoir ! ::===" + Fore.RESET)


        self.dir_path = os.path()
        self.lexique_path = self.dir_path + '/fr_lexique-383-.tsv'      # Linux / (Maybe change for other OS)
        self.sentence_path = self.dir_path + '/fr_sentences.tsv'        # Linux / (Maybe change for other OS)

        print("Path + Lexique", self.lexique_path)
        print("Path + Lexique", self.sentence_path)




        MainPipeline()._RUN()





if __name__ == '__main__':
    lex_lit().__init__