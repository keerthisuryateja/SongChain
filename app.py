from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import json
import os
from music_player.playlist import DoublyLinkedList
from music_player.node import Node
from music_player.fetcher import SongFetcher
from music_player.audio import AudioPlayer

app = Flask(__name__)
# Enable CORS for frontend Vite app
CORS(app, supports_credentials=True)

# Global State
playlist = DoublyLinkedList()
fetcher = SongFetcher()
player = AudioPlayer()
is_running = True

# Helper to serialize a Node to JSON
def serialize_node(node):
    if not node:
        return None
    return {
        "song_id": node.song_id,
        "title": node.title,
        "artist": node.artist,
        "duration": node.duration,
        "category": node.category,
        "hidden_status": node.hidden_status,
        "weight": node.weight,
        "url": node.url,
        "thumbnail": node.thumbnail
    }

HISTORY_FILE = "history.json"

def save_history():
    """Save the playlist, queue, and playback state to disk."""
    state = {
        "playlist": [],
        "queue": [],
        "current_id": None,
        "playback_time": 0
    }
    
    # Save playlist
    curr = playlist.head
    while curr:
        state["playlist"].append(serialize_node(curr))
        curr = curr.next
        
    # Save queue
    for q_node in playlist.queue:
        state["queue"].append(serialize_node(q_node))
        
    # Save current
    if playlist.current:
        state["current_id"] = playlist.current.song_id
        
    # Save playback time if playing or paused
    state["playback_time"] = player.get_time()
    
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        print("Failed to save history:", e)

def load_history():
    """Load history and restore state."""
    if not os.path.exists(HISTORY_FILE):
        return
        
    try:
        with open(HISTORY_FILE, "r") as f:
            state = json.load(f)
            
        song_map = {}
        
        # Restore playlist
        for song_data in state.get("playlist", []):
            node = playlist.add_song(
                song_id=song_data["song_id"],
                title=song_data["title"],
                artist=song_data["artist"],
                url=song_data["url"],
                duration=song_data["duration"],
                category=song_data.get("category", "Unknown"),
                weight=song_data.get("weight", 1.0),
                thumbnail=song_data.get("thumbnail")
            )
            node.hidden_status = song_data.get("hidden_status", False)
            song_map[node.song_id] = node
            
        # Restore current
        current_id = state.get("current_id")
        if current_id in song_map:
            playlist.current = song_map[current_id]
            # Don't auto-play on startup, just prepare it. The frontend might send Play.
            
        # Restore queue
        for q_data in state.get("queue", []):
            if q_data["song_id"] in song_map:
                playlist.add_to_queue(song_map[q_data["song_id"]])
                
        # Store initial playback time to resume on first play
        global initial_resume_time
        initial_resume_time = state.get("playback_time", 0)
            
    except Exception as e:
        print("Failed to load history:", e)

initial_resume_time = 0

def app_play(node, start_time=0):
    """Helper to dynamically fetch fresh streaming URL and play it."""
    url = getattr(node, 'url', None)
    if url:
        stream_url = fetcher.get_stream_url(url)
        if stream_url:
            player.play(stream_url, start_time=start_time)
            return True
    return False

def monitor_playback():
    """Background thread to handle 'next' on song end."""
    while is_running:
        time.sleep(1)
        if hasattr(player, 'is_playing') and not player.is_playing() and player.has_ended():
            next_node = playlist.next()
            if next_node:
                try:
                    app_play(next_node)
                except Exception as e:
                    print("Error auto-playing next track:", e)
            else:
                player.stop()
        
        # Periodically save history
        save_history()

# Load history before starting monitor thread
load_history()

# Start background monitor thread
monitor_thread = threading.Thread(target=monitor_playback, daemon=True)
monitor_thread.start()

@app.route("/api/search", methods=["POST"])
def search_and_add():
    data = request.json
    query = data.get("query")
    category_override = data.get("category")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    song_data = fetcher.fetch(query)
    if song_data:
        if category_override:
            song_data["category"] = category_override
            
        node = playlist.add_song(**song_data)
        
        # If queue empty and nothing playing, auto-play
        if not player.is_playing() and playlist.count() == 1:
            playlist.current = node
            app_play(node)
            
        return jsonify({"success": True, "node": serialize_node(node)}), 200
    else:
        return jsonify({"error": "Failed to fetch song"}), 500

@app.route("/api/play", methods=["POST"])
def play():
    global initial_resume_time
    if playlist.current:
        if not player.is_playing():
            # Check if it's currently paused (meaning VLC has the media loaded but is paused)
            import vlc
            if player.player.get_state() == vlc.State.Paused:
                player.pause() # This unpauses in audio.py
            else:
                # Need to start fresh or from history
                start_t = initial_resume_time if initial_resume_time > 0 else 0
                app_play(playlist.current, start_time=start_t)
                initial_resume_time = 0 # Clear it after first use
        return jsonify({"success": True, "node": serialize_node(playlist.current)})
    return jsonify({"error": "No song selected"}), 400

