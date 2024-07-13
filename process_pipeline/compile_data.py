



class CompileData():

    def match_words_sentence(self, input_words):
        print(f'::Beginning Function:: Find words in sentences :: Total words: {len(input_words)}')

        sentence_loop_count:int = 0
        individual_found_words_count:int = 0
        found_sentence_with_words:int = 0
        sentence_results = None
        full_list_sentences:list = []

        ## Pull sentence into variable, and run through ---- THIS MIGHT SPLIT UP into functions later!
        local_sentences:list[str] = self.loaded_sentences




        for sentence_line in local_sentences:
            # Interupt Checks:
            if sentence_loop_count >= self.limit_sentence_search:
                print(Fore.LIGHTYELLOW_EX + 'Reached max matched sentence search, exiting...' + Fore.RESET)
                break
            if found_sentence_with_words >= self.max_found_sentences:
                print(Fore.LIGHTYELLOW_EX + f'Reached max sentences with matched words {found_sentence_with_words}, exiting...' + Fore.RESET)
                break

            # Progress updates:
            interval = self.max_found_sentences // 4 ## double slash divide + round down
            if found_sentence_with_words == interval:
                print(Fore.LIGHTGREEN_EX + 'Process around 25%' + Fore.RESET)
            if found_sentence_with_words == interval *2:
                print(Fore.LIGHTGREEN_EX + 'Process around 50%' + Fore.RESET)
            if found_sentence_with_words == interval *3:
                print(Fore.LIGHTGREEN_EX + 'Process around 75%' + Fore.RESET)                

            # Run function to match input words in this specific sentence!
            word_match: dict = self.word_match_loop(sentence_line, input_words)

            if word_match is not None:
                ## Has matched values
                individual_found_words_count += word_match[0]
                found_sentence_with_words += 1
                sentence_results = word_match[1]
            if word_match is not None and sentence_results is not None:
                full_list_sentences.append(sentence_results)
            
            sentence_loop_count += 1

        ## Has finished entire loop. Set local variables to more global ones
        self.sentence_matched_words = full_list_sentences
        send_stats = {"SentenceTotal": sentence_loop_count, "SentenceMatch": found_sentence_with_words,\
                      "WordMatch": individual_found_words_count, "WordList": len(input_words)}
        self.finished_stats(send_stats)


    def word_match_loop(self, input_sentence: list[dict], input_word_list: list[dict]) -> list[int,dict]:
        found_words:list = []
        found_count:int = 0
        build_sentence = None
        obj_return = None
        sentence_has_word:bool = False
        working_sentence:list[dict] = input_sentence

        for word_details in input_word_list:
            ##print('---DEBUG---', 'What is words???, Why is it finding it three times', word_details)
            try:
                current_word = word_details.get('Word', 'Null')     # Pull only the word, so it can search for it in the regex pattern
            except Exception as err:
                self.excption_handling(0, err, "Unable to pull data from Dict: Missing data? Wrong variable passed?")

            regx_word_pattern = re.compile(r'\b({0})\b'.format(re.escape(current_word)), flags=re.IGNORECASE)
            matched_word = regx_word_pattern.findall(working_sentence)
            if len(matched_word) > 0:
                sentence_has_word = True
                islate_word_pattern = r'(!!)\1(&&)'
                added_chrcts = re.sub(regx_word_pattern, islate_word_pattern, working_sentence)      ## Add the speical characters around each word
                working_sentence = added_chrcts         ## Just to be clear, set working sentence back to itself, to add more than 1 word
                found_words.append(word_details)        ## Add the entire word dictionary to sentence/ list
                found_count += 1

        if sentence_has_word is True:               ## Don't add sentence to list, unless there was actually words in the sentence
            build_sentence:dict = {"Sentence": working_sentence, "WordDetails": found_words}
            obj_return:list[int, dict] = [found_count, build_sentence]

        if len(found_words) > 0: return obj_return      ## This likely can be squished into sentence has word 
        else: return None