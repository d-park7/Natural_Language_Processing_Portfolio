import os
import pickle
from nltk import word_tokenize
from nltk.util import ngrams


def parse_text_file(file_path: str) -> str:
    """Parse a text file into a string

    Input: file name

    Returns: str
    """
    try:
        contents = ''
        with open(os.path.join(os.getcwd(), file_path)) as file:
            for line in file:
                contents = contents + line.rstrip('\n')
    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        return contents


def create_ngrams_as_dict(text: list) -> dict:
    """Create a unigram dict and bigram dict

    Input: list of strings to create ngrams from

    Returns: unigram dict AND bigram dict
    """
    unigrams = word_tokenize(text)
    bigrams = list(ngrams(unigrams, 2))
    
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {n:bigrams.count(n) for n in set(bigrams)}
    return unigram_dict, bigram_dict 


if __name__ == "__main__":
    # English train data
    contents = parse_text_file('data/LangId.train.English')
    unigram_dict , bigram_dict = create_ngrams_as_dict(contents)
    pickle.dump(unigram_dict, open('data/LangId.train.English.unigram.p', 'wb'))
    pickle.dump(bigram_dict, open('data/LangId.train.English.bigram.p', 'wb'))    


    # French train data
    contents = parse_text_file('data/LangId.train.French')
    unigram_dict , bigram_dict = create_ngrams_as_dict(contents)
    pickle.dump(unigram_dict, open('data/LangId.train.French.unigram.p', 'wb'))    
    pickle.dump(bigram_dict, open('data/LangId.train.French.bigram.p', 'wb'))    


    # Italian train data
    contents = parse_text_file('data/LangId.train.Italian')
    unigram_dict , bigram_dict = create_ngrams_as_dict(contents)
    pickle.dump(unigram_dict, open('data/LangId.train.Italian.unigram.p', 'wb'))    
    pickle.dump(bigram_dict, open('data/LangId.train.Italian.bigram.p', 'wb'))    