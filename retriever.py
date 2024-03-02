import json
from functools import reduce


class Retriever:

    # pass in inverted-index for comparison
    def __init__(self, index):
        #print("index is:",index)
        with open(index, 'r') as indexFile:
            self.invertedIndex = json.load(indexFile)

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
            if query[0] == 'quit' or query[0] == 'q' or query[0] == 'exit':
                break
            print(query)
            for url in self.findTokenCounts(query):
                print(url)

    # Does AND operation
    def findTokenCounts(self, queryTokens):
        found = []

        if len(queryTokens) == 1:
            try:
                found = self.invertedIndex[queryTokens[0]][0]
            except:
                print('"'+queryTokens[0]+'"', 'not found.')
        else:
            for query in queryTokens:
                try:
                    found.append(self.invertedIndex[query][0])
                except:
                    print('"'+query+'"', 'not found.')
            
            # Make sure that at least one term searched for is found
            if len(found) >= 1:
                found = reduce(set.intersection, map(set, found))

        if len(found) >= 5:
            return list(found)[:5] # Cast it as a list to avoid issues with sets
        else:
            return found
