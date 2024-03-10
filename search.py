from retrieve_one import Retriever

def Search(query):
    # Put path of merged index reports
    invertedIndexPath = "reports/MergedIndexReports"
    # Put path of number of docs indexed
    indexedNumFile = "reports/docsIndexed.txt"
    # Put path of docID mapping
    docMapping = "reports/docMapping.json"

    retriever = Retriever(invertedIndexPath, indexedNumFile, docMapping)
    return retriever.retrieve(query)

if __name__ == "__main__":
    query = input("Enter Query: ")
    results = Search(query)
    print(results)