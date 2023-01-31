import pickle
import re
import argparse 
import csv
import os


class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first 
        self.mi = mi
        self.id = id 
        self.phone = phone 
        
    def display(self):
        print(f"\nEmployee id: {self.id}\n\t{self.first} {self.mi} {self.last}\n\t{self.phone}")


def parse_args():
    """Parses through the system arguments that user provides
    Using argparse allows more informative descriptions and is a more specified use case
    rather than sys
    """
    parser = argparse.ArgumentParser(description="Read multiple People objects from csv file")
    parser.add_argument(
        "-f",
        "--file_name",
        type=str,
        required=True,
        help="Name of csv file"
    )
    args = parser.parse_args()
    return args


def parse_csv_into_dict(filepath: str):
    """Parses a csv file of Person objects into a dictionary of Person objects
    
    Input string must be path to csv file
    
    Returns:
        dict: {Person.id: Person object}
        or
        empty dict
    """
    person_dict = {}
    try:
        with open(os.path.join(os.getcwd(), filepath), encoding="utf-8") as file:
            csv_reader = csv.reader(file, delimiter=',')
            line_count = 0
            
            for row in csv_reader:
                last_name = row[0]
                first_name = row[1]
                middle_initial = row[2]
                id = row[3]
                phone = row[4]

                if line_count == 0:
                    line_count += 1
                else:
                    last_name = last_name.capitalize()
                    first_name = first_name.capitalize()

                    if not middle_initial:
                        middle_initial = 'X'
                    else:
                        middle_initial = middle_initial.upper()

                    while not is_correct_id(id):
                        id = input("Please enter a valid id: ")
                    while not is_correct_phone(phone):
                        phone = input("Enter phone number: ")

                    new_person = Person(last=last_name, first=first_name, mi=middle_initial, id=id, phone=phone)
                    person_dict.update({id: new_person})
                    line_count += 1

    # catching path file naming errors
    except OSError as err:
        print("OS error:" , err)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    finally:
        return person_dict
    

def is_correct_id(id: str):
    regex_match = re.match(r"[a-z]{2}[0-9]{4}$", id, re.IGNORECASE)
    if not regex_match:
        print(f"ID invalid: {id}")
        print("ID is two letters followed by 4 digits")
        return False
    return True


def is_correct_phone(phone: str):
    regex_match = re.match(r"[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone)
    if not regex_match:
        print(f"Phone {phone} is invalid")
        print("Enter phone number in form 123-456-7890")
        return False
    return True


if __name__ == '__main__':
    args = parse_args()
    person_dict = parse_csv_into_dict(args.file_name)

    pickle.dump(person_dict, open("data/people.p", "wb"))
    pickle_dict = pickle.load(open("data/people.p", "rb"))

    print("\n\nEmployee list:")
    for person in pickle_dict:
        pickle_dict[person].display()
