import nltk
nltk.download('stopwords')
nltk.download('punkt')

import os
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Set the directory where your text files are located
directory = "data"

# Ensure NLTK stop words and tokenizer are ready
stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)

# Function to preprocess text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()
    # Tokenize
    tokens = word_tokenize(text)
    # Remove stopwords and punctuations
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations]
    # Remove blank space tokens (if any)
    tokens = [word for word in tokens if word.strip()]
    # Return the preprocessed tokens
    return tokens

# Iterate through each file in the directory
# for filename in os.listdir(directory):
#     # Check if the file is a text file
#     if filename.endswith(".txt"):
#         # Create the path to the current file
#         file_path = os.path.join(directory, filename)
#         # Open and read the file
#         with open(file_path, 'r', encoding='utf-8') as file:
#             text = file.read()
#             # Print original text of sample files before preprocessing
#             print(f"Original text of {filename}:\n{text}\n")
#             # Preprocess the text
#             preprocessed_tokens = preprocess_text(text)
#             # Convert tokens back to string for saving and displaying
#             preprocessed_text = ' '.join(preprocessed_tokens)
#             # Print preprocessed text of sample files
#             print(f"Preprocessed text of {filename}:\n{preprocessed_text}\n")
#             # Save the preprocessed text to a new file
#             preprocessed_file_path = os.path.join(directory, f"preprocessed_{filename}")
#             with open(preprocessed_file_path, 'w', encoding='utf-8') as outfile:
#                 outfile.write(preprocessed_text)

# # Note: This code will print and save all files in the directory.
# # To limit the output to 5 sample files, you can add a counter and break the loop accordingly.

import os
import pickle

# Assuming 'data' directory contains preprocessed files prefixed with 'preprocessed_'
directory = "data"
inverted_index = {}

# Function to update inverted index with tokens from a document
def update_inverted_index(tokens, doc_name):
    for token in tokens:
        if token not in inverted_index:
            inverted_index[token] = [doc_name]
        elif doc_name not in inverted_index[token]:
            inverted_index[token].append(doc_name)

# Build the inverted index
for filename in os.listdir(directory):
    if filename.startswith("preprocessed_"):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().split()
            update_inverted_index(tokens, filename)

# Save the inverted index using pickle
with open("inverted_index.pkl", 'wb') as outfile:
    pickle.dump(inverted_index, outfile)

# Load the inverted index
with open("inverted_index.pkl", 'rb') as infile:
    loaded_inverted_index = pickle.load(infile)

# Function to perform Boolean operations
def perform_operation(set1, set2, operation):
    if operation == "AND":
        return set1.intersection(set2)
    elif operation == "OR":
        return set1.union(set2)
    elif operation == "AND NOT":
        return set1 - set2
    elif operation == "OR NOT":
        return set1 - set2
    else:
        return set()

# Function to preprocess and tokenize query terms (reusing the preprocess_text function from Q1)
def preprocess_query(query):
    return preprocess_text(query)  # Assume preprocess_text is defined as in Q1

def process_queries(queries):
    for i, (query, operations) in enumerate(queries, start=1):
        terms = preprocess_query(query)
        sets = [set(loaded_inverted_index.get(term, [])) for term in terms]
        result_set = sets[0]
        for op, next_set in zip(operations, sets[1:]):
            result_set = perform_operation(result_set, next_set, op)
        # Output format
        print(f"Query {i}: {' '.join(terms)}")
        print(f"Number of documents retrieved for query {i}: {len(result_set)}")
        print(f"Names of the documents retrieved for query {i}: {', '.join(sorted(result_set))}")

# Sample input (replace this with actual input handling)
sample_queries = [
    ("Car bag in a canister", ["OR", "AND NOT"]),
    ("Coffee brewing techniques in cookbook", ["AND", "OR NOT", "OR"])
]

process_queries(sample_queries)