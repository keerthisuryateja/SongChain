const API_BASE = 'http://127.0.0.1:5000/api';

export const api = {
    async getStatus() {
        const res = await fetch(`${API_BASE}/status`);
        return res.json();
    },
    async getPlaylist() {
        const res = await fetch(`${API_BASE}/playlist`);
        return res.json();
    },
    async getQueue() {
        const res = await fetch(`${API_BASE}/queue`);
        return res.json();
    },
    async searchAndAdd(query) {
        const res = await fetch(`${API_BASE}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        return res.json();
    },
    async play() {
        const res = await fetch(`${API_BASE}/play`, { method: 'POST' });
        return res.json();
    },
    async pause() {
        const res = await fetch(`${API_BASE}/pause`, { method: 'POST' });
        return res.json();
    },
    async next() {
        const res = await fetch(`${API_BASE}/next`, { method: 'POST' });
        return res.json();
    },
    async prev() {
        const res = await fetch(`${API_BASE}/prev`, { method: 'POST' });
        return res.json();
    },
    async jump(index) {
        const res = await fetch(`${API_BASE}/jump`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ index })
        });
        return res.json();
    },
    async seek(time) {
        const res = await fetch(`${API_BASE}/seek`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ time })
        });
        return res.json();
    },
    async shuffle() {
        const res = await fetch(`${API_BASE}/shuffle`, { method: 'POST' });
        return res.json();
    },
    async delete(song_id) {
        const res = await fetch(`${API_BASE}/delete`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song_id })
        });
        return res.json();
    },
    async toggleHide(song_id) {
        const res = await fetch(`${API_BASE}/toggle_hide`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ song_id })
        });
        return res.json();
    },

    // Queue modifications
    async addToQueue(index) {
        const res = await fetch(`${API_BASE}/queue/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ index })
        });
        return res.json();
    },
    async clearQueue() {
        const res = await fetch(`${API_BASE}/queue/clear`, { method: 'POST' });
        return res.json();
    },
    async shuffleQueue() {
        const res = await fetch(`${API_BASE}/queue/shuffle`, { method: 'POST' });
        return res.json();
    },
    async addRandomToQueue() {
        const res = await fetch(`${API_BASE}/queue/random`, { method: 'POST' });
        return res.json();
    },

    // Randomization Extensions
    async randomPick() {
        const res = await fetch(`${API_BASE}/random_pick`, { method: 'POST' });
        return res.json();
    },
    async weightedRandom() {
        const res = await fetch(`${API_BASE}/weighted_random`, { method: 'POST' });
        return res.json();
    },
    async shuffleCategory(category) {
        const res = await fetch(`${API_BASE}/shuffle_category`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category })
        });
        return res.json();
    },
    async playCategory(category) {
        const res = await fetch(`${API_BASE}/play_category`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category })
        });
        return res.json();
    }
};
