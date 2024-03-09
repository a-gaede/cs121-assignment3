from retriever import Retriever

if __name__ == "__main__":
    # Put path of merged index reports
    invertedIndexPath = "reports/MergedIndexReports"
    # Put path of number of docs indexed
    indexedNumFile = "reports/docsIndexed.txt"
    # Put path of docID mapping
    docMapping = "reports/docMapping.json"

    retriever = Retriever(invertedIndexPath, indexedNumFile, docMapping)
    retriever.retrieve()
