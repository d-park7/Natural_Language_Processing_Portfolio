import os
import pickle
from nltk import word_tokenize, ngrams

def parse_text_file_into_str(file_path: str) -> str:
    """Parse a text file into a string

    Input: file name

    Returns: str
    """
    try:
        contents = ''
        with open(os.path.join(os.getcwd(), file_path)) as file:
            contents = file.read().splitlines()
    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        return contents 


def compute_probability(text: str, unigram_dict: dict, bigram_dict: dict, V: int) -> int:
    """Probability that given text is either in English, French, or Italian

    Input: string of text, dict of train unigrams, dict of train bigrams, total number of tokens

    Returns: computed probability as int
    """
    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_laplace = 1

    for bigram in bigrams_test:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        p_laplace = p_laplace * ((b + 1) / (u + V))
        
    return p_laplace


def write_likely_lang_to_file(english_prob: int, french_prob: int, italian_prob: int, line_num: int) -> None:
    """Helper function to write the most likely language to a file 'LangId.computed.out'

    Input: probability that text was English, probability that text was French, probability that text was Italian

    Returns: None
    
    Side-effect: if 'LangId.computed.out' is not created,
                    create 'LangId.computed.out'
                 then append to that file
    """
    most_likely_language = ''
    max_prob = max(english_prob, french_prob, italian_prob)
    if max_prob == english_prob:
        most_likely_language = 'English\n'
    elif max_prob == french_prob:
        most_likely_language = 'French\n'
    else:
        most_likely_language = 'Italian\n'

    with open('LangId.computed.out', 'a') as file:
        file.write(str(line_num) + ' ')
        file.write(most_likely_language)


def compute_accuracy() -> int:
    """Computes the accuracy of the model based on the 'LandId.sol' file
    
    Input: None

    Returns: accuracy as int
    """
    test_contents = ''
    with open('LangId.computed.out') as test_file:
        test_contents = test_file.read().splitlines()

    solution_contents = ''
    with open('data/LangId.sol') as solution_file:
        solution_contents = solution_file.read().splitlines()
        
    total_count = len(test_contents)
    line_num = 1
    num_correct = 0
    for test_line, solution_line in zip(test_contents, solution_contents):
        if test_line == solution_line:
            num_correct = num_correct + 1
        else:
            print('incorrect line: ', line_num)
        line_num = line_num + 1

    return (num_correct / total_count)
    

if __name__ == "__main__":
    english_pickle_unigram = pickle.load(open('data/LangId.train.English.unigram.p', 'rb'))
    english_pickle_bigram = pickle.load(open('data/LangId.train.English.bigram.p', 'rb'))

    french_pickle_unigram = pickle.load(open('data/LangId.train.French.unigram.p', 'rb'))
    french_pickle_bigram = pickle.load(open('data/LangId.train.French.bigram.p', 'rb'))
 
    italian_pickle_unigram = pickle.load(open('data/LangId.train.Italian.unigram.p', 'rb'))
    italian_pickle_bigram = pickle.load(open('data/LangId.train.Italian.bigram.p', 'rb'))
    
    total_vocab = len(english_pickle_unigram) + len(french_pickle_unigram) + len(italian_pickle_unigram)
    test_contents = parse_text_file_into_str('data/LangId.test')
    
    for index, line in enumerate(test_contents):
        english_prob = compute_probability(line, english_pickle_unigram, english_pickle_bigram, total_vocab)

        french_prob = compute_probability(line, french_pickle_unigram, french_pickle_bigram, total_vocab)

        italian_prob = compute_probability(line, italian_pickle_unigram, italian_pickle_bigram, total_vocab)
        
        write_likely_lang_to_file(english_prob, french_prob, italian_prob, index + 1)
        
    print('accuracy: ', compute_accuracy())