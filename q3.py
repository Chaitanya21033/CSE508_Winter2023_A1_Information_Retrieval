import re
import pickle
from collections import defaultdict

# Preprocessing function: lowercase and remove punctuation
def preprocess(text):
    return re.sub(r'[^\w\s]', '', text.lower()).split()

# Create the positional index
from collections import defaultdict

# Replace lambda with a regular function for defaultdict
def default_dict_list():
    return defaultdict(list)


import os
import pickle
from collections import defaultdict

# Directory where your files are located
data_dir = './data'

# Function to read files and return their content
def read_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Function to build the positional index from preprocessed files
def create_positional_index(directory):
    positional_index = defaultdict(default_dict_list)
    for i in range(1, 1000):  # Assuming file numbering starts from 1 to 999
        preprocessed_filename = os.path.join(directory, f'preprocessed_file{i}.txt')
        if os.path.exists(preprocessed_filename):
            text = read_file_content(preprocessed_filename)
            words = text.split()  # Assuming preprocessed files are whitespace-separated words
            for position, word in enumerate(words):
                positional_index[word][f'file{i}.txt'].append(position)
    return positional_index

positional_index = create_positional_index(data_dir)

# The rest of the code for saving/loading the index and handling queries remains the same

# Save the positional index
with open('positional_index.pkl', 'wb') as f:
    pickle.dump(positional_index, f)

# Load the positional index for search operations
with open('positional_index.pkl', 'rb') as f:
    loaded_positional_index = pickle.load(f)

# Example of handling a query remains the same as provided in the previous code snippet

# Function to search for phrase queries in the positional index
def search_phrase(query, positional_index):
    words = preprocess(query)  # Assuming preprocess is defined as before
    if not words:
        return 0, []
    
    # Retrieve postings lists for each word in the query if it exists in the index
    postings_lists = []
    for word in words:
        if word in positional_index:
            postings_lists.append(positional_index[word])
        else:
            return 0, []  # If any word in the query is not found, return no documents found
    
    # Ensure we have postings lists to work with
    if not postings_lists:
        return 0, []
    
    # Attempt to find documents where the phrase occurs in order
    results = set(postings_lists[0].keys())  # Start with documents for the first word
    for i in range(1, len(words)):
        results &= set(postings_lists[i].keys())  # Intersect with documents containing subsequent words
    
    # Now check for actual phrase occurrence in the intersected documents
    final_docs = []
    for doc in results:
        valid_positions = [postings_lists[0][doc]]  # Positions of the first word in documents
        for i in range(1, len(words)):
            valid_positions.append([pos - i for pos in postings_lists[i][doc]])  # Adjust positions for phrase matching
        
        # Check if there's any position where the entire phrase occurs
        if any(set.intersection(*map(set, valid_positions))):
            final_docs.append(doc)
    
    return len(final_docs), final_docs


# Example of handling a query
n_queries = 2
queries = ["Car bag in a canister", "Coffee brewing techniques in cookbook"]

for i, query in enumerate(queries, start=1):
    n_docs, docs = search_phrase(query, loaded_positional_index)
    print(f"Number of documents retrieved for query {i} using positional index: {n_docs}")
    print(f"Names of documents retrieved for query {i} using positional index: {', '.join(docs)}")
