from nltk import word_tokenize
import re
import argparse

def parse_args():
    """Parses through the system arguments that user provides
    Using argparse allows more informative descriptions and is a more specified use case
    rather than sys
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
    try:
        with open(file_name) as file:
            contents = file.read()
    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        return contents


def normalize_text(text: str) -> str:
    text = re.sub(r'[.?!,:;()\-\n\d]',' ', text.lower())
    tokens = word_tokenize(text)
    return tokens


def calc_lexical_diversity(text: str):
    text = word_tokenize(text)
    return len(text) / len(set(text))


if __name__ == "__main__":
    args = parse_args()
    contents = parse_text_file(args.file_name)
    print(contents)
    lexical_diversity = calc_lexical_diversity(contents)
    tokens = normalize_text(contents)
    print(lexical_diversity)