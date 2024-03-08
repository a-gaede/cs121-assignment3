import json
import os
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


class InvertedIndex:
    def __init__(self):
        self.invertedIndex = {}
        self.docMapping = {}

    """OPEN FILE AND GET TEXT"""

    # Open HTML json file
    def openHTML(self, path):
        with open(path, 'r') as HTMLjson:
            data = json.load(HTMLjson)

        return data

    # Get HTML text
    def getText(self, dataContent):
        soup = BeautifulSoup(dataContent, 'html.parser')
        text = {
            'p': ' '.join([p.get_text() for p in soup.find_all('p')]),
            'bold': ' '.join([bold.get_text() for bold in soup.find_all(['b', 'strong'])]),
            'h1': ' '.join([h1.get_text() for h1 in soup.find_all('h1')]),
            'h2': ' '.join([h2.get_text() for h2 in soup.find_all('h2')]),
            'h3': ' '.join([h3.get_text() for h3 in soup.find_all('h3')]),
            'h4': ' '.join([h4.get_text() for h4 in soup.find_all('h4')]),
            'h5': ' '.join([h5.get_text() for h5 in soup.find_all('h5')]),
            'h6': ' '.join([h6.get_text() for h6 in soup.find_all('h6')]),
            'title': ' '.join([title.get_text() for title in soup.find_all('title')])
        }

        return text

    """TOKENIZE AND STEM"""

    # Tokenize text
    def tokenize(self, text):
        tokens = []
        token = ""
        for char in text.lower():
            if char.isalpha():
                token += char
            else:
                if token:
                    tokens.append(token)
                    token = ""
        if token:
            tokens.append(token)
        return tokens

    # Stem tokens
    def stem(self, tokens):
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]

        return tokens

    """PERFORM TEXT PROCESSING TASKS ON HTML CONTENT"""

    # Process
    def textProcessing(self, dataContent):
        text = self.getText(dataContent)
        tokens = {}

        for field in text:
            fieldTokens = self.tokenize(text[field])
            stemmedFieldTokens = self.stem(fieldTokens)
            tokens[field] = stemmedFieldTokens

        return tokens

    """CREATE POSTINGS AND CREATE INDEX"""

    # Calculate term frequency within document
    def computeFrequencies(self, tokens):
        documentTokenFrequency = {}
        for token in tokens:
            if token not in documentTokenFrequency:
                documentTokenFrequency[token] = 1
            else:
                documentTokenFrequency[token] += 1

        return documentTokenFrequency

    # Add to dictionary in format
    # token: [[posting1], [posting2], [posting3], etc...]
    # where posting is in format
    # [docID, field, frequency]
    def computePostings(self, documentID, field, frequencies):
        for token in frequencies:
            if token in self.invertedIndex:
                self.invertedIndex[token].append(
                    [documentID, field, frequencies[token]])
            else:
                self.invertedIndex[token] = [
                    [documentID, field, frequencies[token]]]

    # Add the postings to the index given file
    def index(self, dirPath, fileName, count):
        data = self.openHTML(dirPath + "/" + fileName)
        dataContent = data['content']
        URL = data['url']
        dataID = count

        self.docMapping[dataID] = URL

        tokens = self.textProcessing(dataContent)
        frequencies = {}

        for field in tokens:
            frequencies[field] = self.computeFrequencies(tokens[field])

        for field in frequencies:
            self.computePostings(
                dataID, field, frequencies[field])


if __name__ == "__main__":
    # ADD YOUR DIRECTORY ROOT HERE FOR YOUR WEBPAGES
    ROOT = r"test"
    count = 0
    InvertedIndex = InvertedIndex()
    for dirPath, _, fileNames in os.walk(ROOT):
        for fileName in fileNames:
            count += 1
            print(f'Processing Doc {count}')
            InvertedIndex.index(dirPath, fileName, count)
            break

    print(InvertedIndex.invertedIndex)
