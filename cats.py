"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    lst = []
    for i in paragraphs:
        if select(i) == True:
            lst += [i]
               # try to debug with print
        else:
            lst += []
    if len(lst) > k:
        return lst[k] 
    return ''

    # iterate over paragraph
    # when True put it in the list
    # return the kth element
    # keep adding to the list
    

    # END PROBLEM 1


def about(subject):
    """Return a select function that returns whether
    a paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), 'subjects should be lowercase.'
    # BEGIN PROBLEM 2
    def filter(paragraph):
        para = remove_punctuation(paragraph).lower().split()
        for x in subject:
            for a in para: # we don't want all the sentence, we just want a word x, a, b, the word of the list, from the sentence.
                if x == a:
                    return True
        return False
    return filter

    # subject is a list f words
    # "about" is going to take the list
    # return a function that return Boolea

    # END PROBLEM 2


def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed) # split will give 'Cute' and 'Dog!'
    source_words = split(source) # /t means tab, so it's like a blank space
    # BEGIN PROBLEM 3
    
    correct_words = 0

    if typed_words == source_words:
        return 100.0
    elif len(typed_words) == 0 or len(source_words) == 0:
        return 0.0
    else:
        
        for x in range(len(typed_words)):
            
            if x < len(source_words) and typed_words[x] == source_words[x]:
                correct_words += 1
                
        return (correct_words / len(typed_words)) * 100
    
    # float value
    # extra words in typed are incorrect
   
   # this function looks for a single word to match. 
   # a m and b m doesn't match for example
    # but you get 50.0% accuracy because m matches with m
    # single words remember
   # but Cat and cat doesn't match as a word!
   # just evaluate single words, typed and resource
   # THIS FUNC IS NOT GOING TO SPLIT THE LETTERS OF A WORD

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed) / 5) / (elapsed / 60.0) # the / will return float values

    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    
    if typed_word in word_list:
        return typed_word
    else:
        value = min(word_list, key = lambda x: abs(diff_function(typed_word, x, limit))) # value = the word
        if abs(diff_function(typed_word, value, limit)) > limit:
            return typed_word
        else:
            return value
            
        #return x
    # How do we compare the x-diff to the value and return x
    # Pick the word with the min difference
    # Return that word
    # word_list[value]  
        
        # IDEAS
        # min(abs(diff_function(word_list, second, third)))
        # Evaluate the difference between typed_word and diff_f(word_list[0], word_list[1], ...) (of each word of the word_list)
        # Get the absolute value of each difference
        # Pick the word with the min difference
        # Return that word
    # The diff function does the absolute value, get the differente
    # QUESTIONS
        # What is w2 in the diff_function?
        # What does 1 means in 1 if w1[0] and what does 0 means in else 0?

    # END PROBLEM 5


def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a typeding word
        source: a string representing a desired source word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    
    if typed == source:
        return 0
    if limit == 0:
        return 1
    # return (limit == 0) 
    if min(len(typed), len(source)) == 0:
        return max(len(typed), len(source))
    
    diff = (typed[0] != source[0]) # True = 1, False = 0
    # diff = 1 if typed and source have identical initial letter, else 0
    return diff + feline_fixes(typed[1:], source[1:], limit - diff)

    # END PROBLEM 6


def minimum_mewtations(typed, source, limit):
    """A diff function that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    Arguments:
        typed: a typeding word
        source: a string representing a desired source word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
     # Base cases should go here, you may add more base cases as needed.
        # BEGIN
    if limit < 0:
        return 1
    elif typed == source: 
        return 0
    elif min(len(typed), len(source)) == 0:
        return max(len(typed), len(source))
    else:
        diff = typed[0] != source[0]
        add_diff = 1 + minimum_mewtations(typed, source[1:], limit-1)
        remove_diff = 1 + minimum_mewtations(typed[1:], source, limit-1)
        substitute_diff = diff + minimum_mewtations(typed[1:], source[1:], limit-diff)
    
        return min(add_diff, remove_diff, substitute_diff)

        
        # END


def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""

FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    
    if len(typed) <= len(prompt): # the length of the lists

        correct_words = 0
        i = 0
        correct = True

        while i < len(typed) and correct: # i is less than the first wrong word
            if typed[i] == prompt[i]:
                correct_words += 1
                i += 1
            else:
                correct = False # one single = for assignment
        
        progress = correct_words / len(prompt)
        
        dict = {'id': user_id, 'progress': progress}
        
        upload(dict)
        return progress

        # return the progress ratio
    
    # the upload function is going to call on a 2-elements dictionary
        # {'id': 1, 'progress': 0.6}

    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player typeded typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    
    times = []
    for player_times in times_per_player:
            
            inter = []
            for y in range(len(player_times) - 1): # the -1 in a for loop is equivalent to a less or equal in a while loop.

                diff_y = player_times[y+1] - player_times[y]
                inter.append(diff_y)
            times.append(inter)

    num_times = len(times[0]) # length = 2 cuz 2 elements on the list # times[0] is the first list of times 

    return match(words[0:num_times], times) # from zero to the num_times because there might be a case where words is more than times

    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10

    fastest = {player: {word: None for word in word_indices} for player in player_indices}

    for word_index in word_indices:
        for player_index in player_indices:
            word_time = time(match, player_index, word_index)
            if fastest[player_index][word_index] is None or word_time < fastest[player_index][word_index][1]:
                fastest[player_index][word_index] = (get_word(match, word_index), word_time)
    result = [[] for _ in player_indices]

    for word_index in word_indices:
        fastest_word = None
        
        for player_index in player_indices:
            if fastest_word is None or fastest[player_index][word_index][1] < fastest_word[1]:
                fastest_word = fastest[player_index][word_index]
        for player_index in player_indices:
            if fastest[player_index][word_index] == fastest_word:
                result[player_index].append(fastest_word[0])
                break
    
    return result
    
    # which words did player 0 won? the lesser time
    # which words did player 1 won? the lesser time


    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(get_all_words(match)), "word_index out of range of words"
    return get_all_words(match)[word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]


def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]


def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        typed = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - typed).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
