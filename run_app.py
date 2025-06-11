import webview
import threading
import subprocess
import time

def start_streamlit():
    subprocess.Popen(['streamlit', 'run', 'FileTree_App.py'])
    time.sleep(5)  # Wait for Streamlit to start

if __name__ == "__main__":
    threading.Thread(target=start_streamlit).start()
    webview.create_window("File Tree Visualizer", "http://localhost:8501")
    webview.start()

    