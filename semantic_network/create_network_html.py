import json
import networkx as nx
from pyvis.network import Network

# Load the word paths from the json file
with open("word_paths.json", 'r') as f:
    word_paths = json.load(f)

# choose 100 words
word_paths = {k: word_paths[k] for k in list(word_paths)[:5000]}

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for word, paths in word_paths.items():
    for path_word in paths:
        G.add_edge(word, path_word)

# Convert the NetworkX graph into a PyVis network
pyvis_graph = Network(notebook=True, select_menu=True)
pyvis_graph.from_nx(G)

# Provide the nodes with labels
for node in pyvis_graph.nodes:
    node["title"] = f"Word: {node['id']}"
    node["label"] = node["id"]


pyvis_graph.show_buttons(filter_=['physics']) 

#turn physics off
pyvis_graph.toggle_physics(False)

# Save the graph to an HTML file
pyvis_graph.show("word_graph.html")
