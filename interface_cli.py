##import argparse # Maybe use ... but for now nah. 

class cli():

    def __init__(self) -> None:
        print('CLI Interface - Initiated')

    def mode_prompt(self) -> None:
        mode_select = input("\
                            === Make a selection ===\n\
                            1. Process word Data (and save) _OG FUNCTION_\n\
                            2. Word Search - Specify word (Normal Word Search)\n\
                            3. Word Search - Specify word (Infinitive Search)"
                            )

    def process_selection(self, selection):
        if selection == "1":
            print('Mod 1: Start normal mode')
        if selection == "2":
            print('Mode 2: Word Search (Normal Word Search)')
        if selection == "3":
            print('Mode 3: Word Search (Infinitive Search)')
    
        if selection != "1" and selection != "2" and selection != "3":
            print("Invalid input selected, please type only numbers '1','2', or '3'")


if __name__ == '__main__':
    cli().__init__