import sys
import csv


class Person:
    """Person with first, last name and other..."""

    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first 
        self.mi = mi
        self.id = id 
        self.phone = phone 
        
    def display(self):
        return

# TODO: part 4
def process_csv(file_name: str):
        with open(file_name, encoding='utf-8-sig') as file:
            for line in file:
                


if __name__ == '__main__':
    process_csv('data.csv')

    person = Person('last', 'first', 'mi', 1, '123-123-1231')