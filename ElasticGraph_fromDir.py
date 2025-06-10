from pyvis.network import Network
import os


def create_network(height='750px', width='100%', directed=True):
    """
    Initializes and returns a Pyvis Network object.
    """
    return Network(height=height, width=width, directed=directed)

def add_file_node(net, path, parent=None):
    """
    Adds a file node to the network with its size as the value.
    """
    size = os.path.getsize(path)
    label = os.path.basename(path)
    net.add_node(path, label=label, value=size)
    if parent:
        net.add_edge(parent, path)

def traverse_directory(net, directory, parent=None):
    """
    Recursively traverses the directory, adding nodes and edges to the network.
    """    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            add_file_node(net, item_path, parent)
        elif os.path.isdir(item_path):
            net.add_node(item_path, label=item)
            if parent:
                net.add_edge(parent, item_path)
            traverse_directory(net, item_path, item_path)

def build_directory_network(root_dir, output_file='directory_tree.html', show_buttons=True):
    """
    Builds the directory network and saves it to an HTML file.
    """
    net = create_network()
    net.add_node(root_dir, label=os.path.basename(root_dir))
    traverse_directory(net, root_dir, root_dir)
    if show_buttons:
        net.show_buttons()
    #net.show(output_file)
    net.save_graph(output_file)
    print(f"Directory network saved to {output_file}")
    return (output_file)