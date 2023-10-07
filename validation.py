import os

def is_valid_fasta(file_content):
    # Define a regular expression to validate FASTA format
    fasta_pattern = r'^>.*\n[ACGTNURYSWKMBDHVXacgtnuryswkmdbhvx\n]*$'
    return bool(re.match(fasta_pattern, file_content, re.MULTILINE | re.IGNORECASE))


def is_protein_alignment(input_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            sequence = ''.join(line.strip() for line in lines if not line.startswith('>'))
            valid_protein_chars = "DEFHIKLMNPQRSVWYdefhiklmnpqrsvwy"
            return any(aa in valid_protein_chars for aa in sequence)
    except Exception:
        return False    


def is_protein_alignment_nexus(input_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            sequence_found = False
            for line in lines:
                if sequence_found:
                    if any(aa in line for aa in "ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy"):
                        return True
                if line.strip().startswith("MATRIX"):
                    sequence_found = True
    except Exception:
        pass
    return False

def is_fasta_aligned(input_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            sequences = []
            current_sequence = ""
            for line in lines:
                line = line.strip()
                if line.startswith(">"):
                    if current_sequence:
                        sequences.append(current_sequence)
                    current_sequence = ""
                else:
                    current_sequence += line
            if current_sequence:
                sequences.append(current_sequence)
            return all(len(seq) == len(sequences[0]) for seq in sequences)
    except Exception:
        return False

def is_nexus_aligned(input_file):
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()
            sequence_found = False
            sequences = []
            for line in lines:
                line = line.strip()
                if sequence_found and line:
                    sequences.append(line)
                if line.startswith("MATRIX"):
                    sequence_found = True
            return all(len(seq) == len(sequences[0]) for seq in sequences)
    except Exception:
        return False

def is_valid_fasta(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if len(lines) < 2 or not lines[0].startswith('>'):
                return False
        return True
    except Exception:
        return False
        
        
# Define the text_formatting function here
def text_formatting(text_file_path):
    try:
        # Determine the full path to the text file within the package
        package_directory = os.path.dirname(__file__)
        full_text_file_path = os.path.join(package_directory, text_file_path)

        with open(full_text_file_path, 'r') as intro_file:
            lines = intro_file.readlines()
            formatted_text = ""

            for line in lines:
                line = line.strip()  # Remove leading and trailing whitespace

                if line.startswith('**') and line.endswith('**'):
                    # Apply bold formatting
                    text_to_format = line.strip('**')
                    formatted_text += f'<b>{text_to_format}</b><br>'
                elif line.startswith('*') and line.endswith('*'):
                    # Apply italic formatting
                    text_to_format = line.strip('*')
                    formatted_text += f'<i>{text_to_format}</i><br>'
                else:
                    # Keep the line as is (normal formatting)
                    formatted_text += f'{line}<br>'
            return formatted_text  # Set HTML content with formatting

    except FileNotFoundError as e:
        return "Error: Content not found."        
