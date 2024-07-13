
import re
import os
from datetime import datetime
from colorama import init, Fore, Back, Style


class CompileData():

    def __init__(self):
        self.placeholder = 0
        pass


    def match_words_sentence(
            self, 
            lex_words:list[dict], 
            input_sentences:list[str],
            limit_sentences:int = 0,
            found_sentence_cap: int = 0
            ) -> list[dict]:        # Returns sentences with words in them
        
        sentence_results:dict = None
        s_w_Final:list[dict] = []
        sentence_count:int = 0
        word_count:int = 0
        word_sentence_count:int = 0
        
        for _s in input_sentences:
            # Interupt Checks:
            if sentence_count >= limit_sentences:
                break
            if word_sentence_count >= found_sentence_cap:
                break

            # Breakout to function --> 
            word_search = self.word_match_loop(_s, lex_words)

            if word_search is not None:
                word_count += word_search[0]
                sentence_results = word_search[1]

                s_w_Final.append(sentence_results)
                word_sentence_count += 1
            sentence_count += 1
        return s_w_Final

    def word_match_loop(
            self, 
            input_sentence: list[dict],
            lex_word_list: list[dict]
            ) -> list[int,dict]:

        # SET Working Sentence:
        working_sentence:list[dict] = input_sentence

        # Loop variables:
        match_word:list = []
        word_count:int = 0
        sentence_has_word:bool = False

        for _w in lex_word_list:
            word_to_search = _w.get('Word')     # SET word to use in search
            regx_search_pattern = re.compile(r'\b({0})\b'.format(re.escape(word_to_search)), flags=re.IGNORECASE)
            regx_match = regx_search_pattern.findall(working_sentence)           
            if len(regx_match) > 0:
                sentence_has_word = True
                
                regx_char_pattern = r'(!!)\1(&&)'
                regx_added_chrcts = re.sub(regx_search_pattern, regx_char_pattern, working_sentence)      ## Add the speical characters around each word
                working_sentence = regx_added_chrcts

                match_word.append(_w)
                word_count += 1

        # Outside Loop / Finished:
        if sentence_has_word:
            build_sentence:dict = {"Sentence": working_sentence, "WordDetails": match_word}
            obj_return:list[int, dict] = [word_count, build_sentence]
            return obj_return
        else: return None


    def pull_word_from_list(self, word_line ):
        print('this one')

    def add_characters_sentence(self, working_sentence, characters, search_pattern):
        print('Do thing')

if __name__ == '__main__':
    CompileData()