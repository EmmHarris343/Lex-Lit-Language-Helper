import csv
from colorama import init, Fore, Back, Style



Threshold = 10000

loop_count = 0
find_word = "vue"
found_max = 10
found_cnt = 0

print("yo")
with open("fr_sentences.tsv") as fd:     
    rd = csv.reader(fd, delimiter="\t", quotechar='"')    
    for row in rd:          ## Loop through sentences
        if loop_count >= Threshold:
            break
        if found_cnt >= found_max:
            print(Fore.LIGHTYELLOW_EX, 'Reached max matched words, exiting.', Fore.WHITE)
            break
        if find_word in row[2]:
            hghlt_ = row[2].replace(find_word,  Fore.LIGHTMAGENTA_EX + find_word + Fore.WHITE)
            print('Found --->', hghlt_)
            found_cnt += 1
        #print(row[2])
        loop_count +=1
        