@app.route("/api/pause", methods=["POST"])
def pause():
    player.pause()
    return jsonify({"success": True, "playing": player.is_playing()})

@app.route("/api/next", methods=["POST"])
def next_song():
    global initial_resume_time
    initial_resume_time = 0 # reset history resume time
    node = playlist.next()
    if node:
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "End of playlist"}), 404

@app.route("/api/prev", methods=["POST"])
def prev_song():
    global initial_resume_time
    initial_resume_time = 0
    node = playlist.previous()
    if node:
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "Beginning of playlist"}), 404

@app.route("/api/jump", methods=["POST"])
def jump():
    global initial_resume_time
    initial_resume_time = 0
    data = request.json
    index = data.get("index")
    node = playlist.jump_to(index)
    if node:
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/api/playlist", methods=["GET"])
def get_playlist():
    nodes = []
    curr = playlist.head
    while curr:
        nodes.append(serialize_node(curr))
        curr = curr.next
    return jsonify({
        "playlist": nodes,
        "current": serialize_node(playlist.current)
    })

@app.route("/api/queue", methods=["GET"])
def get_queue():
    nodes = [serialize_node(n) for n in playlist.view_queue()]
    return jsonify({"queue": nodes})

@app.route("/api/queue/add", methods=["POST"])
def add_to_queue():
    data = request.json
    index = data.get("index")
    node = playlist.jump_to(index)
    if node:
        playlist.add_to_queue(node)
        return jsonify({"success": True})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/api/queue/clear", methods=["POST"])
def clear_queue():
    playlist.clear_queue()
    return jsonify({"success": True})

@app.route("/api/queue/shuffle", methods=["POST"])
def shuffle_queue():
    playlist.shuffle_queue()
    return jsonify({"success": True})

@app.route("/api/queue/random", methods=["POST"])
def add_random_to_queue():
    playlist.add_random()
    return jsonify({"success": True})

@app.route("/api/shuffle", methods=["POST"])
def shuffle_list():
    playlist.shuffle_list()
    return jsonify({"success": True})

@app.route("/api/shuffle_category", methods=["POST"])
def shuffle_category():
    data = request.json
    category = data.get("category")
    if not category:
        return jsonify({"error": "No category provided"}), 400
    playlist.shuffle_category(category)
    return jsonify({"success": True})

@app.route("/api/play_category", methods=["POST"])
def play_category():
    data = request.json
    category = data.get("category")
    if not category:
        return jsonify({"error": "No category provided"}), 400
    
    # Filter songs by category
    cat_nodes = playlist.filter_by_category(category)
    if not cat_nodes:
        return jsonify({"error": "No songs in this category"}), 404
        
    # Jump to the first song of this category
    node = cat_nodes[0]
    # Find its index in the actual list
    curr = playlist.head
    idx = 0
    found = False
    while curr:
        if curr == node:
            found = True
            break
        curr = curr.next
        idx += 1
    
    if found:
        playlist.jump_to(idx)
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "Song not found in list"}), 404

@app.route("/api/random_pick", methods=["POST"])
def random_pick():
    global initial_resume_time
    initial_resume_time = 0
    node = playlist.random_pick()
    if node:
        playlist.current = node
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "Playlist empty"}), 404

@app.route("/api/weighted_random", methods=["POST"])
def weighted_random():
    global initial_resume_time
    initial_resume_time = 0
    node = playlist.weighted_random()
    if node:
        playlist.current = node
        app_play(node)
        return jsonify({"success": True, "node": serialize_node(node)})
    return jsonify({"error": "Playlist empty"}), 404

@app.route("/api/toggle_hide", methods=["POST"])
def toggle_hide():
    data = request.json
    song_id = data.get("song_id")
    if playlist.toggle_hide(song_id):
        return jsonify({"success": True})
    return jsonify({"error": "Song not found"}), 404

@app.route("/api/delete", methods=["POST"])
def delete_song():
    data = request.json
    song_id = data.get("song_id")
    if playlist.delete(song_id):
        return jsonify({"success": True})
    return jsonify({"error": "Song not found"}), 404

@app.route("/api/seek", methods=["POST"])
def seek():
    data = request.json
    time_ms = data.get("time", 0)
    player.set_time(time_ms)
    return jsonify({"success": True})

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify({
        "playing": player.is_playing(),
        "current_song": serialize_node(playlist.current),
        "total_songs": playlist.count(),
        "categories": playlist.category_count(),
        "playback_time": player.get_time()
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
