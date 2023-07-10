import wandb
import json
import random

with open('word_paths.json', 'r') as f:
    word_paths = json.loads(f.read())

# Convert dictionary items to a list
items = list(word_paths.items())

# Shuffle the list
random.shuffle(items)

wandb.init(project='Logit Bias Exploration')

# Change the dict items to shuffled list items
data = [(k, *words) for k, words in items if len(words) == 3]

table = wandb.Table(columns=['Suppression Word', 'Response 1', 'Response 2', 'Response 3'], data=data)
wandb.log({'table': table})
wandb.finish()
