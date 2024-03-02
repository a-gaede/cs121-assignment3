from retriever import Retriever

if __name__ == "__main__":
    # Put path of index file
    invertedIndexFile = 'reports\invertedIndex.json'
    # Put path of docID mapping file
    docMapping = 'reports\docMapping.json'
    retriever = Retriever(invertedIndexFile, docMapping)
    retriever.retrieve()
