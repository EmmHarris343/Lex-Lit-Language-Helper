#.
from colorama import init, Fore, Back, Style

import interface_cli
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





if __name__ == '__main__':
    lex_lit().__init__