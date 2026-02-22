import yt_dlp
import uuid

class SongFetcher:
    def __init__(self):
        # Configuration for yt-dlp
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'noplaylist': True,
        }

    def fetch(self, query: str):
        """
        Attempts to fetch a song from Gaana API (if available),
        otherwise falls back to yt-dlp.
        """
        try:
            return self._fetch_gaana(query)
        except Exception:
            return self._fetch_ytdlp(query)

    def _fetch_gaana(self, query: str):
        """
        Stub for GaanaPy fetching.
        Raises an exception to trigger yt-dlp fallback if not implemented or unavailable.
        """
        try:
            import gaanapy
            # Using GaanaPy unofficial API if it exists on the system
            # As a simplified placeholder, if this fails, we go to yt-dlp
            raise NotImplementedError("GaanaPy integration not fully available.")
        except ImportError:
            raise NotImplementedError("GaanaPy not installed.")

    def _fetch_ytdlp(self, query: str):
        """
        Uses yt-dlp to search for the query and extract stream URL + metadata.
        Returns a dictionary or None
        """
        # Ensure we just search for 1 result
        search_query = f"ytsearch1:{query}"
        
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(search_query, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    entry = info['entries'][0]
                    
                    category = entry.get('categories', ['Unknown'])[0] if entry.get('categories') else 'Unknown'
                    
                    # We store the webpage_url to persist in history without expiring.
                    # We will resolve it at playback time.
                    webpage_url = entry.get('webpage_url')
                    if not webpage_url or "googlevideo.com" in webpage_url:
                        # Fallback to reconstructing youtube link if possible
                        webpage_url = f"https://www.youtube.com/watch?v={entry.get('id')}" if entry.get('id') else entry.get('url')
                    
                    return {
                        'song_id': str(uuid.uuid4())[:8],
                        'title': entry.get('title', 'Unknown Title'),
                        'artist': entry.get('uploader', 'Unknown Artist'),
                        'url': webpage_url,
                        'duration': entry.get('duration', 0),
                        'category': category,
                        'thumbnail': entry.get('thumbnail')
                    }
                return None
            except Exception as e:
                print(f"Error fetching from yt-dlp: {e}")
                return None

    def get_stream_url(self, url: str) -> str:
        """Resolves a webpage URL to a direct streaming URL on the fly."""
        # If it's already a direct stream, just return it
        if "googlevideo.com" in url: return url
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info and len(info['entries']) > 0:
                    return info['entries'][0].get('url')
                return info.get('url', url)
        except Exception as e:
            print(f"Error extracting stream link: {e}")
            return None
