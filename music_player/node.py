class Node:
    def __init__(self, song_id, title, artist, url, duration, category="Unknown", weight=1.0, hidden_status=False, thumbnail=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.url = url
        self.duration = duration
        self.category = category
        self.weight = weight
        self.hidden_status = hidden_status
        self.thumbnail = thumbnail
        
        # Pointers
        self.prev = None
        self.next = None
        self.original_prev = None # Might be useful for restoring after sort
        self.original_next = None

    def __repr__(self):
        return f"Node({self.title} by {self.artist} [{self.category}])"
