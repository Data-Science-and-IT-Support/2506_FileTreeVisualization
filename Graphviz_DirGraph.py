import os
import subprocess
import requests
from graphviz import Digraph
from typing import Dict

def convert(size: int) -> str:
    kilo = 1024
    units = ["bytes","kB","MB","GB","TB","PB"]
    i = 0
    while size >= kilo and i < len(units)-1:
        size /= kilo; i += 1
    if units[i]=="bytes" and size==1: units[i] = "byte"
    return f"{round(size, 2)} {units[i]}"

def compute_dir_stats(root: str) -> Dict[str, Dict[str,int]]:
    stats: Dict[str, Dict[str,int]] = {}
    for dirpath, _, files in os.walk(root):
        total = 0
        n_files = 0
        for f in files:
            p = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(p)
                n_files += 1
            except OSError:
                continue
        stats[dirpath] = {"n_files": n_files, "total_size": total}
    return stats

def build_dot(root: str, stats: Dict[str, Dict[str,int]], max_depth: int = -1, show_hidden: bool = False) -> Digraph:
    dot = Digraph(format='svg')
    dot.attr(rankdir='LR', overlap='scale', splines='polyline')
    root = os.path.abspath(root)
    for dirpath, info in stats.items():
        rel = os.path.relpath(dirpath, root)
        depth = rel.count(os.sep)
        if 0 <= max_depth < depth:
            continue
        name = os.path.basename(dirpath) or rel
        label = f"{name}\\n{info['n_files']} files, {convert(info['total_size'])}"
        dot.node(rel, label=label, shape='folder', style='filled', fillcolor='lemonchiffon')
        if dirpath != root:
            parent = os.path.relpath(os.path.dirname(dirpath), root)
            dot.edge(parent, rel)
    return dot

def render_svg(dot: Digraph, output_filename: str = "dir_tree.svg") -> str:
    src = dot.source
    try:
        proc = subprocess.run(['dot', '-Tsvg'], input=src.encode(),
                              capture_output=True, check=True)
        svg = proc.stdout.decode()
        open(output_filename, 'w', encoding='utf-8').write(svg)
        return output_filename
    except (FileNotFoundError, subprocess.CalledProcessError):
        resp = requests.get(
            'https://quickchart.io/graphviz', params={'graph': src, 'format': 'svg', 'layout': 'dot'}
        )
        resp.raise_for_status()
        open(output_filename, 'wb').write(resp.content)
        return output_filename
