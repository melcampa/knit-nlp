import re
import os

# Define a list of common knitting abbreviations
abbreviations = ['k', 'p', 'yo', 'sl', 'inc', 'dec', 'ssk', 'cable', 'tbl', 'CO', 'BO', 'K2TOG']

# Define a function to tokenize the knitting pattern
def tokenize_knitting_pattern(pattern):
    # Create a regular expression to capture the abbreviations and numbers
    regex = r'(' + '|'.join(abbreviations) + r')(\d*)'  # Matches abbreviation followed by optional number
    tokens = re.findall(regex, pattern)
    
    # Format the tokens
    tokenized_pattern = [f'{abbreviation}{num if num else ""}' for abbreviation, num in tokens]
    
    return tokenized_pattern

# Define a function to process a folder of txt files
def process_knitting_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):  # Only process .txt files
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, 'r') as file:
                content = file.read()  # Read the entire content of the file
                
                # Expand and tokenize the pattern based on the content
                expanded_content = expand_knitting_instructions(content)
                
                # Write the updated pattern to a new file in the output folder
                output_file_path = os.path.join(output_folder, filename)
                with open(output_file_path, 'w') as output_file:
                    output_file.write("\n".join(expanded_content))  # Each row's stitches on a new line
    
    print(f"Processed files from {input_folder} and saved to {output_folder}")

# Function to handle knitting instructions (e.g., "knit across")
def expand_knitting_instructions(pattern):
    expanded_pattern = []
    lines = pattern.splitlines()
    
    # Define a variable for the number of stitches
    total_stitches = None

    for line in lines:
        line = line.strip()

        # Handle the abbreviation 'CO' for cast-on
        if "CO" in line:  # Look for CO abbreviation instead of full phrase "Cast on"
            # Extract number of stitches (e.g., from "CO 96")
            co_match = re.search(r'CO (\d+)', line)
            if co_match:
                total_stitches = int(co_match.group(1))
                expanded_pattern.append(" ".join(["k1"] * total_stitches))  # Cast on 96 stitches, for example
        elif "repeat" in line:
            # Handle repeat instruction like *K10, K2tog* Repeat around
            repeat_match = re.search(r'\*([^\*]+)\* Repeat around', line)  # Capture the instructions inside the repeat block
            if repeat_match:
                repeat_sequence = repeat_match.group(1).strip()  # e.g., "K10, K2tog"
                repeat_tokens = tokenize_knitting_pattern(repeat_sequence)  # Tokenize the sequence
                
                # Calculate the number of repeats based on total stitches
                if total_stitches:
                    repeat_count = total_stitches // len(repeat_tokens)  # Number of full repeats based on CO
                    row = []
                    for _ in range(repeat_count):
                        row.extend(repeat_tokens)
                    remaining_stitches = total_stitches % len(repeat_tokens)
                    row.extend(repeat_tokens[:remaining_stitches])  # Handle any leftover stitches
                    expanded_pattern.append(" ".join(row))  # Join stitches into a single line
                    # Update total_stitches for the next line (stitches decrease after each repeat)
                    total_stitches -= len(row)
        elif "to end" in line:
            # Handle "to end" as in "*K to end"
            line_tokens = tokenize_knitting_pattern(line)
            expanded_pattern.append(" ".join(line_tokens))  # Join the stitches in the same line
        elif "decreased" in line:
            # Skip lines with decrease information (e.g., "8 stitches decreased, 64 stitches remaining")
            continue
        else:
            # Tokenize the line normally
            expanded_pattern.append(" ".join(tokenize_knitting_pattern(line)))  # Join the stitches in the same line

    return expanded_pattern

# Example usage
input_folder = 'input_patterns'  # Folder containing your input .txt files
output_folder = 'data'           # Folder to save the output files

# Process the folder and get tokenized patterns
process_knitting_folder(input_folder, output_folder)
