#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 5180- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#Importing some Python libraries
import csv
import numpy as np
import math

documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])




#Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {"I", "and", "She", "her", "They", "their"}

stopwordDocuments = []

for i in documents:
    documentWords = i.split()
    
    passed = []
    for word in documentWords:
        if word not in stopWords:
          passed.append(word)
    stopwordDocuments.append(" ".join(passed))   

print("Documents after stopward removal: ")
print(stopwordDocuments )
print("\n")

  


#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
steeming = {
    'loves' : 'love',
    'love' : 'love',
    'cats' : 'cat',
    'cat' : 'cat',
    'dogs' : 'dog',
    'dog' : 'dog'
}

stemmingDocuments = []

for i in stopwordDocuments:
    documentWords = i.split()
    stemWords = []

    for word in documentWords:
        if word in steeming:
            stemWords.append(steeming[word])
        else:
            stemWords.append(word)

    stemmingDocuments.append(" ".join(stemWords))

print("Document after stemming: ")
print(stemmingDocuments)
print("\n")



#Identifying the index terms.
#--> add your Python code here
terms = ['love', 'cat', 'dog']

termCount = {term: [0,0,0] for term in terms}

for i, documentWords in enumerate(stemmingDocuments):
    for term in terms:
        termCount[term][i] = documentWords.split().count(term)

print("Index Term Word Count Chart: ")
print("| Term | d1 | d2 | d3 |")
print("|------|----|----|----|")
for term in terms:
    print(f"| {term} | {termCount[term][0]} | {termCount[term][1]} | {termCount[term][2]} |")




#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here

#Calculating TF
total_terms = [len(doc.split()) for doc in stemmingDocuments]
tf = {term: [0, 0, 0] for term in terms}

for term in terms:
    for i in range(len(stemmingDocuments)):
        
        if total_terms[i] > 0:
            tf[term][i] = termCount[term][i] / total_terms[i]
        else:
            tf[term][i] = 0

print("\nTF Table:")
print("| Term | d1 | d2 | d3 |")
print("|------|----|----|----|")
for term in terms:
    print(f"| {term} | {tf[term][0]:.3f} | {tf[term][1]:.3f} | {tf[term][2]:.3f} |")





# Calculating IDF
N = len(stemmingDocuments)  
idf = {term: 0 for term in terms}

for term in terms:
    
    df = 0
    for count in termCount[term]:
        if count > 0:
            df += 1
    
    if df > 0:
        idf[term] = math.log10(N / df)
    else:
        idf[term] = 0

print("\nIDF Table:")
print("| Term | IDF |")
print("|------|-----|")
for term in terms:
    print(f"| {term} | {idf[term]:.3f} |")







# Calculating TF-IDF
tf_idf = {term: [0, 0, 0] for term in terms}

for term in terms:
    for i in range(len(stemmingDocuments)):
        
        tf_idf[term][i] = tf[term][i] * idf[term]


print("\nTF-IDF Matrix:")
print("| Document | love | cat | dog |")
print("|----------|------|-----|-----|")
for i in range(len(stemmingDocuments)):
    print(f"| d{i + 1}      | {tf_idf['love'][i]:.3f} | {tf_idf['cat'][i]:.3f} | {tf_idf['dog'][i]:.3f} |")