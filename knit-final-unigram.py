import random
import os
from collections import defaultdict

# Step 1: Load Knitting Patterns from a folder
def load_patterns_from_folder(folder_path):
    patterns = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                patterns.append(file.read())
    return patterns

# Step 2: Preprocess the Corpus
# Normalize the case, split patterns, and handle commas
corpus = ' '.join(load_patterns_from_folder('input_patterns'))  # Load all patterns from files in 'data'
corpus = corpus.lower()  # Normalize case

tokens = corpus.split()

# Step 3: Build Unigrams (frequency distribution of tokens)
unigrams = defaultdict(int)

# Count the frequency of each token
for token in tokens:
    unigrams[token] += 1

# Step 4: Generate a Knitting Pattern using the Unigram Model
def generate_pattern(unigrams, start_tokens, num_rows=5):
    """
    Generates a knitting pattern dynamically based on a unigram model.

    :param unigrams: Dictionary of unigram frequencies
    :param start_tokens: List of tokens to start the sequence
    :param num_rows: Number of rows to generate
    :return: List of rows with knitting instructions
    """
    rows = []
    
    # Convert the unigram dictionary to a list of tokens, weighted by their frequency
    weighted_tokens = []
    for token, freq in unigrams.items():
        weighted_tokens.extend([token] * freq)

    for _ in range(num_rows):
        row = list(start_tokens)
        
        # Generate the rest of the row based on the unigram model
        while len(row) < len(start_tokens) + random.randint(2, 5):  # Generate a row of random length
            next_token = random.choice(weighted_tokens)  # Randomly select a token based on frequency
            row.append(next_token)

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

# Example usage
start_row = ['k1', 'k1']  # Example starting row
num_rows = 5  # Number of rows to generate

# Generate knitting pattern
generated_rows = generate_pattern(unigrams, start_row, num_rows)

# Format the generated pattern
formatted_pattern = format_pattern(generated_rows)

# Display the output
print("Generated Knitting Pattern:")
print(formatted_pattern)
