#using OOP API, data stored in Library and Book objects

from collections import defaultdict
from string import punctuation

from flask import Flask

class Library(object):
    def __init__(self, _input):
        self.input = _input
        self.book_chunks = _input.split('\n\n')
        self.books = []
        self.index = defaultdict(list)

        for book in self.book_chunks:
            if book:
                book_obj = Book(book)
                self.books.append(book_obj)

                for word in book_obj.words():
                    self.index[word].append(book_obj)

    def search(self, keyword):
        return self.index[keyword]

class Book(object):
    def __init__(self, book_chunk):
        self.chunk = book_chunk.splitlines()
        self.attrib = {}

        for i, line in enumerate(self.chunk):
            if line:
                if i == 0:
                    self.attrib['title'] = line.split('TITLE: ')[1]
                elif i == 1:
                    self.attrib['author'] = line.split('AUTHOR: ')[1]
                elif i == 2:
                     self.attrib['synopsis'] = line.split('SYNOPSIS: ')[1]
                else:
                    self.attrib['synopsis'] += ' ' + line

    def words(self):
        words = set()
        clean = [words.update(s.lower().translate(None, punctuation).split()) for s in self.attrib.values()]

        return words

def __getattr__(self, name):
    return self.attrib[name]

try_objects = Flask(__name__)

string = open('test.txt','r').read()
library = Library(string)

@try_objects.route('/')
def index():
    result = []
    for book in library.books:
        result.append(book.attrib)

    return str(result)

@try_objects.route('/search/<word>')
def searched(word):
    books = library.search(word)
    result = []
    for book in books:
        result.append(book.attrib)

    return str(result)


if __name__ == '__main__':
    try_objects.run(debug=True)
