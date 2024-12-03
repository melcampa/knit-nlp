import random
from collections import defaultdict

# Step 1: Load Knitting Patterns Corpus
with open('knitting-patterns.txt', 'r') as file:
    corpus = file.read()

# Step 2: Preprocess the Corpus
# Normalize the case, split patterns, and handle angle brackets
corpus = corpus.lower()  # Normalize case
patterns = corpus.split('<')  # Split by opening angle brackets

# Remove pattern names (the first part before <), and process each pattern
cleaned_patterns = []
for pattern in patterns:
    pattern = pattern.strip()
    if pattern:
        # Remove the ending bracket and split instructions
        pattern = pattern.split('>')[0].strip()
        instructions = pattern.split(';')  # Split by semicolons to get rows
        # Further process rows if needed (e.g., remove extra spaces)
        instructions = [row.strip() for row in instructions if row.strip()]
        cleaned_patterns.append(instructions)

# Step 3: Build N-Grams
n = 3  # Trigram model
ngrams = defaultdict(list)

# Tokenize the instructions into individual knitting operations
tokens = []
for pattern in cleaned_patterns:
    for row in pattern:
        tokens.extend(row.split())  # Tokenize each row into individual stitches

# Create n-grams from the tokens
for i in range(len(tokens) - n):
    key = tuple(tokens[i:i+n-1])  # Prefix of length n-1
    next_token = tokens[i+n-1]  # The next token
    ngrams[key].append(next_token)

# Step 4: Generate a Knitting Pattern
def generate_pattern(ngrams, start_tokens, stitches_per_row, num_rows=5):
    """
    Generates a knitting pattern dynamically to meet the target stitches per row.

    :param ngrams: Dictionary of n-grams
    :param start_tokens: List of tokens to start the sequence
    :param stitches_per_row: Target number of stitches per row
    :param num_rows: Number of rows to generate
    :return: List of rows with knitting instructions
    """
    rows = []
    for _ in range(num_rows):
        current = tuple(start_tokens)
        row = list(current)
        total_stitches = len(start_tokens)  # Initialize stitch count

        while total_stitches < stitches_per_row:
            if current in ngrams:
                next_token = random.choice(ngrams[current])
                row.append(next_token)

                # Update stitch count for `kfb`
                if next_token == 'kfb':
                    total_stitches += 1  # Add one extra stitch for `kfb`

                total_stitches += 1  # General token adds one stitch
                current = tuple(row[-n+1:])  # Update current context
            else:
                break  # Stop if no continuation is found

        rows.append(' '.join(row[:stitches_per_row]))  # Trim row to target stitches

    return rows

# Step 5: Format the Generated Output
def format_pattern(rows):
    """
    Formats the generated pattern rows with semicolons.

    :param rows: List of rows with knitting instructions
    :return: Formatted string with rows separated by semicolons
    """
    return ';\n'.join(rows) + ' ;'


def count_stitches(row):
    """
    Counts the number of stitches in a row of knitting instructions.
    :param row: A string representing a row of knitting instructions.
    :return: The total number of stitches in the row.
    """
    stitches = row.split()  # Split the row into individual stitches
    count = 0

    for stitch in stitches:
        count += 1  # Each token typically represents one stitch
        if stitch == 'kfb':  # Handle 'kfb', which adds an extra stitch
            count += 1

    print(f"Row: '{row}' -> Stitches: {count}")
    return count


# Example usage
start = ['k1', 'kfb']  # Starting sequence for the generator
stitches_per_row = 8  # Target stitches per row
num_rows = 7  # Number of rows to generate

generated_rows = generate_pattern(ngrams, start, stitches_per_row, num_rows)

# Format the generated pattern
formatted_pattern = format_pattern(generated_rows)

# Display the output
print("Generated Knitting Pattern:")
print(formatted_pattern)

stitch_counts = [count_stitches(row) for row in generated_rows]

print(stitch_counts)