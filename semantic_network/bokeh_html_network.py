import json
import networkx as nx
from bokeh.io import output_file, show
from bokeh.models import (Circle, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, Range1d, TapTool, WheelZoomTool, PanTool)
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral4

# Load the word paths from the json file
with open("word_paths.json", 'r') as f:
    word_paths = json.load(f)

# Choose 1000 words
word_paths = {k: word_paths[k] for k in list(word_paths)[:10000]}

# Create an undirected graph 
G = nx.Graph()

# Add nodes and edges to the graph
for word, paths in word_paths.items():
    for path_word in paths:
        G.add_edge(word, path_word)

# Create a mapping between node labels and integer indices
label_to_index = {label: index for index, label in enumerate(G.nodes)}

# Create a new graph using integer indices
G_int = nx.relabel_nodes(G, label_to_index)

# Configure the plot
plot = Plot(width=800, height=800,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))



# Add tools to interact with the plot
plot.add_tools(HoverTool(tooltips=[("word", "@word_label")]), 
               TapTool(), WheelZoomTool(), PanTool())


# Generate the positions for the nodes
positions_labels = nx.spring_layout(G_int,k=0.04,scale=0.9)  # Increase scale and k


# Create the network graph
graph_renderer = from_networkx(G_int, positions_labels, scale=1, center=(0, 0))

# Since we have mapped word_labels to integers, we need to create a reverse mapping for display
index_to_label = {v: k for k, v in label_to_index.items()}

# Add extra node attributes for hover tool
degree_cent = nx.degree_centrality(G_int)
nx.set_node_attributes(G_int, degree_cent, 'degree_cent')
nx.set_node_attributes(G_int, index_to_label, 'word_label')

# Configure the node glyphs
graph_renderer.node_renderer.glyph = Circle(size=2.5, fill_color='black')
graph_renderer.node_renderer.selection_glyph = Circle(size=3, fill_color=Spectral4[2])
graph_renderer.node_renderer.hover_glyph = Circle(size=3, fill_color=Spectral4[1])


# Add the word labels as a node attribute
graph_renderer.node_renderer.data_source.data['word_label'] = list(index_to_label.values())


# Configure the edge glyphs
graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.9, line_width=1)
graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color=Spectral4[2], line_width=2)
graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color=Spectral4[1], line_width=2)

# Set the inspection and selection policy
graph_renderer.inspection_policy = NodesAndLinkedEdges()
graph_renderer.selection_policy = NodesAndLinkedEdges()

# Add extra node attributes for hover tool
connected_nodes = {n: list(G_int.neighbors(n)) for n in G_int.nodes()}
nx.set_node_attributes(G_int, connected_nodes, 'connected_nodes')

# Mapping connected nodes from integers back to their labels
for node in G_int.nodes(data=True):
    node[1]['connected_nodes'] = [index_to_label[i] for i in node[1]['connected_nodes']]

# Convert the list of connected nodes to an unordered list in HTML
for node in G_int.nodes(data=True):
    node[1]['connected_nodes'] = '<ul>' + ''.join(['<li>'+i+'</li>' for i in node[1]['connected_nodes']]) + '</ul>'

# Add the connected_nodes to the node renderer data source
graph_renderer.node_renderer.data_source.data['connected_nodes'] = [i[1]['connected_nodes'] for i in G_int.nodes(data=True)]

# Modify the HoverTool tooltips to include connected nodes
plot.add_tools(HoverTool(tooltips=[("word", "@word_label"), ("connected nodes", "@connected_nodes{safe}")]))


# Append the graph to the plot
plot.renderers.append(graph_renderer)

# Output to an HTML file
output_file("word_graph.html")

# Show the result
show(plot)
