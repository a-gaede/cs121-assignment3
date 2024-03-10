import json
import math
from nltk.stem import PorterStemmer
from collections import defaultdict


class Retriever:

    # pass in inverted-index directory and doc map for comparison
    def __init__(self, path, totalNum, docMapping):
        self.stemmer = PorterStemmer()
        self.invertedIndexPath = path
        with open(totalNum, "r") as total:
            self.total = int(total.read())
        with open(docMapping, "r") as docMapFile:
            self.docMap = json.load(docMapFile)

    # individual query token acquisition
    def getQueryTokens(self, interfaceQuery=None):
        if interfaceQuery:
            query = interfaceQuery
        else:
            query = input("Enter Query: ")
        return [self.stemmer.stem(word) for word in query.split()]

    def computeMergedPostings(self, tokens):
        mergedPostings = {}
        for token in tokens:
            with open(f"{self.invertedIndexPath}/Index-{token[0]}.json") as II:
                data = json.load(II)
                if token in data:
                    mergedPostings[token] = data[token]

        return dict(sorted(mergedPostings.items(), key=lambda item: len(item[1])))

    # Return dict of the lowest term in format
    # docID : postings
    def computeLowestPostings(self, lowest):
        lowestPostings = {}
        for post in lowest:
            docID = post[0]
            if docID in lowestPostings:
                lowestPostings[docID].append(post)
            else:
                lowestPostings[docID] = [post]

        return lowestPostings

    # Return dict of AND terms in format
    # doc ID : postings
    def computeAND(self, merged):
        if merged:
            # Term with lowest document frequency
            lowest = min(merged, key=lambda term: len(merged[term]))
            # Get the docIDs from lowest
            docIDs = {post[0] for post in merged[lowest]}
            # Store AND posts
            ANDPostings = self.computeLowestPostings(merged[lowest])

            for token in list(merged.keys())[1:]:
                for post in merged[token]:
                    if post[0] in docIDs:
                        ANDPostings[post[0]].append(post)

            return ANDPostings
        return {}

    def computeTFIDF(self, post, df):
        return (post[1] + post[2]) * math.log10(self.total / df)

    # Scores are computed as follows
    # (FIELD WEIGHT + log(tf)) * log(N / df)
    def computeScores(self, postings):
        scores = defaultdict(int)

        for docID in postings:
            df = len(postings[docID])
            scores[docID] = sum(
                [self.computeTFIDF(post, df) for post in postings[docID]]
            )

        uniqueScores = {v: k for k, v in scores.items()}

        return uniqueScores

    # Retrieves results for one query
    def retrieve(self,query):
        tokens = [self.stemmer.stem(word) for word in query.split()]
        merged = self.computeMergedPostings(tokens)
        ANDPostings = self.computeAND(merged)
        scores = self.computeScores(ANDPostings)
        if len(scores) == 0:
            return "No results"

        results =  "Results:" + f"#\tScore\tURL"

        sortedScores = dict(
            sorted(scores.items(), key=lambda item: item[0], reverse=True)
        )
        if len(scores) > 5:
            sortedScores = dict(
                sorted(scores.items(),
                        key=lambda item: item[0], reverse=True)[:5]
            )
        for i, score in enumerate(sortedScores):
            results += f"\n{i+1}\t{round(score)}\t{self.docMap[str(sortedScores[score])]}"
        return results
