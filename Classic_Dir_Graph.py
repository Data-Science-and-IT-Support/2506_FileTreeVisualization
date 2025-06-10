import os
import subprocess
import requests
import streamlit as st
from graphviz import Digraph
from typing import Dict

def convert(size: int) -> str:
    kilo = 1024
    units = ["bytes","kB","MB","GB","TB","PB"]
    i = 0
    while size >= kilo and i < len(units)-1:
        size /= kilo; i += 1
    if units[i]=="bytes" and size==1: units[i] = "byte"
    return f"{round(size,2)} {units[i]}"

def compute_dir_stats(root: str) -> Dict[str, Dict[str,int]]:
    stats = {}
    for dirpath, dirs, files in os.walk(root):
        n_files = 0; total = 0
        for f in files:
            p = os.path.join(dirpath, f)
            try:
                size = os.path.getsize(p); total += size; n_files += 1
            except OSError:
                st.warning(f"Skipping inaccessible file {p}")
        stats[dirpath] = {"n_files": n_files, "total_size": total}
    return stats

def build_dot(root: str, stats, max_depth=-1, show_hidden=False) -> str:
    dot = Digraph('G', format='svg')
    dot.attr(rankdir='LR', overlap='scale', splines='polyline')
    root = os.path.abspath(root)
    for dirpath, info in stats.items():
        rel = os.path.relpath(dirpath, root)
        depth = rel.count(os.sep)
        if 0 <= max_depth < depth: continue
        name = os.path.basename(dirpath) or rel
        label = f"{name}\\n{info['n_files']} files, {convert(info['total_size'])}"
        dot.node(rel, label=label, shape='folder', style='filled', fillcolor='lemonchiffon')
        parent = os.path.relpath(os.path.dirname(dirpath), root)
        if dirpath != root:
            dot.edge(parent, rel)
    return dot.source

def render_svg(dot_source: str, filename: str = "dir_tree.svg") -> str:
    """Try local dot, else fallback to QuickChart."""
    try:
        proc = subprocess.run(['dot','-Tsvg'], input=dot_source.encode(), capture_output=True, check=True)
        svg = proc.stdout.decode()
        open(filename,'w', encoding='utf8').write(svg)
        return filename
    except (FileNotFoundError, subprocess.CalledProcessError):
        st.info("Local 'dot' not found; using QuickChart Graphviz API.")
        resp = requests.get(
            'https://quickchart.io/graphviz',
            params={'graph':dot_source, 'format':'svg', 'layout':'dot'}
        )
        if resp.ok:
            open(filename,'wb').write(resp.content)
            return filename
        else:
            resp.raise_for_status()

def display_graph(root_dir: str, max_depth=-1, show_hidden=False):
    stats = compute_dir_stats(root_dir)
    dot_src = build_dot(root_dir, stats, max_depth, show_hidden)
    try:
        # Try to display in Streamlit directly
        st.graphviz_chart(dot_src, use_container_width=True)
    except Exception:
        # Fallback: render SVG and show image
        fname = render_svg(dot_src)
        st.image(fname, use_column_width=True)

if __name__ == "__main__":
    root = 'C:/Users/Email/Desktop/CAM' #os.getcwd()
    display_graph(root, max_depth=2, show_hidden=False)
