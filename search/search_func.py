import re

def substication(word):
    generated_words = []
    for index in range(len(word)):
        for counter in range(26):
            subs_char = chr(97 + counter)
            subs_word = word[:index] + str(subs_char) + word[index + 1:]
            generated_words.append(subs_word)
    return generated_words

def insertion(word):
    generated_words = []
    for index in range(len(word) + 1):
        for counter in range(26):
            ins_char = chr(97 + counter)
            ins_word = word[:index] + str(ins_char) + word[index:]
            generated_words.append(ins_word)
    return generated_words


def deletion(word):
    generated_words = []
    for index in range(len(word)):
        del_word = word[:index] + word[index + 1:]
        generated_words.append(del_word)
    return generated_words

def generate_search_token(word):
    search_tokens = []
    subs = substication(word)
    ins = insertion(word)
    dele = deletion(word)
    search_tokens.extend(subs)
    search_tokens.extend(ins)
    search_tokens.extend(dele)
    return search_tokens

from hashtag.edit_distance import edit_distance
# data is a list of tuples serach function search in first elements and return secend elements
def search(inp, data):
    inp = inp.lower()
    finded = []
    # words = re.split('[^A-Za-z0-9]+', inp)
    edit_distances = {}
    for exp in data:
        # exp_clean = re.sub('[^A-Za-z0-9]+', '', exp[0]).lower()
        exp_clean = exp[0]
        # for word in words:
        #     if word in exp_clean:
        #         finded.append(exp[1])
        #         continue
        #     if len(word) < 5:
        #         continue
        #     search_tokens = generate_search_token(word)
        #     for search_token in search_tokens:
        #         if search_token in exp_clean:
        #             finded.append(exp[1])
        edit_distances[exp[0]] = edit_distance(inp, exp_clean, len(inp), len(exp_clean))
        if("Apa" in exp[0]):
            print(f'{exp[0]}, {exp_clean}, {inp}, {edit_distances[exp[0]]}')
    hashtags = sorted(list(data), key= lambda h: search_key(h, edit_distances))
    result = [h[1] for h in hashtags if edit_distances[h[0]] < len(h[0]) / 2 and edit_distances[h[0]] >= 0]
    return result

def search_key(h, edit_distances):
    if( h[0] in edit_distances):
         return edit_distances[h[0]] 
    else: 
        edit_distances[h[0]] = -1
        return -1