# 2506_FileTreeVisualization
***Goal:*** *App Im writing this te,t to explain to you the motive And reason of this app. It was though as a weekend project g when I wanted to organize my own files and photos in my computers.  I also have many high capacity HD and I know there are many duplicated files.  The pro lem is ghat sometimes they have different name.
Using the windows file explorer demonstrates was not easy or adequate thus I thought of making an app where I can see the file structure visually.  Also a list with the most important info of the files under any specific directory and its children.  That way I could compare the file size and the name.
Making easier to find and delete duplicates.

You just need to write the base directory and have few choices to see the structure.

This app can also be used to explain a project a college or somebody else or to understand the organization of a file system. For example the structure of a software project.

I hope is intituve enough  , for any feedback please send me a message. My email is in my website. Where i will post this app installer as well

At this moment works only for Windows,  if I see 8nterest I will create an installer for other OS

#

## Set up your Environment
This repo contains a requirements.txt file with a list of all the packages and dependencies you will need. Before you install the virtual environment. Before you can start with plotly in Jupyter Lab you have to install node.js (if you haven't done it before).
- Check **Node version**  by run the following commands:
    ```sh
    node -v
    ```
    If you haven't installed it yet, begin at `step_1`. Otherwise, proceed to `step_2`.


### **`macOS`** type the following commands : 

- `Step_1:` Update Homebrew and install Node by following commands:
    ```sh
    brew update
    brew install node
    ```

- `Step_2:` Install the virtual environment and the required packages by following commands:

    ```BASH
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
### **`WindowsOS`** type the following commands :

- `Step_1:` Update Chocolatey and install Node by following commands:
    ```sh
    choco upgrade chocolatey
    choco install nodejs
    ```

- `Step_2:` Install the virtual environment and the required packages by following commands.

   For `PowerShell` CLI :

    ```PowerShell
    pyenv local 3.11.3
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

    For `Git-Bash` CLI :
    ```
    pyenv local 3.11.3
    python -m venv .venv
    source .venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```



