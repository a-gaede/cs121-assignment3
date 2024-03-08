import json
import os
from stemmer import PorterStemmer
from docMapper import DocMapper
from bs4 import BeautifulSoup
from retriever import Retriever

# Class for Inverted Index


class InvertedIndex:
    def __init__(self):
        # Dictionary to hold postings
        self.invertedIndex = {}
        # Holds number of indexed documents
        self.indexedDocuments = 0

    # Tokenize text
    def tokenize(self, text):
        stemmer = PorterStemmer()
        tokens = []
        token = ""
        for char in text.lower():
            if char.isalpha():
                token += char
            else:
                if token:
                    try:
                        stemmer.stem(token)
                    except:
                        print("couldn't stem", token)
                    tokens.append(token)
                    token = ""
        if token:
            try:
                stemmer.stem(token)
            except:
                print("couldn't stem", token)
            tokens.append(token)
        return tokens

    # Add to dictionary in format
    # token: [{document URLs}, token frequency]
    def computePostings(self, tokens, documentID):
        for token in tokens:
            if token in self.invertedIndex:
                self.invertedIndex[token][0].add(documentID)
                self.invertedIndex[token][1] += 1
            else:
                self.invertedIndex[token] = [{documentID}, 1]

    # Open HTML json file
    def openHTML(self, path):
        with open(path, 'r') as HTMLjson:
            data = json.load(HTMLjson)

        return data

    # Get HTML text
    def getText(self, dataContent):
        soup = BeautifulSoup(dataContent, 'html.parser')
        text = soup.get_text()

        self.indexedDocuments += 1

        return text

    def getImportantText(self, dataContent):
        soup = BeautifulSoup(dataContent, 'html.parser')

        # Define tag priorities (weights)
        tag_priorities = {
            'title': 3,
            'h1': 2,
            'b': 1,
            'strong': 1,
            # anchor tag: 2
            # metadata keywords: 3
        }

        # Extracting meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})['content']

        # Initialize important_text
        important_text = {}

        # Add metadata keywords to important_text
        for keyword in meta_keywords.split(','):
            important_text[keyword.strip()] = 3

        # Add anchor tag keywords to important_text
        for anchor_tag in soup.find_all('a'):
            anchor_text = anchor_tag.get_text().strip()
            for word in anchor_text.split():
                if word not in important_text:
                    important_text[word] = 2

        # Extract remaining keywords along with associated tags
        for tag in soup.find_all(['title', 'h1', 'b', 'strong']):
            # Get tag name and associated text
            tag_name = tag.name
            tag_text = tag.get_text().strip()

            # Assign weight based on tag priority
            weight = tag_priorities.get(tag_name, 0)

            # Update important text with weighted tag text
            if weight > 0:
                for word in tag_text.split():
                    if word not in important_text:
                        important_text[word] = weight

        return important_text

    # Helper function to get index
    def getInvertedIndex(self):
        return self.invertedIndex

    # Add the postings to the index given file
    def createPostings(self, dirPath, fileName):
        docID = mapper.add_mapping(dirPath + "/" + fileName)
        data = self.openHTML(dirPath + "/" + fileName)
        dataContent = data['content']

        text = self.getText(dataContent)
        tokens = self.tokenize(text)

        self.computePostings(tokens, docID)

    # Create report file of index
    def writeDataFile(self):
        with open('reports/InvertedIndexReport.txt', 'w', encoding='utf-8') as InvertedIndexReport:
            for token in self.invertedIndex:
                InvertedIndexReport.write(
                    f"{token}\n\tFound in: {self.invertedIndex[token][0]}\n\tFrequency: {self.invertedIndex[token][1]}\n")

    # Create report file of unique tokens
    def writeTokensFile(self):
        with open('reports/TokenReport.txt', 'w') as TokenReport:
            TokenReport.write(f'{len(self.invertedIndex)} unique words.')

    def writeNumberIndexedFile(self):
        with open('reports/NumberIndexed.txt', 'w') as NumberReport:
            NumberReport.write(
                f'{self.indexedDocuments} total indexed documents')

        # Create json of inverted index
    def writeInvertedIndexToJson(self):
        jsonStructure = {token: [list(docUrls), frequency]
                         for token, (docUrls, frequency) in self.invertedIndex.items()}

        with open('reports/invertedIndex.json', 'w') as invertedIndexJson:
            json.dump(jsonStructure, invertedIndexJson)

    def runInvertedIndex(self, root):
        count = 0
        for dirPath, _, fileNames in os.walk(root):
            for fileName in fileNames:
                count += 1
                self.createPostings(dirPath, fileName)
                print(f'Processing {count}')
        self.writeDataFile()
        self.writeTokensFile()
        self.writeNumberIndexedFile()
        self.writeInvertedIndexToJson()


if __name__ == "__main__":
    InvertedIndex = InvertedIndex()
    mapping_file = "doc_mapping.json"
    mapper = DocMapper(mapping_file)

    # ADD YOUR DIRECTORY ROOT HERE FOR YOUR WEBPAGES
    ROOT = "./../../DEV"
    # InvertedIndex.runInvertedIndex(ROOT)
    retriever = Retriever(InvertedIndex.getInvertedIndex())
    retriever.retrieve()
    retriever.findTokenCounts()
