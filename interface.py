import tkinter as tk
from retriever import Retriever


def run():
    window = tk.Tk()
    window.geometry("600x200")

    label = tk.Label(text="Search")
    entry = tk.Entry(width=50)

    label.pack()
    entry.pack()
    # Put path of merged index reports
    invertedIndexPath = "reports/MergedIndexReports"
    # Put path of number of docs indexed
    indexedNumFile = "reports/docsIndexed.txt"
    # Put path of docID mapping
    docMapping = "reports/docMapping.json"

    retriever = Retriever(invertedIndexPath, indexedNumFile, docMapping)

    global displayLabel

    displayLabel = tk.Label()

    def search():
        global displayLabel
        displayString = ""
        displayLabel.destroy()
        search = entry.get()
        tokens = retriever.getQueryTokens(interfaceQuery=search)
        merged = retriever.computeMergedPostings(tokens)
        ANDPostings = retriever.computeAND(merged)
        scores = retriever.computeScores(ANDPostings)
        sortedScores = dict(
            sorted(scores.items(), key=lambda item: item[0], reverse=True)
        )
        if len(scores) > 5:
            sortedScores = dict(
                sorted(scores.items(),
                       key=lambda item: item[0], reverse=True)[:5]
            )

        for score in sortedScores:
            displayString += f"{retriever.docMap[str(sortedScores[score])]}\n"

        displayLabel = tk.Label(text=displayString)
        displayLabel.pack()

    enterButton = tk.Button(window, text="Enter", command=search)
    enterButton.pack()

    window.mainloop()


if __name__ == "__main__":
    run()
