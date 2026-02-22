import vlc
import time

class AudioPlayer:
    def __init__(self):
        # Create a VLC instance and media player
        self.instance = vlc.Instance("--no-xlib", "--quiet")
        self.player = self.instance.media_player_new()
        self._is_playing = False

    def play(self, url: str, start_time: int = 0) -> bool:
        """
        Play a stream from a given URL.
        """
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        self._is_playing = True
        
        if start_time > 0:
            # We must wait for the media player to be ready before setting time
            time.sleep(0.5)
            # Setting time in milliseconds
            self.player.set_time(start_time)

        # Give it a moment to start so we can check if it fails immediately
        time.sleep(0.5)
        
        # Check vlc state
        state = self.player.get_state()
        if state == vlc.State.Error:
            self._is_playing = False
            return False
            
        return True

    def pause(self):
        if self._is_playing:
            self.player.pause()
            self._is_playing = False
        else:
            # Unpause if it's already paused
            state = self.player.get_state()
            if state == vlc.State.Paused:
                self.player.play()
                self._is_playing = True

    def stop(self):
        self.player.stop()
        self._is_playing = False

    def is_playing(self) -> bool:
        state = self.player.get_state()
        return state == vlc.State.Playing

    def has_ended(self) -> bool:
        state = self.player.get_state()
        return state == vlc.State.Ended

    def get_time(self) -> int:
        return self.player.get_time()
        
    def set_time(self, time_ms: int):
        self.player.set_time(time_ms)
