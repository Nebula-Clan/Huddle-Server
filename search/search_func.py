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


# data is a list of tuples serach function search in first elements and return secend elements
def search(inp, data):
    inp = inp.lower()
    finded = []
    words = re.split('[^A-Za-z0-9]+', inp)
    for exp in data:
        exp_clean = re.sub('[^A-Za-z0-9]+', '', exp[0]).lower()
        for word in words:
            if word in exp_clean:
                finded.append(exp[1])
                continue
            if len(word) < 5:
                continue
            search_tokens = generate_search_token(word)
            for search_token in search_tokens:
                if search_token in exp_clean:
                    finded.append(exp[1])
    return finded
