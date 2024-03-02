from retriever import Retriever

if __name__ == "__main__":
    # Put path of index file
    invertedIndexFile = 'reports\invertedIndex.json'
    retriever = Retriever(invertedIndexFile)
    retriever.retrieve()
