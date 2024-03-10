import ijson
import os
import ujson as json


def isValidKey(key):
    # Check if the first character of the key is a letter (a-z, A-Z) or a digit (0-9)
    return key[0].isascii() and (key[0].isalpha() or key[0].isdigit())


def mergeJsonsIncremental(inputFolder, outputFolder):
    mergedData = {}
    for filename in os.listdir(inputFolder):
        if filename.endswith(".json"):
            with open(os.path.join(inputFolder, filename), "rb") as f:
                print(f"Processing file {filename}")
                objects = ijson.items(f, "")
                for obj in objects:
                    for key, value in obj.items():
                        mergedData.setdefault(key, []).extend(value)

    # Split merged data based on the first letter of the keys
    splitData = {}
    for key, value in mergedData.items():
        if isValidKey(key):  # Check if the key is valid
            firstLetter = key[0].lower()
            splitData.setdefault(firstLetter, {}).update({key: value})

    # Write split data to separate JSON files
    for firstLetter, data in splitData.items():
        outputFile = os.path.join(outputFolder, f"Index-{firstLetter}.json")
        with open(outputFile, "w") as f:
            json.dump(data, f)
        print(f"Wrote {outputFile}")

    print("Merge and split process completed.")


if __name__ == "__main__":
    # Path to the folder containing the JSON files
    inputFolder = 'reports/InvertedIndexReports'

    # Path to the output folder
    outputFolder = 'reports/MergedIndexReports'

    # Run the function
    mergeJsonsIncremental(inputFolder, outputFolder)
