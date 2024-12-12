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

# Step 3: Build Bigrams (pairs of consecutive tokens)
bigrams = defaultdict(list)

# Create bigrams from the tokens
for i in range(len(tokens) - 1):
    key = tokens[i]  # Current token
    next_token = tokens[i + 1]  # Next token
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
        while len(row) < random.randint(5, 10):  # Generate row of random length
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

# Example usage
start_tokens = ['k1', 'p1']
num_rows = 5  # Number of rows to generate

# Generate knitting pattern
generated_rows = generate_pattern(bigrams, start_tokens, num_rows)

# Format the generated pattern
formatted_pattern = format_pattern(generated_rows)

# Display the output
print("Generated Knitting Pattern:")
print(formatted_pattern)