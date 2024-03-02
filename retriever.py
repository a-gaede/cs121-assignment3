import json
from functools import reduce


class Retriever:

    # pass in inverted-index for comparison
    def __init__(self, index, docMap):
        with open(index, 'r') as indexFile:
            self.invertedIndex = json.load(indexFile)
        with open(docMap, 'r') as docMapFile:
            self.docMapping = json.load(docMapFile)

    # individual query token acquisition
    def getQueryTokens(self):
        query = input("Enter Query:")
        queryTokens = self.tokenize(query)
        return queryTokens

    # tokenize method from indexConstruction
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

    # loop repeatedly taking queries until 'quit'
    def retrieve(self):
        queryTag = True
        while queryTag:
            query = self.getQueryTokens()
            if query[0] == 'quit':
                break
            print(query)
            results = self.findTokenCounts(query)
            if len(results) == 0:
                print("No results")
                continue
            for docID in results:
                print(self.docMapping[str(docID)])

    # Does AND operation
    def findTokenCounts(self, queryTokens):
        found = []

        if len(queryTokens) == 1:
            if queryTokens[0] in self.invertedIndex:
                found = self.invertedIndex[queryTokens[0]][0]
        else:
            for query in queryTokens:
                if query in self.invertedIndex:
                    found.append(self.invertedIndex[query][0])
            if len(found) != 0:
                found = list(reduce(set.intersection, map(set, found)))

        if len(found) >= 5:
            return found[:5]
        else:
            return found
