from pyvis.network import Network
import os

net = Network(height='750px', width='100%', directed=True)

def add_file_node(path, parent=None):
    size = os.path.getsize(path)
    label = os.path.basename(path)
    net.add_node(path, label=label, value=size)
    if parent:
        net.add_edge(parent, path)

def traverse_directory(directory, parent=None):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            add_file_node(item_path, parent)
        elif os.path.isdir(item_path):
            net.add_node(item_path, label=item)
            if parent:
                net.add_edge(parent, item_path)
            traverse_directory(item_path, item_path)

root_dir = 'C:/Users/Email/Desktop/CAM'
net.add_node(root_dir, label=os.path.basename(root_dir))
traverse_directory(root_dir, root_dir)

net.show_buttons()
net.show('directory_tree.html')
