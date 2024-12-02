import re
from sklearn.feature_extraction.text import TfidfVectorizer
from pymongo import MongoClient
from collections import defaultdict
import numpy as np

# Define documents as a list
documents = [
    "After the medication, headache and nausea were reported by the patient.",
    "The patient reported nausea and dizziness caused by the medication.",
    "Headache and dizziness are common effects of this medication.",
    "The medication caused a headache and nausea, but no dizziness was reported.",
]

queries = [
    "nausea and dizziness",
    "effects",
    "nausea was reported",
    "dizziness",
    "the medication",
]

# MongoDB Connect
client = MongoClient("mongodb://localhost:27017/")
db = client.search_engine
termsCol = db.terms
documentsCol = db.documents

# Clear existing collections to prevent duplicates
termsCol.delete_many({})
documentsCol.delete_many({})

tfidfVector = TfidfVectorizer()
documentVector = tfidfVector.fit_transform(documents)
documentTerms = tfidfVector.get_feature_names_out()
matrix = documentVector.toarray()
invertedIndex = defaultdict(list)

# Tokenize and Preprocess Function
def tokenize(document):
    document = re.sub(r"[^\w\s]", "", document).lower()

    # Array of tokens
    tokens = document.split()

    # Unigrams
    unigrams = tokens

    # Bigrams
    bigrams = [" ".join(tokens[i:i + 2]) for i in range(len(tokens) - 1)]

    # Trigrams
    trigrams = [" ".join(tokens[i:i + 3]) for i in range(len(tokens) - 2)]

    return unigrams + bigrams + trigrams

# Populate the inverted index and MongoDB
for i, document in enumerate(documents):
    # Insert the document into the MongoDB collection
    documentsCol.insert_one({"_id": i, "content": document})

    # Tokenize the document
    tokens = tokenize(document)

    # Process each token
    for token in tokens:
        if token in documentTerms:
            pos = list(documentTerms).index(token)
            tfidf = matrix[i, pos]

            # Add the token to the inverted index and MongoDB
            invertedIndex[token].append({"docID": i, "tfidf": tfidf})

# Insert tokens into the MongoDB `terms` collection
for term, refs in invertedIndex.items():
    termsCol.insert_one({"term": term, "docs": refs})

# Query Scoring Function
def queryScore(query):
    qVector = np.zeros(len(documentTerms))
    qTokens = tokenize(query)
    qScores = []
    qDot = qVector * tfidfVector.idf_
    qLinalg = np.linalg.norm(qDot)

    print(f"Query tokens: {qTokens}")  # Debugging: Print query tokens

    for token in qTokens:
        term = termsCol.find_one({"term": token})  # Search for the term in MongoDB
        if term:
            pos = list(documentTerms).index(token)
            qVector[pos] += 1
        else:
            print(f"Token '{token}' not found in terms collection.")  # Debugging: Missing tokens

    for doc in documentsCol.find():
        docID = doc["_id"]
        docSent = doc["content"]
        docVector = matrix[docID]
        docLinalg = np.linalg.norm(docVector)

        if docLinalg > 0 and qLinalg > 0:
            cosineScore = np.dot(qDot, docVector) / (qLinalg * docLinalg)
            qScores.append((docSent, cosineScore))

    # Return results sorted by score in descending order
    return sorted(qScores, key=lambda x: x[1], reverse=True)
# Process Queries
for i, q in enumerate(queries):
    print(f"Query {i + 1}: {q}")

    output = queryScore(q)

    for document, score in output:
        print(f" \"{document}\", {score:.2f}")