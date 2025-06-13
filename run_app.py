# run_app.py
import subprocess
import threading
import time
import webview
import os
import socket
import sys


import logging
logging.basicConfig(filename="run_app.log", level=logging.DEBUG)

def is_port_open(port, host="localhost"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_streamlit():
    import subprocess
    import os

    # Absolute or relative path to your bundled streamlit.exe
    streamlit_path = os.path.join(os.path.dirname(__file__), "streamlit.exe")
    app_path = os.path.join(os.path.dirname(__file__), "FileTree_App.py")

    print(f"Running: {streamlit_path} run {app_path}")

    try:
        proc = subprocess.Popen(
            [streamlit_path, "run", app_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in proc.stderr:
            print("[Streamlit STDERR]", line.strip())

    except Exception as e:
        print("❌ Failed to launch Streamlit:", e)

def wait_for_server():
    print("Waiting for Streamlit server to start...")
    for _ in range(40):
        if is_port_open(8501):
            print("Streamlit server is running.")
            return True
        time.sleep(0.5)
    print("Streamlit server failed to start.")
    return False

def main():
    threading.Thread(target=start_streamlit, daemon=True).start()
    if wait_for_server():
        webview.create_window("File Tree Viewer", "http://localhost:8501", width=1200, height=800)
        webview.start()
    else:
        print("Failed to start Streamlit.")

if __name__ == "__main__":
    main()
