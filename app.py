# app.py

from colorama import init, Fore, Back, Style

import interface_cli
import app_conf

from process_pipeline.main_pipeline import MainPipeline

from control_plane.ctrl_main import CtrlMain

##import read_both // OLD and bad. don't use.
##from process_pipeline.main_ import main_loop()

class lex_lit:
    def __init__(self):
        print('Initializing base App..')

        # things to do first..

        self.ctrl_plane = CtrlMain()
        



        ## All look good. Startup
        self.app_main()



    def app_main(self):
        print(Fore.LIGHTGREEN_EX + "Yo / Wesh - Startup!" + Fore.RESET)

        # MainPipeline()._RUN()


        self.ctrl_plane.main_ctrl()

        self.ctrl_plane.another_ctrl()
        




        print(Fore.LIGHTGREEN_EX + "Reached End, for better or worse. ===:: Exiting, Bye!; Au-revoir ! ::===" + Fore.RESET)



if __name__ == '__main__':
    lex_lit()