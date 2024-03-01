
class Retriever:

    #pass in inverted-index for comparison
    def __init__(self, index):
        self.invertedIndex = index

    #individual query token acquisition    
    def getQueryTokens(self):
        query = input("Enter Query:")
        queryTokens = self.tokenize(query)
        return queryTokens

    #tokenize method from indexConstruction
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

    #loop repeatedly taking queries until 'quit'
    def retrieve(self):
        queryTag = True
        while queryTag:
            query = self.getQueryTokens()
            if query[0] == 'quit':
                break
            print(query)

    #currently unfinished--indexes based of AND'ing the terms in query with corresponding terms in index
    def findTokenCounts(self):
        #prints empty dictionary
        print(self.invertedIndex)
