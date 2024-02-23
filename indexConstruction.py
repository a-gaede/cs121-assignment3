import json
import os
from bs4 import BeautifulSoup

class InvertedIndex:
  def __init__(self):
    self.invertedIndex = {}

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

  def computePostings(self, tokens, documentID):
      for token in tokens:
          if token in self.invertedIndex:
            self.invertedIndex[token][0].add(documentID)
            self.invertedIndex[token][1] += 1
          else:
            self.invertedIndex[token] = [{documentID}, 1]
    
  def openHTML(self, path):
    with open(path, 'r') as HTMLjson:
      data = json.load(HTMLjson)
      
    return data

  def getText(self, dataContent):
    soup = BeautifulSoup(dataContent, 'html.parser')
    text = soup.get_text()
    
    return text
  
  def getInvertedIndex(self):
    return self.invertedIndex
  
  def createPostings(self, dirPath, fileName):
      data = self.openHTML(dirPath + "/" + fileName)
      dataContent = data['content']
      dataID = data['url']
      
      text = self.getText(dataContent)
      tokens = self.tokenize(text)
      
      self.computePostings(tokens, dataID)
      
  def writeDataFile(self):
    with open('reports/InvertedIndexReport.txt', 'w', encoding='utf-8') as InvertedIndexReport:
        for token in self.invertedIndex:
          InvertedIndexReport.write(f"{token}\n\tFound in: {self.invertedIndex[token][0]}\n\tFrequency: {self.invertedIndex[token][1]}\n")

if __name__ == "__main__":
  InvertedIndex = InvertedIndex()
  
  ROOT = "developer/DEV" 
  count = 0
  for dirPath, _, fileNames in os.walk(ROOT):
    for fileName in fileNames:
      count+=1
      InvertedIndex.createPostings(dirPath, fileName)
      print(f'Processing {count} of 32212')
  InvertedIndex.writeDataFile()
  
