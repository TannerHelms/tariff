import re

def clean_hts_file(input_file, output_file):
    # Patterns to match the lines to be removed
    unwanted_pattern = re.compile(r'^\d+\.?\d*%\s1?/?\s*Free\s?\(.*?\)\s*\d+%.*')
    percentage_pattern = re.compile(r'^\d+\.?\d*%\s1?/?\s*.*')
    kg_pattern = re.compile(r'^\s*kg\s*$')
    empty_line_pattern = re.compile(r'^\s*$')
    
    with open(input_file, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    for line in lines:
        if not unwanted_pattern.search(line) and not percentage_pattern.search(line) and not kg_pattern.search(line) and not empty_line_pattern.search(line):
            # Tokenize the line
            tokens = line.split()
            # Keep only the first three tokens and the description
            if len(tokens) > 3:
                cleaned_line = ' '.join(tokens[:3] + [' '.join(tokens[3:])])
            else:
                cleaned_line = line
            cleaned_lines.append(cleaned_line)

    with open(output_file, 'w') as file:
        file.writelines(cleaned_lines)

if __name__ == "__main__":
    input_file = 'chapter_full_text/85.txt'
    output_file = 'chapter_full_text/85.txt'
    clean_hts_file(input_file, output_file)
    print(f'Cleaned file saved as {output_file}')
