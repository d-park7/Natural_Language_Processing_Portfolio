import sys
import re
import argparse 
import csv
import os


class Person:
    """Person with first, last name and other..."""

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first 
        self.mi = mi
        self.id = id 
        self.phone = phone 
        
    def display(self):
        print(f"Employee list:\n\nEmployee id: {self.id}\n\t{self.first} {self.mi} {self.last}\n\t{self.phone}")


def parse_args():
    parser = argparse.ArgumentParser(description="Read csv file")
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        required=False,
        help="Name of csv file"
    )
    args = parser.parse_args()
    return args


# TOOD: change to dict of lines using file.read().splitlines()
# separate the functionality to separate functions
#  1: parse the csv into a dict
#  2: other remaining functionality
def user_parse_csv(filepath: str):
    try:
        with open(os.path.join(os.getcwd(), filepath), encoding="utf-8-sig") as file:
            dict_of_lines = file.read().splitlines()
            print("dict of lines: ", dict_of_lines)
            csv_reader = csv.reader(file, delimiter=',')
            print(csv_reader)
            line_count = 0
            
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    row[0] = row[0].capitalize()
                    row[1] = row[1].capitalize()
                    if not row[2]:
                        row[2] = 'X'
                    else:
                        row[2] = row[2].upper()

                    print(f"last name: {row[0]}")
                    print(f"first name: {row[1]}")
                    print(f"MI: {row[2]}")
                    
                    if not check_id(row[3]):
                        change_id(row[3])

                    line_count += 1

    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def check_id(id: str):
    regex_match = re.match(r"[a-z]{2}[0-9]{4}$", id, re.IGNORECASE)
    if not regex_match:
        print("ID invalid: {id}")
        print("ID is two letters followed by 4 digits")
        change_id()


def change_id(id: str):
    return


if __name__ == '__main__':
    #process_csv('data/data.csv')
    args = parse_args()
    user_parse_csv(args.file_name)

    person = Person('Doe', 'John', 'R', 9, '123-123-1231')
    person.display()