import random
from typing import Optional, List, Dict
from music_player.node import Node

class DoublyLinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.current: Optional[Node] = None
        self.queue: List[Node] = []
        self._length = 0

    def add_song(self, song_id, title, artist, url, duration, category="Unknown", weight=1.0, thumbnail=None):
        new_node = Node(song_id, title, artist, url, duration, category, weight, thumbnail=thumbnail)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._length += 1
        return new_node

    def count(self) -> int:
        return self._length

    def delete(self, song_id: str) -> bool:
        curr = self.head
        while curr:
            if curr.song_id == song_id:
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                
                if self.current == curr:
                    self.current = curr.next if curr.next else curr.prev
                
                self._length -= 1
                return True
            curr = curr.next
        return False

    def next(self) -> Optional[Node]:
        if self.queue:
            return self.queue.pop(0)

        if self.current and self.current.next:
            # Skip hidden statuses
            curr = self.current.next
            while curr and curr.hidden_status:
                curr = curr.next
            self.current = curr
            return self.current
        return None

    def previous(self) -> Optional[Node]:
        if self.current and self.current.prev:
            curr = self.current.prev
            while curr and curr.hidden_status:
                curr = curr.prev
            self.current = curr
            return self.current
        return None

    def jump_to(self, index: int) -> Optional[Node]:
        if index < 0 or index >= self.count():
            return None
        
        curr = self.head
        for _ in range(index):
            if curr:
                curr = curr.next
        self.current = curr
        return self.current

    def search(self, query: str) -> List[Node]:
        results = []
        query = query.lower()
        curr = self.head
        while curr:
            if query in curr.title.lower() or query in curr.artist.lower() or query in curr.category.lower():
                results.append(curr)
            curr = curr.next
        return results

    def toggle_hide(self, song_id: str) -> bool:
        curr = self.head
        while curr:
            if curr.song_id == song_id:
                curr.hidden_status = not curr.hidden_status
                return True
            curr = curr.next
        return False

    # Queue Management
    def add_to_queue(self, node: Node):
        self.queue.append(node)

    def clear_queue(self):
        self.queue.clear()

    def view_queue(self) -> List[Node]:
        return list(self.queue)

    # Category Management
    def filter_by_category(self, category: str) -> List[Node]:
        results = []
        curr = self.head
        while curr:
            if curr.category.lower() == category.lower():
                results.append(curr)
            curr = curr.next
        return results

    def category_count(self) -> Dict[str, int]:
        counts = {}
        curr = self.head
        while curr:
            counts[curr.category] = counts.get(curr.category, 0) + 1
            curr = curr.next
        return counts

    def get_all_nodes(self) -> List[Node]:
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr)
            curr = curr.next
        return nodes

    # Randomization Features
    def shuffle_list(self):
        nodes = self.get_all_nodes()
        random.shuffle(nodes)
        self._rebuild_links(nodes)

    def _rebuild_links(self, nodes: List[Node]):
        self.head = None
        self.tail = None
        self._length = 0
        for n in nodes:
            n.prev = None
            n.next = None
            if not self.head:
                self.head = n
                self.tail = n
            else:
                self.tail.next = n
                n.prev = self.tail
                self.tail = n
            self._length += 1
        
        if self.current not in nodes:
            self.current = self.head

    def shuffle_category(self, category: str):
        nodes = self.get_all_nodes()
        cat_nodes = [n for n in nodes if n.category.lower() == category.lower()]
        other_nodes = [n for n in nodes if n.category.lower() != category.lower()]
        
        random.shuffle(cat_nodes)
        
        # We need a strategy to weave them back. For simplicity, just append cat_nodes at the end of other_nodes.
        # A more robust approach would maintain exact original positions of other_nodes.
        # Let's do that: maintain original indices for others.
        
        indices = [i for i, n in enumerate(nodes) if n.category.lower() == category.lower()]
        random.shuffle(indices)
        
        new_nodes = list(nodes)
        for i, matched_node in zip(indices, cat_nodes):
            new_nodes[i] = matched_node
            
        self._rebuild_links(new_nodes)

    def random_pick(self) -> Optional[Node]:
        if self._length == 0:
            return None
        nodes = self.get_all_nodes()
        return random.choice(nodes)

    def weighted_random(self) -> Optional[Node]:
        if self._length == 0:
            return None
        nodes = self.get_all_nodes()
        weights = [n.weight for n in nodes]
        return random.choices(nodes, weights=weights, k=1)[0]

    def shuffle_queue(self):
        random.shuffle(self.queue)

    def add_random(self):
        pick = self.random_pick()
        if pick:
            self.add_to_queue(pick)
