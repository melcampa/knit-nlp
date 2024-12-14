import random
import os
from collections import defaultdict
import re

# Step 1: Load Knitting Patterns from a folder
def load_patterns_from_folder(folder_path):
    patterns = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file: 
                patterns.append(file.read())
    return patterns

# Step 2: Preprocess the Corpus
# Normalize the case, split patterns, and handle commas
def preprocess_corpus(corpus):
    """
    Extracts meaningful knitting instructions, recognizes terms like 'Cast on' and 'CO',
    and normalizes the text.
    """
    # Extract rows that likely contain instructions (rows starting with "Row", "Cast on", or similar terms)
    rows = re.findall(r'(Row \d+.*?:.*|Cast on.*|CO.*)', corpus, re.IGNORECASE)
    
    # Normalize the text: lowercase everything and ensure consistent spacing
    normalized_rows = []
    for row in rows:
        # Replace abbreviations for clarity and normalize
        row = row.lower()
        row = re.sub(r'\bco\b', 'cast on', row)  # Replace 'CO' with 'cast on'
        row = re.sub(r'[;,]', ' ', row)          # Remove punctuation like ';' and ','
        row = re.sub(r'\s+', ' ', row.strip())   # Normalize whitespace
        normalized_rows.append(row)
    
    return ' '.join(normalized_rows)

raw_corpus = ' '.join(load_patterns_from_folder('C:\\Users\\chipr\\OneDrive\\Desktop\\final\\knit-nlp\\input_patterns'))  # Load all patterns from files in 'data'
corpus = preprocess_corpus(raw_corpus)
corpus = corpus.lower() 

tokens = corpus.split()
bigrams = defaultdict(list)

# Create bigrams from the tokens
for i in range(len(tokens) - 1):
    key = tokens[i]  
    next_token = tokens[i + 1] 
    bigrams[key].append(next_token)

# Step 4: Generate a Knitting Pattern using the Bigram Model
def generate_pattern(bigrams, start_tokens, num_rows=5):
    """
    Generates a knitting pattern dynamically based on a bigram model.

    :param bigrams: Dictionary of bigrams (token pairs)
    :param start_tokens: List of tokens to start the sequence
    :param num_rows: Number of rows to generate
    :return: List of rows with knitting instructions
    """
    rows = []

    for _ in range(num_rows):
        # Randomly select the starting token from a list
        current_token = random.choice(start_tokens)
        row = [current_token]

        # Generate the rest of the row based on the bigram model
        while len(row) < 10:  # Generate row
            if current_token in bigrams:
                next_token = random.choice(bigrams[current_token])  # Pick a random next token from bigram
                row.append(next_token)
                current_token = next_token  # Update current token for next iteration
            else:
                break  # Stop if no bigram is found for the current token

        generated_row = ' '.join(row)
        rows.append(generated_row)

    return rows


# Step 5: Format the Generated Output
def format_pattern(rows):
    """
    Formats the generated pattern rows with semicolons.

    :param rows: List of rows with knitting instructions
    :return: Formatted string with rows separated by semicolons
    """
    return ';\n'.join(rows) + ' ;'

def extract_start_tokens(corpus):
    """
    Extract potential starting tokens for knitting patterns.
    """
    # Regex to capture starting tokens (e.g., 'cast on', 'row 1:')
    matches = re.findall(r'(cast on|row \d+.*?:)', corpus, flags=re.IGNORECASE)
    return list(set(matches))  # Remove duplicates

start_tokens = extract_start_tokens(corpus)
print("Possible starting tokens:", start_tokens)
num_rows = 5  # Number of rows to generate

# Generate knitting pattern
generated_rows = generate_pattern(bigrams, start_tokens, num_rows)

# Format the generated pattern
formatted_pattern = format_pattern(generated_rows)

# Display the output
print("Generated Knitting Pattern:")
print(formatted_pattern)
