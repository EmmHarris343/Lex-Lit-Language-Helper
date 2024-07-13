import sys
import re # Regex bleh bleh




class DataTransformations:

    def __init__(self):
        self.trim_detail_word_list = None
        self.refined_wordlexique = None

    def refine_wordlex_frequency(self, wordlist: list[dict], freq_search: int, freq_type: int = 0, word_limit:int = 0, exluded_words:list = []) -> list[dict]:
        found_count:int = 0
        word_frequency:float = None
        final_word_list:list[dict] = []

        for word_entry in wordlist:
            isolate_word = word_entry.get('Word', 'NULL')
            sub_details = word_entry.get('Details')
            # What type of Frequency it will search (default 0, Films)
            if freq_type == 0: word_frequency = float(sub_details.get('FreqFilm'))
            if freq_type == 1: word_frequency = float(sub_details.get('FreqLivre'))
            
            if word_limit != 0 and found_count >= word_limit:
                break
            if float(word_frequency) >= freq_search:
                if isolate_word not in exluded_words:
                    final_word_list.append(word_entry)
                    found_count += 1        
        
        return final_word_list


    def refine_wordlex_search(self, wordlist: list[dict], _keyword:str, search_type: int = 0, word_limit:int = 0) -> list[dict]:
        found_count:int = 0
        final_word_list:list[dict] = []

        search_word:str = ''
        for word_entry in wordlist:
            isolate_word = word_entry.get('Word', 'NULL')
            sub_details = word_entry.get('Details')
            isolated_infinitif = sub_details.get('Infinitif')

            if search_type == 0:        
                search_word = isolate_word          # Search for Word in current form
            if search_type == 1:        
                search_word = isolated_infinitif    # Search for infinitive form
            
            if word_limit != 0 and found_count >= word_limit:
                break
            if search_word == _keyword:
                final_word_list.append(word_entry)
                found_count += 1
        
        return final_word_list



    ## It's already kind of small. But, to make it smaller ..... could still do this.       At this point just strips out the frequency/ other word classs found
    def trim_details_words(self, wordlist: list[dict])-> list[dict]:        
        try:
            final_word_list:list[dict] = []
            for entry in wordlist:
                # Nest-Layer 0
                isolate_word = entry.get('Word', 'NULL')        ## Get just the word
                
                # Nest-Layer 1
                sub_details = entry.get('Details')              ## Points to the Sub (Or nested) details in each Dict
                genre = sub_details.get('Genre')
                infinitive = sub_details.get('Infinitif')
                word_type = sub_details.get('WordType')

                ## Build dictionary line for each word
                trimed_word_dict = {"Word": isolate_word, "Genre": genre, "Infinitif": infinitive, "WordType": word_type}
                final_word_list.append(trimed_word_dict)
                return final_word_list
        except Exception as err:
            self.excption_handling(1, err, 'Failure when trying to simplify words list/ dict, Entry Missing? Type-Mismatch?')       ## [0-1: err:warn], [Message to say], [pass exception]


 