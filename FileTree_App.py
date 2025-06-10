import os
import io
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from Graphviz_DirGraph import compute_dir_stats, build_dot, render_svg
from graphviz import Digraph
from DF_from_Dir import build_directory_dataframe
from streamlit.components.v1 import html
from ElasticGraph_fromDir import build_directory_network


st.title("📁 File Tree Visualizer")

directory = st.text_input("Directory to visualize", value=os.getcwd())
max_depth = st.slider("Max folder depth", 0, 10, 2)
show_hidden = st.checkbox("Include hidden files/folders", value=False)
render_btn = st.button("Generate Graph")

if render_btn:
    if not os.path.isdir(directory):
        st.error(f"❌ '{directory}' is not a valid directory.")
    else:
        stats = compute_dir_stats(directory)
        dot = build_dot(directory, stats, max_depth=max_depth, show_hidden=show_hidden)
        
        # Attempt inline Graphviz
        try:
            st.graphviz_chart(dot)
        except Exception:
            svg_path = render_svg(dot)
            st.image(svg_path, use_column_width=True)


#------------------------------------------
if st.button("Generate DataFrame"):
    if not os.path.isdir(directory):
        st.error(f"❌ '{directory}' is not a valid directory.")
    else:
        df = build_directory_dataframe(directory)
        st.dataframe(df)

        # CSV output
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="file_tree.csv",
            mime="text/csv",
        )

        # Excel output
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='FileTree')
            writer.close()
        excel_data = output.getvalue()
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="file_tree.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

#------------------------------------------
if st.button("Generate Network Graph"):
    if not os.path.isdir(directory):
        st.error("❌ Not a valid directory.")
    else:
        html_path = build_directory_network(directory)
        safe_path = html_path.replace("/", "/")
        
        # Read and embed the HTML (inline)
        with open(html_path, 'r', encoding='utf-8') as f:
            html(f.read(), height=600)
        
        # Add a button to open in a new tab
        if st.button("Open in new browser tab"):
            js = f"""
            <script>
                window.open("file://{safe_path}", "_blank");
            </script>
            """
            components.html(js)
