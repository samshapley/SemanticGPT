# SemanticGPT

SemanticGPT is a project that explores the ability of OpenAI's GPT-4 to generate semantic networks based on word relations. It uses logit biasing to suppress certain outputs and guide the model's responses in a certain way. It uses this approach to create word paths (sequences of related words) which are then visualized as a semantic network.

The project consists of several Python scripts and a Jupyter Notebook:

1. `generate_network.py` - This script is responsible for generating the word paths. It uses the nltk corpus to generate a dictionary of the most common words, then uses a suppression loop to guide the GPT model's responses and create a word path for each word in the dictionary. The generated paths are saved in a JSON file.

2. `wandb_log.py` - This script is used for logging the results of the word path generation using Weights & Biases. It reads the word paths from the JSON file, shuffles them, and logs them as a table.

3. `lesson.ipynb` - This Jupyter notebook contains a series of experiments and explorations around the use of logit biasing with the GPT model. It includes experiments with suppressing specific words, suppressing certain categories of characters (like numbers or special characters), and analyzing the errors the model makes when performing arithmetic tasks.

4. `create_network_html.py` - This script uses NetworkX and PyVis to create a visualization of the semantic network from the generated word paths. It reads the word paths from the JSON file, creates a directed graph, and then generates an interactive HTML visualization of the graph.

## Requirements
- Python 3.7 or later
- OpenAI GPT-4 API key
- Libraries: nltk, pyvis, networkx, tqdm, pandas, matplotlib, wandb, json, time, random, os, re

## Usage

Before running the scripts, install the required Python libraries:

```
pip install -r requirements.txt
```

Next, you'll need to set your OpenAI GPT-4 API key as an environment variable:

```
export OPENAI_API_KEY="your-api-key-here"
```

Then, you can run the scripts:

```
python generate_network.py
python wandb_log.py
python create_network_html.py
```

The `lesson.ipynb` notebook can be opened and run in Jupyter notebook or Jupyter lab:

```
jupyter notebook lesson.ipynb
```

or

```
jupyter lab lesson.ipynb
```

Please note that running these scripts will make API requests to the GPT-4 model, which are billed by OpenAI. Also note that the scripts may take a long time to run due to the complexity of the computations and the number of API requests being made.
