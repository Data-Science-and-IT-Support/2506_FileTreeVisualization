#!/usr/bin/env python

#usage
#if __name__ == "__main__":
#    main()


"""
Originally from Alex Eidt

Creates an acyclic directed graph representing the structure of any directory.
"""

import os
import argparse
import requests
from graphviz import Digraph
from typing import Union


# Replace with the actual path to your Graphviz 'bin' directory
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

def convert(size: int) -> str:
    """
    Converts the given "size" into its corresponding bytes representation
    rounded to two decimal places.
    """
    kilo = 1024
    sizes = ["bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    index = 0
    while size >= kilo and index < len(sizes) - 1:
        size /= kilo
        index += 1
    suffix = sizes[index]
    if index == 0 and size == 1:
        suffix = "byte"
    return f"{round(size, 2)} {suffix}"

def size(path: str) -> dict:
    """
    Recursively calculates the size of all files in the given "path"
    directory in an efficient way by starting at the bottom of the directory
    and building up directory sizes.

    Returns a dictionary mapping directory paths to their memory footprint.
    """
    file_sizes = {}
    for root, dirs, files in os.walk(os.path.normpath(path), topdown=False):
        total_size = sum(os.path.getsize(os.path.join(root, f)) for f in files)
        file_sizes[root] = total_size
        for dir_ in dirs:
            dir_path = os.path.join(root, dir_)
            if dir_path in file_sizes:
                file_sizes[root] += file_sizes[dir_path]
    # Convert all sizes in bytes to human-readable format
    for path, size_in_bytes in file_sizes.items():
        file_sizes[path] = convert(size_in_bytes)
    return file_sizes

def graph_dir(
    directory: str,
    filename: str = "",
    orientation: str = "LR",
    data: bool = True,
    show_files: bool = True,
    show_hidden: bool = True,
    max_depth: int = -1,
    ranksep: Union[float, None] = None,
    file_type: str = "svg",
    render: bool = True,
) -> None:
    """
    Creates an acyclic directed adjacency graph of the given directory.

    directory:      The directory to generate the graph for.
    filename:       The name of the file that will store the graph.
    orientation:    Graph orientation: 'LR', 'RL', 'TB', or 'BT'.
    data:           If True, shows memory used for each directory and all files.
    show_files:     If True, shows files in the directory.
    show_hidden:    If True, includes hidden directories/files.
    max_depth:      Maximum depth of directory traversal.
    ranksep:        Distance between layers in inches.
    file_type:      Output file format: 'svg' or 'png'.
    render:         If True, renders the graph using Graphviz; otherwise, uses quickchart.io.
    """
    if not os.path.isdir(directory):
        raise NotADirectoryError(f"The path '{directory}' is not a valid directory.")

    options = ["LR", "RL", "TB", "BT"]
    if orientation.upper() not in options:
        raise ValueError(f'Invalid argument for "orientation". Must be one of {", ".join(options)}')

    if file_type not in ["svg", "png"]:
        raise ValueError('Invalid argument for "file_type". Must be either "png" or "svg"')

    graph_attr = {
        "rankdir": orientation.upper(),
        "overlap": "scale",
        "splines": "polyline",
    }
    if ranksep is not None:
        graph_attr["ranksep"] = str(ranksep)

    tree = Digraph(engine='sfdp', graph_attr=graph_attr)

    index = 0  # Index used to ID files in the graph.

    def multiple(n):
        return "" if n == 1 else "s"

    # Get data for size of each folder.
    dir_sizes = size(directory) if data else {}

    for root, dirs, files in os.walk(os.path.normpath(directory)):
        depth = root[len(directory):].count(os.sep)
        if max_depth > 0 and depth >= max_depth:
            continue
        if not show_hidden:
            dirs[:] = [d for d in dirs if not d.startswith((".", "__"))]
            files = [f for f in files if not f.startswith((".", "__"))]

        tree.attr("node", shape="folder", fillcolor="lemonchiffon", style="filled,bold")

        dir_label = os.path.basename(root) or root
        if data:
            dir_label += f" ({dir_sizes.get(root, '0 bytes')})"
        dir_label += "\l"
        if data and dirs:
            dir_label += f"{len(dirs)} Folder{multiple(len(dirs))}\l"
        if data and files:
            file_memory = convert(sum(os.path.getsize(os.path.join(root, f)) for f in files))
            dir_label += f"{len(files)} File{multiple(len(files))} ({file_memory})\l"

        node_id = os.path.relpath(root, directory)
        tree.node(node_id, label=dir_label)

        for dir_ in dirs:
            child_path = os.path.join(root, dir_)
            child_id = os.path.relpath(child_path, directory)
            tree.node(child_id, label=dir_)
            tree.edge(node_id, child_id)

        if files and show_files:
            index += 1
            tree.attr("node", shape="box", style="")
            file_node_label = "\l".join(files) + "\l"
            file_node_id = f"{node_id}_files_{index}"
            tree.node(file_node_id, label=file_node_label)
            tree.edge(node_id, file_node_id)

    output_filename = filename.rsplit(".", 1)[0] if filename else f"{os.path.basename(directory)}_Graph"
    if render:
        try:
            tree.render(output_filename, format=file_type, cleanup=True)
        except Exception as e:
            raise RuntimeError(f"Graphviz rendering failed: {e}")
    else:
        is_png = file_type == "png"
        url = f'https://quickchart.io/graphviz?{"format=png&" if is_png else ""}graph={tree.source}'
        response = requests.get(url)
        if response.ok:
            mode = "wb" if is_png else "w"
            with open(f"{output_filename}.{file_type}", mode) as f:
                f.write(response.content if is_png else response.text)
        else:
            raise RuntimeError("Error rendering graph with quickchart.io. Graph may be too large.")

def main():
    parser = argparse.ArgumentParser(description="Visualizes directory structure with graphs.")
    parser.add_argument("dir", nargs='?', default=None, help="Root directory path.")
    parser.add_argument("-o", help="Output file name.")
    parser.add_argument("-d", help="Visualization Depth. Default -1.")
    parser.add_argument("-hidden", help='Include hidden directories (starting with "." or "__").', action="store_true")
    parser.add_argument("-m", help="Show number of files/dirs and memory use.", action="store_true")
    parser.add_argument("-f", help="Show files in each directory.", action="store_true")
    parser.add_argument("-ot", help="Graph orientation. Either TB, BT, LR, RL. Default TB.")
    parser.add_argument("-rs", help='Distance between "layers" of directories in inches.')
    parser.add_argument("-ft", help='File Format to render graph as either "svg" or "png". Default "svg".')
    parser.add_argument("-r", help="Render graph online via the quickchart.io API.", action="store_true")
    args = parser.parse_args()

    if args.dir is None:
        args.dir = input("Enter the root directory path: ").strip()

    if not os.path.isdir(args.dir):
        raise NotADirectoryError(f"The path '{args.dir}' is not a valid directory.")

    graph_dir(
        args.dir,
        filename=args.o,
        orientation=args.ot if args.ot else "TB",
        data=args.m,
        show_files=args.f,
        show_hidden=args.hidden,
        max_depth=int(args.d) if args.d else -1,
        ranksep=float(args.rs) if args.rs else None,
        file_type=args.ft if args.ft in ["png", "svg"] else "svg",
        render=args.r,
    )


if __name__ == "__main__":
    main()