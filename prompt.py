import os
import json

# ignore list, a list of files to ignore if name matches
ignore = [
    'prompt.py', 
    '__init__.py',
    'main.py',
    'logit_search.py',
    'token_swap_demo.py',
    'logit_bias.py',
    'semantic_network.py',
    'playground.py',
    'network_image.p',
] 

# Get the current directory
current_dir = os.getcwd()

# Open the target file
with open('prompt.txt', 'w') as outfile:
    # Loop over all files in the current directory
    for filename in os.listdir(current_dir):
        # Check if the file is in the ignore list
        if filename in ignore:
            continue
        
        # Check if the file is a .py or .yml file
        if filename.endswith('.yml') or filename.endswith('.py'):
            # Open the file
            with open(filename, 'r') as infile:
                # Write the file path to the output file
                outfile.write(f"\n--- File Path: {os.path.join(current_dir, filename)} ---\n")
                
                # Read the contents of the file, remove line breaks and leading spaces
                content = infile.read().replace('\n', '').replace('\r', '')
                content = ' '.join(content.split())

                # Write the modified contents of the file to the output file
                outfile.write(content)
                outfile.write("\n")

        # Check if the file is a .ipynb file
        elif filename.endswith('.ipynb'):
            # Open the file
            with open(filename, 'r') as infile:
                # Write the file path to the output file
                outfile.write(f"\n--- File Path: {os.path.join(current_dir, filename)} ---\n")

                # Load the notebook
                notebook = json.load(infile)

                # Loop over all cells in the notebook
                for cell in notebook['cells']:
                    # Check if the cell is a code cell
                    if cell['cell_type'] == 'code':
                        # Join the lines of the cell, remove line breaks and leading spaces
                        content = ''.join(cell['source']).replace('\n', '').replace('\r', '')
                        content = ' '.join(content.split())

                        # Write the contents of the cell to the output file
                        outfile.write(content)
                        outfile.write("\n")
