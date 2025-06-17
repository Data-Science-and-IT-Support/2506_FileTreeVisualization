# 2506_FileTreeVisualization
***Explanation:*** 
Hi there, I hope you are fine. 
I will attempt here to explain to you the motive And reason of this app. It was though as a weekend project. I wanted to organize my own files and photos in my computers.  I have many high capacity HD and there are many duplicated files in most unexpected places.  Sometimes they have the same content but the filename is different.*

Using the windows file explorer was not enough and more difficult that it should. Thus I thought of making an app where I can see the file tree structure visually more than one level down. I also wanted an excel, CSV or Dataframe file with the most important info of the whole tree file so I could search for duolicates, compare file date creation and size, etc. making easier to identify duplicates.

Of course knowing you file tree structure is also very helpful to understand your projects, repos, etc. It can be used also to explain a project structire to someone else, a colleage, student, etc.

I may create new version if needed, for this one I used streamlit as UI, which unfortunately does not have a file picker.

That is why you just need to write in the input box the "root" (base) directory and then select your  choices of hidden or not hidden and how many levels down of the structure you want to explore.

I hope is intituve enough, for any feedback please send me a message. My email is in my website: www.jesusbasail.com Where you will be able to download this app. 

At this moment works only for Windows, on demand other OS would be available.

---

The followng section is regarding the repo setup, not the App itslef. 

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



