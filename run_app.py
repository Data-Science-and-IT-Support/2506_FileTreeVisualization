import subprocess
import threading
import time
import webview
import socket
import os
import logging

logging.basicConfig(filename="run_app.log", level=logging.DEBUG)

def is_port_open(port, host="localhost"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_streamlit():
    base_dir = os.path.dirname(__file__)
    python_exe = os.path.join(base_dir, "_internal", "python.exe")  # REAL Python, not PyInstaller .exe
    app_path = os.path.join(base_dir, "_internal", "FileTree_App.py")

    command = [
        python_exe,
        "-m", "streamlit",
        "run", app_path,
        "--server.port=8501",
        "--server.headless=true"
    ]

    logging.debug("Launching Streamlit with: " + ' '.join(command))
    print("Running:", ' '.join(command))

    try:
        subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except Exception as e:
        logging.error(f"❌ Failed to launch Streamlit: {e}")
        print("❌ Failed to launch Streamlit:", e)

def wait_for_server():
    logging.debug("Waiting for Streamlit server to start...")
    print("Waiting for Streamlit server to start...")
    for _ in range(40):
        if is_port_open(8501):
            logging.debug("Streamlit server is running.")
            return True
        time.sleep(0.5)
    logging.error("Streamlit server failed to start.")
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
