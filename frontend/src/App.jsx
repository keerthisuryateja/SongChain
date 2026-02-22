import React, { useState, useEffect } from 'react';
import {
    Play, Pause, SkipForward, SkipBack, Search, ListMusic,
    Music, Shuffle, ListOrdered, Library, PlusCircle, Trash2, EyeOff, Dices
} from 'lucide-react';
import { api } from './api';

function cleanTitle(title) {
    if (!title) return '';
    // Split by common separators and take the first part
    let cleaned = title.split(/\||\|\||\-|\[/)[0];
    // Remove specific keywords (case insensitive)
    cleaned = cleaned.replace(/full video song/i, '')
        .replace(/video song/i, '')
        .replace(/\(official video\)/i, '')
        .replace(/\(official music video\)/i, '')
        .replace(/lyrical video/i, '')
        .replace(/official audio/i, '')
        .replace(/official/i, '')
        .replace(/8k/i, '')
        .replace(/4k/i, '');
    return cleaned.trim();
}

function App() {
    const [activeTab, setActiveTab] = useState('playlist');
    const [query, setQuery] = useState('');

    const [status, setStatus] = useState(null);
    const [playlistData, setPlaylistData] = useState({ playlist: [], current: null });
    const [queueData, setQueueData] = useState([]);
    const [loading, setLoading] = useState(false);

    const refreshState = async () => {
        try {
            const pl = await api.getPlaylist();
            const st = await api.getStatus();
            const q = await api.getQueue();
            setPlaylistData(pl);
            setStatus(st);
            setQueueData(q.queue || []);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        refreshState();
        const interval = setInterval(refreshState, 1000);
        return () => clearInterval(interval);
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;
        setLoading(true);
        await api.searchAndAdd(query);
        setQuery('');
        await refreshState();
        setLoading(false);
    };

    const handlePlayPause = async () => {
        if (status?.playing) await api.pause();
        else await api.play();
        await refreshState();
    };

    const wrapAction = (fn) => async (...args) => {
        await fn(...args);
        await refreshState();
    };

    return (
        <div className="flex flex-col h-screen bg-surface-950 text-surface-50 font-sans overflow-hidden">
            <div className="flex flex-1 min-h-0 overflow-hidden">

                {/* Sidebar */}
                <aside className="w-56 glass-panel border-r border-surface-700/50 flex flex-col p-5 space-y-6 shrink-0 relative z-10">
                    {/* Logo */}
                    <div className="flex items-center space-x-2 px-1">
                        <div className="w-7 h-7 rounded-lg bg-brand-600 flex items-center justify-center">
                            <Music size={14} className="text-white" />
                        </div>
                        <h1 className="text-base font-semibold text-surface-100">SongChain</h1>
                    </div>

                    {/* Nav */}
                    <nav className="space-y-1 flex-grow">
                        <p className="text-[10px] font-semibold tracking-widest text-surface-500 uppercase mb-2 px-2">Library</p>

                        <button
                            onClick={() => setActiveTab('playlist')}
                            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${activeTab === 'playlist' ? 'bg-brand-600/20 text-brand-300 font-medium' : 'text-surface-400 hover:text-surface-200 hover:bg-surface-800'}`}
                        >
                            <ListMusic size={16} />
                            <span>Playlist</span>
                        </button>

                        <button
                            onClick={() => setActiveTab('queue')}
                            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${activeTab === 'queue' ? 'bg-brand-600/20 text-brand-300 font-medium' : 'text-surface-400 hover:text-surface-200 hover:bg-surface-800'}`}
                        >
                            <ListOrdered size={16} />
                            <span>Up Next</span>
                            {queueData.length > 0 && (
                                <span className="ml-auto bg-brand-600 text-white text-[10px] px-1.5 py-0.5 rounded-full">
                                    {queueData.length}
                                </span>
                            )}
                        </button>

                        <button
                            onClick={() => setActiveTab('categories')}
                            className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-sm transition-colors ${activeTab === 'categories' ? 'bg-brand-600/20 text-brand-300 font-medium' : 'text-surface-400 hover:text-surface-200 hover:bg-surface-800'}`}
                        >
                            <Library size={16} />
                            <span>Categories</span>
                        </button>

                        <div className="pt-4">
                            <p className="text-[10px] font-semibold tracking-widest text-surface-500 uppercase mb-2 px-2">Randomize</p>
                            <button onClick={wrapAction(api.shuffle)} className="w-full flex items-center space-x-3 px-3 py-2 text-surface-400 hover:text-surface-200 hover:bg-surface-800 rounded-lg transition-colors text-sm">
                                <Shuffle size={15} />
                                <span>Shuffle List</span>
                            </button>
                            <button onClick={wrapAction(api.randomPick)} className="w-full flex items-center space-x-3 px-3 py-2 text-surface-400 hover:text-surface-200 hover:bg-surface-800 rounded-lg transition-colors text-sm">
                                <Dices size={15} />
                                <span>Random Pick</span>
                            </button>
                            <button onClick={wrapAction(api.weightedRandom)} className="w-full flex items-center space-x-3 px-3 py-2 text-surface-400 hover:text-surface-200 hover:bg-surface-800 rounded-lg transition-colors text-sm">
                                <Dices size={15} className="opacity-50" />
                                <span>Weighted Pick</span>
                            </button>
                        </div>
                    </nav>

                    {/* Stats */}
                    <div className="text-xs text-surface-500 bg-surface-900/60 p-3 rounded-lg border border-surface-700/40">
                        <div className="flex justify-between mb-1">
                            <span>Library</span>
                            <span className="text-surface-300">{status?.total_songs || 0} songs</span>
                        </div>
                        <div className="flex justify-between">
                            <span>Active</span>
                            <span className="text-surface-300">{playlistData.playlist.filter(n => !n.hidden_status).length} nodes</span>
                        </div>
                    </div>
                </aside>

                {/* Main Content */}
                <div className="flex-1 flex flex-col min-h-0">
                    {/* Tab Content */}
                    <div className="flex-1 overflow-hidden relative">
                        {activeTab === 'playlist' && (
                            <PlaylistView
                                playlistData={playlistData}
                                query={query}
                                setQuery={setQuery}
                                handleSearch={handleSearch}
                                loading={loading}
                                wrapAction={wrapAction}
                            />
                        )}
                        {activeTab === 'queue' && (
                            <QueueView queueData={queueData} wrapAction={wrapAction} />
                        )}
                        {activeTab === 'categories' && (
                            <CategoriesView categories={status?.categories || {}} wrapAction={wrapAction} />
                        )}
                    </div>
                </div>
            </div>

            {/* Player Bar — fixed at bottom of layout */}
            <div className="shrink-0 border-t border-surface-800 bg-surface-900/90 backdrop-blur-xl px-6 py-3 relative z-20">
                <div className="flex items-center justify-between max-w-screen-xl mx-auto">
                    {/* Track info */}
                    <div className="flex items-center flex-1 min-w-0 gap-3">
                        <div className="w-10 h-10 rounded-lg bg-surface-800 flex-shrink-0 flex items-center justify-center border border-surface-700 overflow-hidden">
                            {playlistData.current?.thumbnail ? (
                                <img src={playlistData.current.thumbnail} alt="cover" className="w-full h-full object-cover" />
                            ) : (
                                <Music size={16} className="text-surface-400" />
                            )}
                        </div>
                        <div className="min-w-0">
                            <h4 className="font-medium text-sm text-surface-100 truncate">
                                {cleanTitle(playlistData.current?.title) || 'No track selected'}
                            </h4>
                            <p className="text-xs text-surface-500 truncate">
                                {playlistData.current?.artist || 'Fetch a song to play'}
                            </p>
                        </div>
                    </div>

                    {/* Controls */}
                    <div className="flex flex-col items-center justify-center flex-1 px-4 min-w-[300px]">
                        <div className="flex items-center justify-center gap-4 shrink-0 mb-1.5">
                            <button onClick={wrapAction(api.prev)} className="text-surface-400 hover:text-surface-100 transition-colors active:scale-95">
                                <SkipBack size={20} fill="currentColor" />
                            </button>
                            <button
                                onClick={handlePlayPause}
                                disabled={!playlistData.current}
                                className="w-10 h-10 bg-brand-600 hover:bg-brand-500 text-white rounded-full flex items-center justify-center transition-all shadow-md active:scale-95 disabled:opacity-40 disabled:hover:bg-brand-600"
                            >
                                {status?.playing
                                    ? <Pause size={18} fill="currentColor" />
                                    : <Play size={18} fill="currentColor" className="ml-0.5" />
                                }
                            </button>
                            <button onClick={wrapAction(api.next)} className="text-surface-400 hover:text-surface-100 transition-colors active:scale-95">
                                <SkipForward size={20} fill="currentColor" />
                            </button>
                        </div>
                        <ProgressBar
                            playbackTimeMs={status?.playback_time}
                            durationSec={playlistData.current?.duration}
                            onSeek={async (val) => {
                                await api.seek(val);
                                await refreshState();
                            }}
                        />
                    </div>

                    {/* Right info */}
                    <div className="flex-1 flex justify-end min-w-0">
                        <span className="text-xs text-surface-600 font-medium truncate">Linked List Driver</span>
                    </div>
                </div>
            </div>
        </div>
    );
}

// ==============
// Sub Views
// ==============

function PlaylistView({ playlistData, query, setQuery, handleSearch, loading, wrapAction }) {
    return (
        <div className="flex flex-col h-full">
            <header className="px-8 pt-8 pb-5 flex justify-between items-center border-b border-surface-800 shrink-0">
                <div>
                    <h2 className="text-2xl font-semibold text-surface-50">Your Station</h2>
                    <p className="text-sm text-surface-500 mt-0.5">Doubly Linked List</p>
                </div>
                <form onSubmit={handleSearch} className="relative w-72">
                    <Search className="absolute left-3 top-2.5 text-surface-500" size={15} />
                    <input
                        type="text"
                        placeholder="Search YouTube..."
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        disabled={loading}
                        className="w-full bg-surface-800 border border-surface-700 rounded-lg py-2 pl-9 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/50 focus:border-brand-500/50 text-surface-100 placeholder:text-surface-500 disabled:opacity-50 transition"
                    />
                </form>
            </header>
            <div className="flex-1 overflow-y-auto px-8 py-4 space-y-1.5 custom-scrollbar">
                {playlistData.playlist.length === 0 ? (
                    <EmptyState icon={Music} text="Playlist is empty. Search to add songs!" />
                ) : (
                    playlistData.playlist.map((song, index) => {
                        const isCurrent = playlistData.current?.song_id === song.song_id;
                        return (
                            <div
                                key={song.song_id}
                                className={`glass-card px-4 py-3 flex items-center group ${song.hidden_status ? 'opacity-40' : ''} ${isCurrent ? 'border-brand-500/40 bg-brand-600/10' : ''}`}
                            >
                                <div className="w-8 text-center text-surface-600 text-xs font-mono">{index}</div>
                                <div className="w-10 h-10 rounded-md bg-surface-800 ml-2 overflow-hidden flex-shrink-0 border border-surface-700 flex items-center justify-center">
                                    {song.thumbnail ? <img src={song.thumbnail} className="w-full h-full object-cover" /> : <Music size={14} className="text-surface-500" />}
                                </div>
                                <div className="flex-1 ml-3 truncate cursor-pointer" onClick={wrapAction(() => api.jump(index))}>
                                    <h3 className={`font-medium text-sm truncate ${isCurrent ? 'text-brand-300' : 'text-surface-100'} ${song.hidden_status ? 'line-through' : ''}`}>
                                        {cleanTitle(song.title)}
                                    </h3>
                                    <p className="text-xs text-surface-500 truncate">{song.artist}</p>
                                </div>
                                <span className="shrink-0 px-2 py-0.5 mx-3 rounded-md bg-surface-900 border border-surface-700 text-xs text-surface-400">
                                    {song.category}
                                </span>
                                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
                                    <button title="Play" onClick={wrapAction(() => api.jump(index))} className="p-1.5 hover:bg-surface-700 rounded-md text-surface-400 hover:text-surface-100 transition-colors">
                                        <Play size={14} fill="currentColor" />
                                    </button>
                                    <button title="Add to Queue" onClick={wrapAction(() => api.addToQueue(index))} className="p-1.5 hover:bg-surface-700 rounded-md text-surface-400 hover:text-surface-100 transition-colors">
                                        <PlusCircle size={14} />
                                    </button>
                                    <button title={song.hidden_status ? 'Unhide' : 'Hide'} onClick={wrapAction(() => api.toggleHide(song.song_id))} className="p-1.5 hover:bg-surface-700 rounded-md text-surface-400 hover:text-yellow-400 transition-colors">
                                        <EyeOff size={14} />
                                    </button>
                                    <button title="Delete" onClick={wrapAction(() => api.delete(song.song_id))} className="p-1.5 hover:bg-red-900/40 rounded-md text-surface-400 hover:text-red-400 transition-colors">
                                        <Trash2 size={14} />
                                    </button>
                                </div>
                            </div>
                        );
                    })
                )}
            </div>
        </div>
    );
}

function QueueView({ queueData, wrapAction }) {
    return (
        <div className="flex flex-col h-full">
            <header className="px-8 pt-8 pb-5 flex justify-between items-center border-b border-surface-800 shrink-0">
                <div>
                    <h2 className="text-2xl font-semibold text-surface-50">Up Next</h2>
                    <p className="text-sm text-surface-500 mt-0.5">Playback queue</p>
                </div>
                <div className="flex items-center gap-2">
                    <button onClick={wrapAction(api.addRandomToQueue)} className="glass-button px-3 py-1.5 flex items-center gap-2 text-sm text-surface-300">
                        <PlusCircle size={14} />
                        <span>Add Random</span>
                    </button>
                    <button onClick={wrapAction(api.shuffleQueue)} className="glass-button px-3 py-1.5 flex items-center gap-2 text-sm text-surface-300">
                        <Shuffle size={14} />
                        <span>Shuffle</span>
                    </button>
                    <button onClick={wrapAction(api.clearQueue)} className="glass-button px-3 py-1.5 flex items-center gap-2 text-sm text-red-400 hover:text-red-300 hover:bg-red-900/30">
                        <Trash2 size={14} />
                        <span>Clear</span>
                    </button>
                </div>
            </header>
            <div className="flex-1 overflow-y-auto px-8 py-4 space-y-1.5 custom-scrollbar">
                {queueData.length === 0 ? (
                    <EmptyState icon={ListOrdered} text="Queue is empty. Add songs from your playlist!" />
                ) : (
                    queueData.map((song, i) => (
                        <div key={i + song.song_id} className="glass-card px-4 py-3 flex items-center">
                            <div className="w-8 text-center text-surface-600 text-xs font-mono">{i + 1}</div>
                            <div className="w-10 h-10 rounded-md bg-surface-800 ml-2 overflow-hidden flex-shrink-0 border border-surface-700 flex items-center justify-center">
                                {song.thumbnail ? <img src={song.thumbnail} className="w-full h-full object-cover" /> : <Music size={14} className="text-surface-500" />}
                            </div>
                            <div className="flex-1 ml-3 truncate">
                                <h3 className="font-medium text-sm truncate text-surface-100">{cleanTitle(song.title)}</h3>
                                <p className="text-xs text-surface-500 truncate">{song.artist}</p>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

function CategoriesView({ categories, wrapAction }) {
    const catEntries = Object.entries(categories);
    return (
        <div className="flex flex-col h-full">
            <header className="px-8 pt-8 pb-5 border-b border-surface-800 shrink-0">
                <h2 className="text-2xl font-semibold text-surface-50">Categories</h2>
                <p className="text-sm text-surface-500 mt-0.5">Auto-detected clusters from metadata</p>
            </header>
            <div className="flex-1 overflow-y-auto px-8 py-4 custom-scrollbar">
                {catEntries.length === 0 ? (
                    <EmptyState icon={Library} text="No categories found yet." />
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {catEntries.map(([catName, count]) => (
                            <div key={catName} className="glass-card p-5 flex flex-col gap-3 h-36 group hover:border-brand-500/40">
                                <div>
                                    <h3 className="text-base font-semibold text-surface-50">{catName}</h3>
                                    <p className="text-sm text-surface-500">{count} Track(s)</p>
                                </div>
                                <button onClick={wrapAction(() => api.shuffleCategory(catName))} className="self-start flex items-center gap-2 text-surface-500 hover:text-brand-400 transition-colors opacity-0 group-hover:opacity-100 text-sm">
                                    <Shuffle size={14} />
                                    <span>Shuffle</span>
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function EmptyState({ icon: Icon, text }) {
    return (
        <div className="flex flex-col items-center justify-center h-full text-surface-600 space-y-3 py-20">
            <Icon size={40} className="opacity-20" />
            <p className="text-sm">{text}</p>
        </div>
    );
}

function formatTime(ms) {
    if (!ms || ms < 0) return "0:00";
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

function ProgressBar({ playbackTimeMs, durationSec, onSeek }) {
    const [localTime, setLocalTime] = useState(0);
    const [isDragging, setIsDragging] = useState(false);

    const totalMs = (durationSec || 0) * 1000;

    useEffect(() => {
        if (!isDragging) {
            setLocalTime(playbackTimeMs || 0);
        }
    }, [playbackTimeMs, isDragging]);

    const handleSeek = (e) => {
        const val = parseInt(e.target.value, 10);
        setLocalTime(val);
    };

    const handleSeekCommit = async (e) => {
        const val = parseInt(e.target.value, 10);
        setIsDragging(false);
        await onSeek(val);
    };

    return (
        <div className="flex items-center gap-3 w-full max-w-md mx-auto">
            <span className="text-[10px] text-surface-500 font-mono w-8 text-right">{formatTime(localTime)}</span>
            <input
                type="range"
                min={0}
                max={totalMs || 100}
                value={localTime}
                onChange={handleSeek}
                onMouseDown={() => setIsDragging(true)}
                onMouseUp={handleSeekCommit}
                onTouchStart={() => setIsDragging(true)}
                onTouchEnd={handleSeekCommit}
                className="flex-1 h-1 bg-surface-700 rounded-lg appearance-none cursor-pointer accent-brand-500"
                disabled={!durationSec}
            />
            <span className="text-[10px] text-surface-500 font-mono w-8">{formatTime(totalMs)}</span>
        </div>
    );
}

export default App;
