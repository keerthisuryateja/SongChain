# SongChain: Your New Favorite Playlist (Probably) 🎶

Welcome to SongChain! This is a simple, fun music player built with Python and React. It uses a **doubly linked list** under the hood to manage your songs—because why use a normal list when you can use a linked one? 😉

Whether you're a coding wizard or just someone who wants to play some tunes, this guide will help you get SongChain up and running on your local machine. No jargon, no stress. Let's do this!

## 🛠️ Prerequisites

Before we start, make sure you have these installed on your computer:

1.  **Python** (3.8 or newer): The brain of our operation. [Download it here](https://www.python.org/downloads/).
2.  **Node.js** (14 or newer): Needed for the shiny frontend. [Download it here](https://nodejs.org/).
3.  **VLC Media Player**: We use this to play the audio. **Important:** This is the actual VLC app, not a Python package. Make sure it's installed on your system! [Get it here](https://www.videolan.org/vlc/).

## 🚀 Getting Started

### Step 1: Download the Code
First things first, get the code onto your machine. If you're reading this, you probably already have it. If not, click the big green "Code" button and select "Download ZIP", then unzip it.

### Step 2: Set Up the Backend (The Python Part)
Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux) and navigate to the project folder.

1.  **Create a virtual environment** (think of this as a safe playground for Python packages):
    ```bash
    python -m venv venv
    ```
    *(If `python` doesn't work, try `python3`)*

2.  **Activate the environment**:
    -   **Windows:** `venv\Scripts\activate`
    -   **Mac/Linux:** `source venv/bin/activate`

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the backend server**:
    ```bash
    python app.py
    ```
    You should see a message saying it's running on `http://127.0.0.1:5000`. Keep this terminal window open!

### Step 3: Set Up the Frontend (The React Part)
Open a **new** terminal window (leave the previous one running) and navigate to the `frontend` folder inside the project.

1.  **Go to the frontend folder**:
    ```bash
    cd frontend
    ```

2.  **Install the frontend dependencies**:
    ```bash
    npm install
    ```

3.  **Start the frontend**:
    ```bash
    npm run dev
    ```
    You'll see a link like `http://localhost:5173`.

### Step 4: Let the Music Play! 🎧
Open your web browser and go to `http://localhost:5173`. You should see the SongChain interface!

### 🎵 Add Some Tunes
Right now, your playlist might be empty. Let's fix that!
In your **backend terminal** (the first one), you can stop the server (Ctrl+C), run this command, and then start `app.py` again:

```bash
python populate_songs.py
```
This will fetch a bunch of cool songs for you automatically. Then restart the app with `python app.py`.

## ❓ Troubleshooting

-   **"VLC not found" error?**
    Make sure you installed the actual VLC Media Player app on your computer. If you're on Mac, it needs to be in `/Applications`.

-   **"Port already in use"?**
    Make sure you don't have another instance of the app running. If you do, close those terminal windows and try again.

-   **Songs not playing?**
    Sometimes YouTube links expire or get blocked. Try adding a new song using the "Fetch" button in the app.

That's it! Enjoy your music. 🎸
