# process_pipeline/data_reader.py

import os
import csv
from colorama import init, Fore, Back, Style

class data_tsv_read():

    def __init__(self):
        self.placeholder = 0




    ## The reason for not just loading. Don't want to map each row / header. Easier to pull just each column thats wanted.
    def lexique_loader_tsv(
            self,
            filename_path: str | bytes | os.PathLike, 
            exclude_word: list = [], 
            read_limit: int = 0
            ) -> list[dict]:
        
        arr_words = []      # Temp storage of found words
        word_seen = set()   # For duplicate checking

        with open(filename_path) as fd:
            rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
            found_count = 0     # Outside of for loop so it counts up. When it reaches self.Max_word
            for row in rd:
                word = row['ortho']                 
                if read_limit != 0 and found_count >= read_limit:
                    break   # If limit reached, stop (For testing usually)
                if word not in exclude_word:
                    individual_dictline = {
                        "Word": row['ortho'],
                        "Details":{
                            "Genre": row['genre'],                  # Genre = Gender of word (if any)
                            "Infinitif": row['lemme'],             # Lemme = Non-Conjugated Infinitive Word form (ai = avoir, fait = faire)
                            "WordType": row['cgram'],               # Cgram = Word Class ie: Noun, Adj
                            "Other_WordType": row['cgramortho'],    # Other Variations of word (if also used as adj, noun, verb etc)
                            "FreqFilm": row['freqfilms2'],
                            "FreqLivre": row['freqlivres']
                        }
                    }                        
                    if word not in word_seen:   ## Duplicate word check
                        word_seen.add(word)         
                        arr_words.append(individual_dictline)
                        found_count += 1
        return arr_words
    

#### BACKUP OF THIS, INCASE I BREAK IT!
    def lexique_loader_tsv_backup(
            self, filename_path: str | bytes | os.PathLike, 
            read_limit: int = 0
            ) -> list[dict]:      
        arr_words = []      # Temp storage of found words
        word_seen = set()   # For duplicate checking

        with open(filename_path) as fd:
            rd = csv.DictReader(fd, delimiter="\t", quotechar='"')
            found_count = 0     # Outside of for loop so it counts up. When it reaches self.Max_word
            for row in rd:
                word = row['ortho']                 # Pull from rows to process
                frq_film = row['freqfilms2']        # Pull from rows to process

                if read_limit != 0 and found_count >= read_limit:       # If no limit passed, no limit.
                    break
                if word not in self.excluded_word_list:
                    if float(frq_film) >= self.freq_threshold:
                        individual_dictline = {
                            "Word": row['ortho'],                       # Actual word in use
                            "Details":{
                                "Genre": row['genre'],                  # Genre = Gender of word (if any)
                                "Infinitive": row['lemme'],             # Lemme = Non-Conjugated Infinitive Word form (ai = avoir, fait = faire)
                                "WordType": row['cgram'],               # Cgram = Word Class ie: Noun, Adj
                                "Other_WordType": row['cgramortho'],    # Other Variations of word (if also used as adj, noun, verb etc)
                                "FreqFilm": row['freqfilms2'],
                                "FreqLivre": row['freqlivres']
                            }
                        }                        
                        if word not in word_seen:   ## DUPLICATE CHECK - This stops Any and ALL duplicates (Might be negative)
                            word_seen.add(word)         
                            arr_words.append(individual_dictline)
                            found_count += 1
        return arr_words


    ## Simply load all sentences into variables / memory.
    def sentence_loader_tsv(self, filename_path: str | bytes | os.PathLike) -> list[str]:
        all_sentences:list[str] = []
        with open(filename_path) as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for sentence in rd:
                all_sentences.append(sentence[2])        
        return all_sentences
    
if __name__ == '__main__':
    data_tsv_read().__init__()