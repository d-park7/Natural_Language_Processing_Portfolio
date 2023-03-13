from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import itertools
from random import seed, randint
import re
import argparse


def parse_args():
    """Parses through the system arguments that user provides
    """
    parser = argparse.ArgumentParser(description="Read from text file")
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        required=True,
        help="Name of text file"
    )
    args = parser.parse_args()
    return args


def parse_text_file(file_name: str) -> str:
    """Parse a text file into a string
    Input: file name
    Returns: string
    """
    try:
        with open(file_name) as file:
            contents = file.read()
    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        return contents


def normalize_text(text: str):
    """Normalize the text using nltk
    
    Input: string
    Return: List of all tokens AND Set of nouns
    """
    # clean text and tokenize
    text = re.sub(r'[/+=.?!,:;()\-\n\d]',' ', text.lower())     # remove punctuation and numbers
    text = re.sub(r'\b\w{5,}\b', ' ', text.lower())             # limit words to length > 5
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if not t in stop_words]
    
    # lemmatize tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in tokens]
    unique_lemmas = set(lemmatized)
    
    # pos tagging
    tags = pos_tag(unique_lemmas)

    # print first 20 lemmas and create list of noun lemmas
    noun_lemmas = set()
    for i, val in enumerate(tags):
        if i < 20:
            print(f'tagged lemma {i + 1}: {val}')        
        if val[1] == 'NN':
            noun_lemmas.add(val[0])                        
    return tokens, noun_lemmas 


def calc_lexical_diversity(text: str):
    text = word_tokenize(text)
    return round(len(set(text)) / len(text), 2)


def guessing_game(noun_list: list):
    """Guessing game similar to hangman of tokenized nouns
    
    Input: List of noun tokens
    Return: None
    """
    points = 5
    seed(1234)
    chooser = randint(0, 49)
    answer = list(noun_list[chooser])
    already_guessed = set()
    display = list('_' * len(answer))

    # Uncomment to view answer for dev purposes
    #print(*answer)

    # convert answer to a Set for easier game handling
    set_answer = set(answer)
    print('Let\'s play a word guessing game!')
    while already_guessed != set_answer:
        print(*display)
        guess = input('Guess a letter: ')

        if guess in already_guessed:
            print('Already guessed this letter, choose another letter')
        elif guess in answer:
            already_guessed.add(guess)

            # change the display to match correct guesses
            i = 0
            while i < len(answer):
                if guess == answer[i]:
                    display[i] = guess
                i += 1

            points += 1
            print(f'Right! Score is {points}')
        elif guess == '!' or points <= 0:
            print('Game Over')
            print('Your score is', points)
            return 
        else:
            points -= 1
            print(f'Sorry, guess again. Score is {points}')
    
    print(*display)
    print('You solved it!')
    print('Current score: ', points)
    

if __name__ == "__main__":
    args = parse_args()
    nltk.download('averaged_perceptron_tagger')

    contents = parse_text_file(args.file_name)
    lexical_diversity = calc_lexical_diversity(contents)
    tokens, nouns = normalize_text(contents)
    print(f'\nNumber of tokens: {len(tokens)}')
    print(f'\nNumber of nouns: {len(nouns)}')

    # create a dictionary of {noun: count of noun in tokens}
    noun_dictionary = dict() 
    for noun in nouns:
        noun_dictionary.update({noun: tokens.count(noun)})
    
    # sort in descending order top 50 nouns with highest count 
    sorted_noun_dictionary = sorted(noun_dictionary.items(), key=lambda x:x[1], reverse=True)
    sorted_noun_dictionary = dict(sorted_noun_dictionary)
    print(f'\nTop 50 common nouns: {sorted_noun_dictionary}\n')
    
    game_nouns = list(itertools.islice(sorted_noun_dictionary, 50))
    guessing_game(game_nouns)