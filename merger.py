import json
import os


class Merger:
    def __init__(self):
        self.merged_index = {}
        self.merged_dir = "./reports/MergedIndexReports"

    def merge(self):
        # If no folder exists for a merged index, create one.
        if not os.path.exists(self.merged_dir):
            os.makedirs(self.merged_dir)

        # Directory with unsorted Inverted index
        dirpath = "./reports/InvertedIndexReports"

        files = os.listdir(dirpath)
        total = len(files)
        count = 1

        for i in range(len(files)):
            print(f"Merging {count} / {total}")
            file = json.load(open(dirpath + "/" + files[i], "r", encoding="utf-8"))
            for value in file.keys():
                letter = value[0]

                if not (letter.islower() or letter.isdigit()):
                    continue

                # If the file doesn't already exist, create it.
                if not os.path.exists(
                    f"./reports/MergedIndexReports/Index-{letter}.json"
                ):
                    open(f"./reports/MergedIndexReports/Index-{letter}.json", "w+")

                # Read in the old version of the report
                with open(
                    f"./reports/MergedIndexReports/Index-{letter}.json", "r+"
                ) as outfile:
                    try:
                        curr = json.load(
                            outfile
                        )  # Load the current file for this character
                    except:
                        curr = {}  # If it's not readable, assume it's empty

                    # Check to see if this term has already been added.
                    if not value in curr.keys():
                        curr[value] = file[value]

                    # If it is already in the dict, compare the lists of values
                    else:
                        # Check if values are same
                        if curr[value] == file[value]:
                            pass
                        # If two different lists, merge them
                        else:

                            # Append new values into current dictionary
                            for i in file[value]:

                                # Check for duplicates
                                if i not in curr[value]:
                                    curr[value].append(i)

                    # Write new version of report
                    with open(
                        f"./reports/MergedIndexReports/Index-{letter}.json", "w+"
                    ) as outfile:
                        json.dump(curr, outfile)

            count += 1


if __name__ == "__main__":
    m = Merger()
    m.merge()
