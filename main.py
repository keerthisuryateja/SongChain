import time
import threading
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.panel import Panel

from music_player.playlist import DoublyLinkedList
from music_player.fetcher import SongFetcher
from music_player.audio import AudioPlayer

console = Console()

class SongChainCLI:
    def __init__(self):
        self.playlist = DoublyLinkedList()
        self.fetcher = SongFetcher()
        self.player = AudioPlayer()
        self.is_running = True
        
        # Thread for checking if song has ended to auto-play next
        self.monitor_thread = threading.Thread(target=self._monitor_playback, daemon=True)
        self.monitor_thread.start()

    def _monitor_playback(self):
        while True:
            time.sleep(1)
            if getattr(self, 'is_running', False) and getattr(self, 'player', None):
                if self.player.is_playing() == False and self.player.has_ended():
                    # Song ended, try to play next automatically
                    next_node = self.playlist.next()
                    if next_node:
                        console.print(f"[green]Now Auto-Playing:[/green] {next_node.title}")
                        self.player.play(next_node.url)
                    else:
                        self.player.stop()

    def display_help(self):
        table = Table(title="SongChain Commands")
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")

        table.add_row("fetch <query>", "Fetch and add a song to the playlist")
        table.add_row("play", "Play current song, or resume")
        table.add_row("pause", "Pause current song")
        table.add_row("next", "Play next song in playlist/queue")
        table.add_row("prev", "Play previous song")
        table.add_row("list", "List all songs in playlist")
        table.add_row("queue", "View songs in queue")
        table.add_row("add_queue <index>", "Add a song from playlist to queue")
        table.add_row("clear_queue", "Clear the queue")
        table.add_row("shuffle_list", "Shuffle the entire playlist")
        table.add_row("random_pick", "Play a random song")
        table.add_row("filter <category>", "Filter and show songs by category")
        table.add_row("hide <id>", "Toggle hide/unhide on a song")
        table.add_row("search <query>", "Search playlist")
        table.add_row("jump <index>", "Jump to specific index and play")
        table.add_row("delete <id>", "Delete song from playlist")
        table.add_row("count", "Show total counts")
        table.add_row("quit", "Exit application")
        
        console.print(table)

    def run(self):
        console.print(Panel.fit("[bold violet]Welcome to SongChain[/bold violet]\nA Music Player powered by Python and a Doubly Linked List"))
        self.display_help()
        
        while self.is_running:
            try:
                cmd_input = Prompt.ask("\n[bold green]SONGCHAIN>[/bold green]").strip()
                if not cmd_input:
                    continue
                parts = cmd_input.split(" ", 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                self.handle_command(cmd, args)
            except KeyboardInterrupt:
                self.is_running = False
                console.print("\n[yellow]Exiting...[/yellow]")
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")

    def handle_command(self, cmd: str, args: str):
        if cmd == "quit" or cmd == "exit":
            self.is_running = False
        elif cmd == "help":
            self.display_help()
        elif cmd == "fetch":
            if not args:
                console.print("[red]Please provide a search query.[/red]")
                return
            console.print(f"Fetching [cyan]'{args}'[/cyan]...")
            song_data = self.fetcher.fetch(args)
            if song_data:
                node = self.playlist.add_song(**song_data)
                console.print(f"[green]Added:[/green] {node.title} by {node.artist} ([yellow]{node.category}[/yellow])")
            else:
                console.print("[red]Failed to fetch song.[/red]")
        
        elif cmd == "play":
            if self.playlist.current:
                console.print(f"Playing: {self.playlist.current.title}")
                # Play if we're not currently playing
                if not self.player.is_playing():
                    self.player.play(self.playlist.current.url)
            else:
                console.print("[yellow]No song currently selected. Use 'fetch' to add songs.[/yellow]")
        
        elif cmd == "pause":
            self.player.pause()
            status = "Playing" if self.player.is_playing() else "Paused"
            console.print(f"Playback [yellow]{status}[/yellow]")
            
        elif cmd == "next":
            node = self.playlist.next()
            if node:
                console.print(f"Next: {node.title}")
                self.player.play(node.url)
            else:
                console.print("[yellow]End of playlist.[/yellow]")
                
        elif cmd == "prev":
            node = self.playlist.previous()
            if node:
                console.print(f"Previous: {node.title}")
                self.player.play(node.url)
            else:
                console.print("[yellow]Beginning of playlist.[/yellow]")
                
        elif cmd == "list":
            if self.playlist.count() == 0:
                console.print("[yellow]Playlist is empty.[/yellow]")
                return
            
            table = Table(title="Playlist")
            table.add_column("Idx")
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Artist")
            table.add_column("Category")
            table.add_column("Hidden", justify="center")
            
            curr = self.playlist.head
            idx = 0
            while curr:
                prefix = ">> " if curr == self.playlist.current else "   "
                hidden_str = "[red]Y[/red]" if curr.hidden_status else "[green]N[/green]"
                table.add_row(f"{prefix}{idx}", curr.song_id, curr.title, curr.artist, curr.category, hidden_str)
                curr = curr.next
                idx += 1
            console.print(table)
            
        elif cmd == "queue":
            q = self.playlist.view_queue()
            if not q:
                console.print("[yellow]Queue is empty.[/yellow]")
                return
            console.print("Current Queue:")
            for i, n in enumerate(q):
                console.print(f"{i}: {n.title} by {n.artist}")
                
        elif cmd == "add_queue":
            try:
                idx = int(args)
                node = self.playlist.jump_to(idx)
                if node:
                    self.playlist.add_to_queue(node)
                    console.print(f"Added [green]{node.title}[/green] to queue.")
                else:
                    console.print("[red]Invalid index.[/red]")
            except ValueError:
                console.print("[red]Please provide a valid index number.[/red]")
                
        elif cmd == "clear_queue":
            self.playlist.clear_queue()
            console.print("Queue cleared.")
            
        elif cmd == "shuffle_list":
            self.playlist.shuffle_list()
            console.print("[green]Playlist shuffled.[/green]")
            
        elif cmd == "random_pick":
            node = self.playlist.random_pick()
            if node:
                self.playlist.current = node
                console.print(f"Randomly selected: {node.title}")
                self.player.play(node.url)
                
        elif cmd == "filter":
            results = self.playlist.filter_by_category(args)
            if not results:
                console.print(f"No songs found in category: {args}")
                return
            for r in results:
                console.print(f"{r.title} by {r.artist}")
                
        elif cmd == "hide":
            if self.playlist.toggle_hide(args):
                console.print(f"Toggled hidden status for song {args}.")
            else:
                console.print("[red]Song ID not found.[/red]")
                
        elif cmd == "search":
            results = self.playlist.search(args)
            if not results:
                console.print("No results found.")
                return
            for r in results:
                console.print(f"{r.song_id}: {r.title} by {r.artist}")
                
        elif cmd == "jump":
            try:
                idx = int(args)
                node = self.playlist.jump_to(idx)
                if node:
                    console.print(f"Jumped to: {node.title}")
                    self.player.play(node.url)
                else:
                    console.print("[red]Invalid index.[/red]")
            except ValueError:
                console.print("[red]Please provide a valid index number.[/red]")
                
        elif cmd == "delete":
            if self.playlist.delete(args):
                console.print(f"Deleted song {args}")
            else:
                console.print("[red]Song ID not found.[/red]")
                
        elif cmd == "count":
            console.print(f"Total Songs: {self.playlist.count()}")
            cat_count = self.playlist.category_count()
            if cat_count:
                for cat, count in cat_count.items():
                    console.print(f"- {cat}: {count}")
        else:
            console.print(f"[red]Unknown command: '{cmd}'. Type 'help' for a list of commands.[/red]")

if __name__ == "__main__":
    app = SongChainCLI()
    app.run()
