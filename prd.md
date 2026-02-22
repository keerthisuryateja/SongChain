# Product Requirements Document: SongChain

## 1. Product Overview
**SongChain** is a music player application built on a linked list data structure implementation in Python. It fetches songs from GaanaPy with yt-dlp as fallback, with automatic category detection from song metadata.
install anything you want

## 2. Core Features

### 2.1 Linked List Operations
- **Count** – Display total number of songs in the playlist
- **Play** – Play the current or selected song
- **Pause** – Pause the currently playing song
- **Next** – Move to and play the next song in the list
- **Previous** – Move to and play the previous song in the list
- **Jump to position** – Navigate directly to a specific index in the playlist
- **Search** – Find songs by title, artist, or other metadata
- **Hide/Unhide** – Toggle visibility of individual songs in the playlist
- **Delete** – Remove a song from the playlist entirely

### 2.2 Queue Management
- **Add to queue** – Place selected song(s) into the playback queue
- **Clear queue** – Remove all songs from the current queue
- **View queue** – Display the current playback queue contents

### 2.3 Category Management
- **Filter by category** – Show only songs belonging to a selected category
- **Sort by category** – Reorganize the playlist based on category
- **Category count** – Display number of songs in each category
- **Fetch categories** – Automatically detect and extract categories from song metadata (via GaanaPy/yt-dlp)

### 2.4 Randomization Features
- **Shuffle play** – Play songs in random order
- **Shuffle list** – Randomize the entire playlist order
- **Shuffle category** – Randomize songs within a specific category
- **Random pick** – Select and play a random song from the playlist
- **Weighted random** – Select random songs with probability weights (e.g., based on play count, user preference)
- **Random queue** – Generate a random playback queue from the playlist
- **Shuffle queue** – Randomize the order of the current queue
- **Add random** – Insert random song(s) into the current queue

### 2.5 Music Source Integration
- **Fetch songs** – Retrieve songs using GaanaPy API
- **yt-dlp fallback** – Automatically use yt-dlp if GaanaPy fails
- **Metadata extraction** – Extract song information including title, artist, duration, and category

## 3. Technical Requirements

### 3.1 Data Structure
- Implement a **doubly linked list** as the core data structure for playlist management
- Each node must contain: song ID, title, artist, URL, duration, category, weight (for weighted random), hidden status

### 3.2 External Integrations
- **GaanaPy** – Primary source for fetching songs and metadata
- **yt-dlp** – Fallback source for song retrieval when GaanaPy unavailable
- Automatic category detection from fetched metadata

## 4. Success Criteria
- All features listed above are functional
- Linked list operations correctly demonstrate data structure behavior
- Smooth playback with queue management
- Reliable song fetching with proper fallback