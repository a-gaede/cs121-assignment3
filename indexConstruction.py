import json
import os
import math
from bs4 import BeautifulSoup
from tqdm import tqdm
# Class for Inverted Index


class InvertedIndex:
    def __init__(self):
        # Dictionary to hold postings
        self.invertedIndex = {}
        # Holds number of indexed documents
        self.indexedDocuments = 0
        # Holds mapping for docIDs
        self.docMapping = {}
        # Batch size
        self.batchSize = 500
        # File counter
        self.fileCounter = 0
        # Batch counter
        self.batchCounter = 1

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

    # Calculate term frequency within document
    def computeFrequencies(self, tokens):
        documentTokenFrequency = {}
        for token in tokens:
            if token not in documentTokenFrequency:
                documentTokenFrequency[token] = 1
            else:
                documentTokenFrequency[token] += 1

        return documentTokenFrequency

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

    # Get TF Score (number of times token appears in document / total number of tokens in document)
    def calculateTFScore(self, token, tokens):
        return tokens[token] / len(tokens)

    # Get IDF score (log of total number of documents / number of documents containing token)
    def calculateIDFScore(self, token):
        return math.log(self.indexedDocuments / len(self.invertedIndex[token]), 10)

    # TF multiplied by IDF
    def calculateTFIDFScore(self, tf, idf):
        return round(tf * idf, 5)

    # Compute intial posting with TF score
    def computeTFScorePostings(self, documentTokenFrequency, documentID):
        for token in documentTokenFrequency:
            if token in self.invertedIndex:
                self.invertedIndex[token].append(
                    ([documentID, self.calculateTFScore(token, documentTokenFrequency)]))
            else:
                self.invertedIndex[token] = [
                    [documentID, self.calculateTFScore(token, documentTokenFrequency)]]

    # Compute next posting with TFIDF score
    def computeTFIDFScorePostings(self):
        for token in self.invertedIndex:
            IDFScore = self.calculateIDFScore(token)
            for posting in self.invertedIndex[token]:
                posting[1] = self.calculateTFIDFScore(posting[1], IDFScore)

    # Compute full posting
    def computePostings(self, documentTermFrequency, documentID):
        self.computeTFScorePostings(documentTermFrequency, documentID)

    # Add the postings to the index given file

    def createPostings(self, dirPath, fileName, count):
        data = self.openHTML(dirPath + "/" + fileName)
        dataContent = data['content']
        URL = data['url']
        dataID = count

        self.docMapping[dataID] = URL

        text = self.getText(dataContent)
        tokens = self.tokenize(text)
        tokensFrequencies = self.computeFrequencies(tokens)

        self.computePostings(tokensFrequencies, dataID)

    def createBatchPostings(self, dirPath, fileNames, count):
        self.fileCounter += 1

        if self.fileCounter >= (self.batchSize):
            self.createPostings(dirPath, fileNames, count)
            self.writeIIBatchesToJson(self.batchCounter)
            self.invertedIndex = {}
            self.fileCounter = 0
            self.batchCounter += 1
        else:
            self.createPostings(dirPath, fileNames, count)

    # Create json of inverted index
    def writeIIBatchesToJson(self, batchNumber):
        self.computeTFIDFScorePostings()
        jsonStructure = {token: [(docID, freq) for docID, freq in postings]
                         for token, postings in self.invertedIndex.items()}

        with open(f'reports/InvertedIndexReports/IIBatch{batchNumber}.json', 'w', encoding='utf-8') as invertedIndexJson:
            json.dump(jsonStructure, invertedIndexJson)

    def writeDocMapping(self):
        with open('reports/docMapping.json', 'w', encoding='utf-8') as docMapping:
            json.dump(self.docMapping, docMapping)


if __name__ == "__main__":
    # ADD YOUR DIRECTORY ROOT HERE FOR YOUR WEBPAGES
    ROOT = r"data/DEV"
    InvertedIndex = InvertedIndex()
    for dirPath, _, fileNames in os.walk(ROOT):
        print("Processing:", dirPath)
        for i in tqdm(range(len(fileNames))):
            InvertedIndex.createBatchPostings(dirPath, fileNames[i], i)
    if InvertedIndex.invertedIndex:
        InvertedIndex.writeIIBatchesToJson(
            InvertedIndex.batchCounter)
    InvertedIndex.writeDocMapping()