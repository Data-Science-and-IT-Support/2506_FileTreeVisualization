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


import logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)
#logging.debug("Streamlit app started")

st.title("📁 File Tree Visualizer 2025")
st.write("Hi there, about this App: It was though as a weekend project. \n\n I wanted to organize my own files and photos in my computers.  I have many high capacity HD's and there are many duplicated files in the most unexpected places.  Sometimes they have the same content but the filename is different. Using the windows file explorer was not enough and more difficult than it should. \n\n Thus, I thought of making an app where I can see the file tree structure visually with more than one level down. I also wanted an excel, CSV or Dataframe file with the most important Information of the whole tree file, so I could compare file date creation, size, etc. making easier to identify duplicates. \n\n Of course knowing you file tree structure is also very helpful to understand your projects, repos, etc. It can be used also to explain a project structure to someone else, for example a colleage or a student. \n I may create a new version if needed; for this one I used streamlit as UI, which unfortunately does not have a file picker. \n That is why you just need to write in the input box the 'root'  (base) directory and then select your  choices of hidden, not hidden, how many levels down, etc. \n\n I hope is intituve enough, for any feedback please send me a message. My email is in my website: www.jesusbasail.com Where you will be able to download this app")

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
st.write("The Dataframe choice, ignores the 'Max Folder Depth' option and creates a complete depth Dataframe.")
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
st.write("This is the most time consuming, experimental option. Be careful. It creates a cool elastic graphic but takes a long time and pops out a browser tab that reads it needs Internet connection, but is not true, well, not all the time. Please close that tab. The graph will show here, but be patient.")

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
        #if st.button("Open in new browser tab"):
        #    js = f"""
        #    <script>
        #        window.open("file://{safe_path}", "_blank");
        #    </script>
        #    """
        #    components.html(js)
