import json
import os
from stemmer import PorterStemmer
from bs4 import BeautifulSoup


# Class for Inverted Index
class InvertedIndex:
  def __init__(self):
    # Dictionary to hold postings
    self.invertedIndex = {}
    # Holds number of indexed documents
    self.indexedDocuments = 0

  # Tokenize text
  def tokenize(self, text):
    stemmer = PorterStemmer()
    tokens = []
    token = ""
    for char in text.lower():
        if char.isalpha():
            token += char
        else:
            if token:
                stemmer.stem(token)
                tokens.append(token)
                token = ""
    if token:
        stemmer.stem(token)
        tokens.append(token)
    return tokens

  # Add to dictionary in format 
  # token: [{document URLs}, token frequency]
  def computePostings(self, tokens, documentID):
      for token in tokens:
          if token in self.invertedIndex:
            self.invertedIndex[token][0].add(documentID)
            self.invertedIndex[token][1] += 1
          else:
            self.invertedIndex[token] = [{documentID}, 1]
    
  # Open HTML json file
  def openHTML(self, path):
    with open(path, 'r') as HTMLjson:
      data = json.load(HTMLjson)
      
    return data

  # Get HTML text
  def getText(self, dataContent):
    soup = BeautifulSoup(dataContent, 'html.parser')
    text = soup.get_text()
    
    self.indexedDocuments += 1
    
    return text
  
  # Helper function to get index
  def getInvertedIndex(self):
    return self.invertedIndex
  
  # Add the postings to the index given file
  def createPostings(self, dirPath, fileName, count):
      data = self.openHTML(dirPath + "/" + fileName)
      dataContent = data['content']
      dataID = count
      
      text = self.getText(dataContent)
      tokens = self.tokenize(text)
      
      self.computePostings(tokens, dataID)
      
  # Create report file of index
  def writeDataFile(self):
    with open('reports/InvertedIndexReport.txt', 'w', encoding='utf-8') as InvertedIndexReport:
        for token in self.invertedIndex:
          InvertedIndexReport.write(f"{token}\n\tFound in: {self.invertedIndex[token][0]}\n\tFrequency: {self.invertedIndex[token][1]}\n")
          
  # Create report file of unique tokens
  def writeTokensFile(self):
    with open('reports/TokenReport.txt', 'w') as TokenReport:
      TokenReport.write(f'{len(self.invertedIndex)} unique words.')
      
  def writeNumberIndexedFile(self):
    with open('reports/NumberIndexed.txt', 'w') as NumberReport:
      NumberReport.write(f'{self.indexedDocuments} total indexed documents')

if __name__ == "__main__":
  InvertedIndex = InvertedIndex()
  
  # ADD YOUR DIRECTORY ROOT HERE FOR YOUR WEBPAGES
  ROOT = "/Users/Jaelyn/Downloads/DEV"
  count = 0
  for dirPath, _, fileNames in os.walk(ROOT):
    for fileName in fileNames:
      count+=1
      InvertedIndex.createPostings(dirPath, fileName, count)
      print(f'Processing {count}')
  InvertedIndex.writeDataFile()
  InvertedIndex.writeTokensFile()
  InvertedIndex.writeNumberIndexedFile()
