#! bin/python
"""
    decode morse code that is not delimited
    with spaces
"""
import string
import sys
import os
import pickle

code = {'a':'.-',
        'b':'-...',
        'c':'-.-.',
        'd':'-..',
        'e':'.',
        'f':'..-.',
        'g':'--.',
        'h':'....',
        'i':'..',
        'j':'.---',
        'k':'-.-',
        'l':'.-..',
        'm':'--',
        'n':'-.',
        'o':'---',
        'p':'.--.',
        'q':'-.--',
        'r':'.-.',
        's':'...',
        't':'-',
        'u':'..-',
        'v':'...-',
        'w':'.--',
        'x':'-..-',
        'y':'-.--',
        'z':'--..',
        '-':'..--..',
        }
short_words = ['am', 'an', 'as', 'at', 'go', 'hi', 'if', 'in', 'is', 
    'it', 'ma', 'me', 'my', 'no', 'of', 'oh', 'on', 'or', 'ox', 'pa', 'so', 
    'to', 'up', 'we', 'a', 'i']
vowels = ['a', 'e', 'i', 'o', 'u', 'y']
wordlistfile = '/usr/share/dict/words'

def main(test_code):

    # make a dict with code as keys and lists of words as values
    # things to watch out for
    # upper and lower case
    # multiple words can have the same undelimited code
    # for example aba and abet are both .__...._
    rcode = get_code_for_wordlist()

    # if we get a reasonable set of words to compare, we can use the 
    # word frequency list from norvig

    # get list of word frequencies from norvig
    print('getting norvig word frequencies')
    wfs = {}
    wfl = []
    with open('norvig.webarchive.txt') as norvig:
        for line in norvig:
            l = line.split()
            wfs[l[0]] = int(l[1])
            wfl.append([l[0], int(l[1])])

    # print 10 entries from norvig to see what they look like
    print(sorted(wfl, key=lambda wfl: wfl[1], reverse=True)[:10])
    
    print('trying to solve')
    print(test_code)
    print()

    # see what words occur at the beginning
    wordlists0 = get_first_word(test_code, rcode)
    print(wordlists0)

    # Stand back. I'm going to try recursion!
    wordlists0 = get_words_in_a_sequence(test_code, rcode, [])
    
def getcode_for_word(input_word):
    # build a dictionary entry with the code as the key and
    # the word it represents as the value

    a = ''
    for letter in input_word:
        a += code[letter]
    return a

def get_code_for_wordlist():
    # build a dictionary entry with the code as the key and
    # the word it represents as the value
    codelistfile = 'codelistpickle'
    if os.path.isfile(codelistfile):
        print('getting code from pickle')    
        with open(codelistfile, 'rb') as fc:
            rcode = pickle.load(fc)
    else:
        print('First pass: getting code the hard way. This will save a pickle to speed up the next pass.')
        all_words = []
        rcode = {}
        wordcode = ''
        
        with open(wordlistfile) as fw:
            for line in fw:
                l = line.strip().lower()
                # remove most one and two letter groups
                if len(l) > 2 or l in short_words:
                    # don't use letter groups with no vowels
                    if has_vowel(l):
                        if l not in all_words:
                            all_words.append(l)
                            wordcode = getcode_for_word(l)
                            if wordcode not in rcode:
                                rcode[wordcode] = [l]
                            else:
                                rcode[wordcode].append(l)
        with open(codelistfile, 'wb') as fc:
            pickle.dump(rcode, fc)
    return rcode
    
def mcode(input_word):
    # return undelimited morse code for input word
    return ''.join([code[letter] for letter in input_word])

def has_vowel(l1):
    for l2 in vowels:
        if l2 in l1:
            return True
    return False

def get_word_score(word_to_score, wfs):
    if word_to_score in wfs:
        return wfs[word_to_score]
    else:
        return 0

def get_words_in_a_sequence(some_code, rcode, so_far):
    # this was one attempt at recursion
    for r in rcode:
        if some_code.find(r) == 0:
            found_words = rcode[r]
            l = len(r)
            # print(found_words, '*', so_far, '*', some_code)
            so_far.append(rcode[r])
            some_code = some_code[l:]
            if some_code and so_far:
                get_words_in_a_sequence(some_code, rcode, so_far)
            elif so_far:
                print()
                list_print(so_far)

def list_print(nested_lists):

    if isinstance(nested_lists[0], list):
        for nested_list in nested_lists:
            list_print(nested_list)
    else:
        print(nested_lists)

def get_first_word(some_code, rcode):
    found_words = []
    for r in rcode:
        if some_code.find(r) == 0:
            found_word = rcode[r]
            found_words.append(found_word)
    return found_words

def remove_from_start(test_code, strtoremove):
    # if you have a good guess for the beginnning of the code string
    # call this function to remove those words
    remove_code = ''.join([code[letter] for letter in strtoremove])    
    return test_code[len(remove_code):]

test_code_source = "maryhadalittlelamb"
test_code = ''.join([code[letter] for letter in test_code_source])

# if you have a good guess for the beginnning of the code string
# call this function to remove those words
test_code = remove_from_start(test_code, '')

main(test_code)


