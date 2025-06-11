# run_app.py
import streamlit.web.bootstrap
import threading
import time
import webview
import os
import socket

def is_port_open(port, host="localhost"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_streamlit():
    app_path = os.path.join(os.path.dirname(__file__), "FileTree_App.py")
    streamlit.web.bootstrap.run(app_path, command_line=None)

def wait_for_streamlit(port=8501):
    print("Waiting for Streamlit server to start...")
    for _ in range(40):  # Wait up to 20 seconds
        if is_port_open(port):
            print("Streamlit server is running.")
            return True
        time.sleep(0.5)
    print("Streamlit server failed to start.")
    return False

def main():
    # Start Streamlit in background
    threading.Thread(target=start_streamlit, daemon=True).start()

    # Wait until the server is up
    if wait_for_streamlit():
        # Open Streamlit in PyWebView window
        webview.create_window("File Tree Visualization", "http://localhost:8501", width=1200, height=800)
        webview.start()
    else:
        print("Failed to launch Streamlit app.")

if __name__ == "__main__":
    main()
