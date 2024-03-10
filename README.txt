CS 121 Assignment 3

Adam Gaede, agaede, 85001853 
Eric Eang, eange, 24275414 
Jack Weckerly-Healey, jweckerl, 92409850 
Jaelyn Tran, jaelynt1, 61716269

**TO RUN THE SEARCH ENGINE**

1. Start with indexConstruction.py and set your folder directory with the webpage files in ROOT. One thing you may want to change is self.batchSize 
depending on the size of your corpus. Once ready run indexConstruction.py. It should create the input and output directories for you. If not, manually 
create them in your directory following the naming conventions. indexConstruction.py may take some time to run. 
Alternatively you can download the UCI dev webpages for "reports/InvertedIndexReports" at the link below.

https://drive.google.com/drive/folders/1rduGMkGWX-vfYlmYL17NsMd7FTDBc4Z1?usp=sharing

**SKIP TO STEP 2 IF YOU DID NOT MANUALLY DOWNLOAD THE INDEX REPORTS**

Once you have downloaded it make sure you have the files in ./reports/InvertedIndexReports and then run merger.py.

2. To use the console based GUI open search.py.

**SKIP TO STEP 3 IF YOU WANT TO USE THE WEB BASED GUI**

Run it and type your query into the console once the "Enter Query" prompt shows and it will display the top 5 results alongside the score it was given.
Type quit to leave the GUI.

3. To use the web based GUI run frontend.py and either open http://127.0.0.1:5000 on your browser, or open the file templates/search.html
Type your query into the search bar and press enter.
