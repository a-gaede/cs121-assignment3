import ujson
import os
import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import defaultdict
from urllib.parse import urlparse

"""
FIELD WEIGHTS

1: p
2: b and strong
3: h6
4: h5
5: h4
6: h3
7: h2
8: h1
9: title

"""


class InvertedIndex:
    def __init__(self):
        # Dictionary to hold postings
        self.invertedIndex = defaultdict(list)
        # Holds number of indexed documents
        self.indexedDocuments = 0
        # Holds mapping for docIDs
        self.docMapping = {}
        # Batch size
        self.batchSize = 2
        # File counter
        self.fileCounter = 1
        # Batch counter
        self.batchCounter = 1
        # Stemmer
        self.stemmer = PorterStemmer()
        # Count for IDs
        self.count = 1

    """OPEN FILE AND GET TEXT"""

    # Open HTML json file
    def openHTML(self, path):
        with open(path, "r") as HTMLjson:
            data = ujson.load(HTMLjson)

        return data

    # Get HTML text
    def getText(self, dataContent):
        if dataContent.strip():
            soup = BeautifulSoup(dataContent, "html.parser")
            text = {
                1: [
                    self.stemTokens(self.tokenize(p.get_text()))
                    for p in soup.find_all("p")
                ],
                2: [
                    self.stemTokens(self.tokenize(bold.get_text()))
                    for bold in soup.find_all(["b", "strong"])
                ],
                3: [
                    self.stemTokens(self.tokenize(h6.get_text()))
                    for h6 in soup.find_all("h6")
                ],
                4: [
                    self.stemTokens(self.tokenize(h5.get_text()))
                    for h5 in soup.find_all("h5")
                ],
                5: [
                    self.stemTokens(self.tokenize(h4.get_text()))
                    for h4 in soup.find_all("h4")
                ],
                6: [
                    self.stemTokens(self.tokenize(h3.get_text()))
                    for h3 in soup.find_all("h3")
                ],
                7: [
                    self.stemTokens(self.tokenize(h2.get_text()))
                    for h2 in soup.find_all("h2")
                ],
                8: [
                    self.stemTokens(self.tokenize(h1.get_text()))
                    for h1 in soup.find_all("h1")
                ],
                9: [
                    self.stemTokens(self.tokenize(title.get_text()))
                    for title in soup.find_all("title")
                ],
            }

            # Flattening the nested lists
            for key in text:
                text[key] = [item for sublist in text[key] for item in sublist]

            self.indexedDocuments += 1

            return text
        else:
            return None

    """TOKENIZE AND STEM"""

    # Tokenize text
    def tokenize(self, text):
        tokens = []
        token = ""
        for char in text.lower():
            # Check if an english alphabet character or number
            if 97 <= ord(char) <= 122 or char.isnumeric():
                token += char
            else:
                if token:
                    tokens.append(token)
                    token = ""

        return tokens

    # Stem tokens
    def stemTokens(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

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

    # Calculate term frequency scores within document
    def computeTermFrequencyScores(self, tokens):
        frequencies = self.computeFrequencies(tokens)
        totalTokens = sum(frequencies.values())
        return {token: freq / totalTokens for token, freq in frequencies.items()}

    # Add to dictionary in format
    # token: [[posting1], [posting2], [posting3], etc...]
    # where posting is in format
    # [docID, field, frequency]
    def computePostings(self, documentID, field, termFrequencies):
        for token, freq in termFrequencies.items():
            self.invertedIndex[token].append([documentID, field, freq])

    # CHECK URL VALID
    def isValid(self, URL):
        parsed = urlparse(URL)
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|txt"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|ppsx"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|odc)$",
            parsed.path.lower(),
        )

    # Add the postings to the index given file
    def index(self, dirPath, fileName, dataID):
        data = self.openHTML(dirPath + "/" + fileName)
        dataContent = data["content"]
        URL = data["url"]

        if self.isValid(URL):
            print(f"Processing doc {self.count}")
            self.docMapping[dataID] = URL

            tokens = self.getText(dataContent)
            if tokens != None:
                termFrequencies = {}

                for field in tokens:
                    termFrequencies[field] = self.computeTermFrequencyScores(
                        tokens[field]
                    )

                    self.computePostings(dataID, field, termFrequencies[field])

            self.count += 1
            self.fileCounter += 1

    def createBatchIndexes(self, dirPath, fileNames, count):
        if self.fileCounter >= (self.batchSize):
            self.index(dirPath, fileNames, count)
            self.writeIIBatchesToJson(self.batchCounter)
            self.invertedIndex = defaultdict(list)
            self.fileCounter = 1
            self.batchCounter += 1
        else:
            self.index(dirPath, fileNames, count)

    """CREATE OUTPUT FILES"""

    # Create json of inverted index
    def writeIIBatchesToJson(self, batchNumber):
        jsonStructure = {
            token: [(docID, field, freq) for docID, field, freq in postings]
            for token, postings in self.invertedIndex.items()
        }

        with open(
            f"reports/InvertedIndexReports/IIBatch{batchNumber}.json", "w"
        ) as invertedIndexJson:
            ujson.dump(jsonStructure, invertedIndexJson)

    def writeDocMapping(self):
        with open("reports/docMapping.json", "w") as docMapping:
            ujson.dump(self.docMapping, docMapping)

    def writeTotalDocsIndexed(self):
        with open("reports/docsIndexed.txt", "w") as docsIndexed:
            docsIndexed.write(str(self.indexedDocuments))

    def start(self, ROOT):
        for dirPath, _, fileNames in os.walk(ROOT):
            for fileName in fileNames:
                self.createBatchIndexes(dirPath, fileName, self.count)

        if self.invertedIndex:
            self.writeIIBatchesToJson(self.batchCounter)
        self.writeDocMapping()
        self.writeTotalDocsIndexed()


if __name__ == "__main__":
    ROOT = r"test"
    InvertedIndex = InvertedIndex()
    InvertedIndex.start(ROOT)
