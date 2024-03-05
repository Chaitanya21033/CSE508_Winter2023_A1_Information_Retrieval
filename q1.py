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
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith(".txt"):
        # Create the path to the current file
        file_path = os.path.join(directory, filename)
        # Open and read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            # Print original text of sample files before preprocessing
            print(f"Original text of {filename}:\n{text}\n")
            # Preprocess the text
            preprocessed_tokens = preprocess_text(text)
            # Convert tokens back to string for saving and displaying
            preprocessed_text = ' '.join(preprocessed_tokens)
            # Print preprocessed text of sample files
            print(f"Preprocessed text of {filename}:\n{preprocessed_text}\n")
            # Save the preprocessed text to a new file
            preprocessed_file_path = os.path.join(directory, f"preprocessed_{filename}")
            with open(preprocessed_file_path, 'w', encoding='utf-8') as outfile:
                outfile.write(preprocessed_text)

# Note: This code will print and save all files in the directory.
# To limit the output to 5 sample files, you can add a counter and break the loop accordingly.
