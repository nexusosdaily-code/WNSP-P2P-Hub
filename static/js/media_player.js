// WNSP Media Player - JavaScript Controller
// GPL v3.0 License

// Media Library Data (from WNSP backend)
const mediaLibrary = [
    // University Content
    {
        id: 'univ_001',
        category: 'university',
        type: 'video',
        title: 'Quantum Mechanics Lecture 1',
        artist: 'Prof. Sarah Chen',
        description: 'Introduction to wave-particle duality and the foundations of quantum mechanics',
        size: 245.5,
        duration: '01:32:15',
        thumbnail: '🎓',
        energyCost: 0.0245,
        cached: true,
        url: '#' // Will be replaced with actual media URL
    },
    {
        id: 'univ_002',
        category: 'university',
        type: 'audio',
        title: 'Physics of Blockchain',
        artist: 'Dr. James Liu',
        description: 'Audio lecture on thermodynamics applied to distributed systems',
        size: 48.3,
        duration: '45:20',
        thumbnail: '🎵',
        energyCost: 0.0048,
        cached: true,
        url: '#'
    },
    {
        id: 'univ_003',
        category: 'university',
        type: 'document',
        title: 'Advanced Mathematics Textbook',
        artist: 'MIT OpenCourseWare',
        description: 'Complete calculus and linear algebra reference',
        size: 12.8,
        duration: 'PDF',
        thumbnail: '📘',
        energyCost: 0.0013,
        cached: false,
        url: '#'
    },
    {
        id: 'univ_004',
        category: 'university',
        type: 'video',
        title: 'Laboratory Safety Protocol',
        artist: 'Campus Safety Team',
        description: 'Essential lab safety procedures and emergency response',
        size: 156.2,
        duration: '28:45',
        thumbnail: '🔬',
        energyCost: 0.0156,
        cached: true,
        url: '#'
    },
    // Refugee Resources
    {
        id: 'ref_001',
        category: 'refugee',
        type: 'document',
        title: 'Legal Rights Guide',
        artist: 'UNHCR',
        description: 'Know your rights: asylum, documentation, and legal assistance',
        size: 8.4,
        duration: 'PDF',
        thumbnail: '⚖️',
        energyCost: 0.0008,
        cached: true,
        url: '#'
    },
    {
        id: 'ref_002',
        category: 'refugee',
        type: 'audio',
        title: 'Basic English Lessons',
        artist: 'Language Support Network',
        description: 'Essential English phrases for daily communication',
        size: 35.6,
        duration: '38:12',
        thumbnail: '🗣️',
        energyCost: 0.0036,
        cached: true,
        url: '#'
    },
    {
        id: 'ref_003',
        category: 'refugee',
        type: 'document',
        title: 'Safe Route Maps',
        artist: 'Community Mapping Project',
        description: 'Verified safe routes and checkpoint locations',
        size: 5.2,
        duration: 'PDF',
        thumbnail: '🗺️',
        energyCost: 0.0005,
        cached: false,
        url: '#'
    },
    {
        id: 'ref_004',
        category: 'refugee',
        type: 'video',
        title: 'Medical First Aid Training',
        artist: 'Red Cross',
        description: 'Basic first aid and emergency medical response',
        size: 189.4,
        duration: '42:18',
        thumbnail: '🏥',
        energyCost: 0.0189,
        cached: true,
        url: '#'
    },
    // Rural Communities
    {
        id: 'rural_001',
        category: 'rural',
        type: 'video',
        title: 'Sustainable Farming Techniques',
        artist: 'Agricultural Extension Service',
        description: 'Modern crop rotation and soil management methods',
        size: 312.7,
        duration: '56:30',
        thumbnail: '🌱',
        energyCost: 0.0313,
        cached: true,
        url: '#'
    },
    {
        id: 'rural_002',
        category: 'rural',
        type: 'document',
        title: 'Community Health Guide',
        artist: 'WHO Rural Health Initiative',
        description: 'Disease prevention and basic healthcare practices',
        size: 6.9,
        duration: 'PDF',
        thumbnail: '💊',
        energyCost: 0.0007,
        cached: true,
        url: '#'
    },
    {
        id: 'rural_003',
        category: 'rural',
        type: 'audio',
        title: 'Market Price Updates',
        artist: 'Farmers Cooperative Network',
        description: 'Weekly commodity prices and market trends',
        size: 15.2,
        duration: '18:45',
        thumbnail: '📊',
        energyCost: 0.0015,
        cached: false,
        url: '#'
    },
    // Crisis Response
    {
        id: 'crisis_001',
        category: 'crisis',
        type: 'document',
        title: 'Emergency Evacuation Plan',
        artist: 'Emergency Management Agency',
        description: 'Evacuation routes and assembly point locations',
        size: 3.8,
        duration: 'PDF',
        thumbnail: '🚨',
        energyCost: 0.0004,
        cached: true,
        url: '#'
    },
    {
        id: 'crisis_002',
        category: 'crisis',
        type: 'document',
        title: 'Emergency Contact Directory',
        artist: 'Local Response Team',
        description: 'Critical contact numbers for emergency services',
        size: 2.1,
        duration: 'PDF',
        thumbnail: '📞',
        energyCost: 0.0002,
        cached: true,
        url: '#'
    },
    {
        id: 'crisis_003',
        category: 'crisis',
        type: 'video',
        title: 'Search & Rescue Coordination',
        artist: 'Emergency Response Unit',
        description: 'Rescue operation protocols and communication procedures',
        size: 201.5,
        duration: '35:22',
        thumbnail: '🚁',
        energyCost: 0.0202,
        cached: false,
        url: '#'
    },
    {
        id: 'crisis_004',
        category: 'crisis',
        type: 'audio',
        title: 'Crisis Alert Broadcast',
        artist: 'Civil Defense',
        description: 'Emergency alert system test and instructions',
        size: 8.7,
        duration: '12:30',
        thumbnail: '📡',
        energyCost: 0.0009,
        cached: true,
        url: '#'
    }
];

// Global State
let currentCategory = 'all';
let currentMedia = null;
let audioPlaylist = [];
let currentAudioIndex = 0;
let isShuffleOn = false;
let isRepeatOn = false;

// DOM Elements
const mediaGrid = document.getElementById('mediaGrid');
const searchInput = document.getElementById('searchInput');
const categoryButtons = document.querySelectorAll('.category-btn');
const nowPlayingSection = document.getElementById('nowPlayingSection');
const videoPlayerWrapper = document.getElementById('videoPlayerWrapper');
const audioPlayerWrapper = document.getElementById('audioPlayerWrapper');
const documentViewerWrapper = document.getElementById('documentViewerWrapper');
const videoPlayer = document.getElementById('videoPlayer');
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const shuffleBtn = document.getElementById('shuffleBtn');
const repeatBtn = document.getElementById('repeatBtn');
const progressBar = document.getElementById('progressBar');
const progressFill = document.getElementById('progressFill');
const currentTimeEl = document.getElementById('currentTime');
const durationEl = document.getElementById('duration');
const volumeSlider = document.getElementById('volumeSlider');

// Initialize App
function init() {
    renderMediaGrid();
    attachEventListeners();
    updateNetworkStats();
}

// Render Media Grid
function renderMediaGrid(filter = 'all', searchTerm = '') {
    mediaGrid.innerHTML = '';
    
    let filteredMedia = mediaLibrary;
    
    // Category filter
    if (filter !== 'all') {
        filteredMedia = filteredMedia.filter(item => item.category === filter);
    }
    
    // Search filter
    if (searchTerm) {
        filteredMedia = filteredMedia.filter(item =>
            item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
            item.artist.toLowerCase().includes(searchTerm.toLowerCase())
        );
    }
    
    // Render cards
    filteredMedia.forEach(media => {
        const card = createMediaCard(media);
        mediaGrid.appendChild(card);
    });
    
    // Show message if no results
    if (filteredMedia.length === 0) {
        mediaGrid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">No content found</p>';
    }
}

// Create Media Card
function createMediaCard(media) {
    const card = document.createElement('div');
    card.className = 'media-card';
    card.onclick = () => playMedia(media);
    
    const typeEmoji = media.type === 'video' ? '▶️' : media.type === 'audio' ? '🎵' : '📄';
    const typeLabel = media.type.charAt(0).toUpperCase() + media.type.slice(1);
    
    card.innerHTML = `
        <div class="media-thumbnail">
            ${media.thumbnail}
            <span class="media-type-badge">${typeEmoji} ${typeLabel}</span>
        </div>
        <div class="media-content">
            <h3 class="media-title">${media.title}</h3>
            <div class="media-meta">
                <span>👤 ${media.artist}</span>
                ${media.duration !== 'PDF' ? `<span>⏱️ ${media.duration}</span>` : ''}
            </div>
            <p class="media-description">${media.description}</p>
            <div class="media-footer">
                <div class="cache-status">
                    ${media.cached ? '✅ Cached' : '⬇️ Download'}
                </div>
                <div class="energy-cost">
                    ⚡ ${media.energyCost.toFixed(4)} NXT
                </div>
            </div>
        </div>
    `;
    
    return card;
}

// Play Media
function playMedia(media) {
    currentMedia = media;
    nowPlayingSection.style.display = 'block';
    nowPlayingSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    
    // Hide all players
    videoPlayerWrapper.style.display = 'none';
    audioPlayerWrapper.style.display = 'none';
    documentViewerWrapper.style.display = 'none';
    
    if (media.type === 'video') {
        playVideo(media);
    } else if (media.type === 'audio') {
        playAudio(media);
    } else if (media.type === 'document') {
        viewDocument(media);
    }
    
    updateNetworkStats();
}

// Play Video
function playVideo(media) {
    videoPlayerWrapper.style.display = 'block';
    document.getElementById('videoTitle').textContent = media.title;
    document.getElementById('videoMeta').textContent = `${media.artist} • ${media.duration} • ${media.size} MB`;
    
    // In production, this would load actual video file
    // For demo, show message
    videoPlayer.poster = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450"><rect fill="%23252540" width="800" height="450"/><text x="50%" y="50%" fill="%2394a3b8" text-anchor="middle" font-family="Arial" font-size="24">📹 ' + encodeURIComponent(media.title) + '</text><text x="50%" y="60%" fill="%236366f1" text-anchor="middle" font-family="Arial" font-size="16">Connect to WNSP network to stream</text></svg>';
}

// Play Audio
function playAudio(media) {
    audioPlayerWrapper.style.display = 'block';
    document.getElementById('audioTitle').textContent = media.title;
    document.getElementById('audioArtist').textContent = media.artist;
    document.getElementById('coverArt').textContent = media.thumbnail;
    
    // Build playlist from current category
    audioPlaylist = mediaLibrary.filter(item => item.type === 'audio' && item.category === media.category);
    currentAudioIndex = audioPlaylist.findIndex(item => item.id === media.id);
    
    // In production, this would load actual audio file
    // audioPlayer.src = media.url;
    // audioPlayer.play();
}

// View Document
function viewDocument(media) {
    documentViewerWrapper.style.display = 'block';
    document.getElementById('documentTitle').textContent = media.title;
    document.getElementById('documentMeta').textContent = `${media.artist} • ${media.size} MB`;
    
    // In production, this would load actual PDF
    const viewer = document.getElementById('documentViewer');
    viewer.srcdoc = `
        <html>
        <body style="margin: 0; padding: 40px; font-family: Arial; background: #f5f5f5; color: #333;">
            <div style="max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h1 style="color: #6366f1; margin-bottom: 20px;">${media.thumbnail} ${media.title}</h1>
                <p style="color: #666; margin-bottom: 30px;"><strong>Author:</strong> ${media.artist}</p>
                <hr style="border: none; border-top: 2px solid #eee; margin: 30px 0;">
                <p style="line-height: 1.8; color: #444;">${media.description}</p>
                <div style="margin-top: 40px; padding: 20px; background: #f8f9ff; border-left: 4px solid #6366f1; border-radius: 4px;">
                    <p style="margin: 0; color: #6366f1; font-weight: bold;">📡 WNSP Network Status</p>
                    <p style="margin: 10px 0 0 0; color: #666; font-size: 14px;">This document is available on the mesh network. Energy cost: ${media.energyCost} NXT</p>
                </div>
                <div style="margin-top: 30px; text-align: center; color: #999; font-size: 14px;">
                    <p>Connect to WNSP network to view full document</p>
                    <p style="margin-top: 10px;">GPL v3.0 License • Community Knowledge Network</p>
                </div>
            </div>
        </body>
        </html>
    `;
}

// Audio Controls
function togglePlayPause() {
    if (audioPlayer.paused) {
        audioPlayer.play();
        playPauseBtn.textContent = '⏸️';
    } else {
        audioPlayer.pause();
        playPauseBtn.textContent = '▶️';
    }
}

function playPrevious() {
    if (currentAudioIndex > 0) {
        currentAudioIndex--;
        playAudio(audioPlaylist[currentAudioIndex]);
    }
}

function playNext() {
    if (isShuffleOn) {
        currentAudioIndex = Math.floor(Math.random() * audioPlaylist.length);
    } else if (currentAudioIndex < audioPlaylist.length - 1) {
        currentAudioIndex++;
    } else if (isRepeatOn) {
        currentAudioIndex = 0;
    }
    
    if (audioPlaylist[currentAudioIndex]) {
        playAudio(audioPlaylist[currentAudioIndex]);
    }
}

function toggleShuffle() {
    isShuffleOn = !isShuffleOn;
    shuffleBtn.style.color = isShuffleOn ? 'var(--primary-color)' : 'var(--text-primary)';
}

function toggleRepeat() {
    isRepeatOn = !isRepeatOn;
    repeatBtn.style.color = isRepeatOn ? 'var(--primary-color)' : 'var(--text-primary)';
}

function updateProgress() {
    const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progressFill.style.width = `${progress}%`;
    currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
    durationEl.textContent = formatTime(audioPlayer.duration);
}

function seekAudio(e) {
    const rect = progressBar.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    audioPlayer.currentTime = percent * audioPlayer.duration;
}

function updateVolume() {
    audioPlayer.volume = volumeSlider.value / 100;
}

function formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Category Filter
function filterByCategory(category) {
    currentCategory = category;
    renderMediaGrid(category, searchInput.value);
    
    // Update active button
    categoryButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.category === category) {
            btn.classList.add('active');
        }
    });
}

// Search
function handleSearch() {
    renderMediaGrid(currentCategory, searchInput.value);
}

// Update Network Stats
function updateNetworkStats() {
    // Calculate stats
    const totalCached = mediaLibrary.filter(m => m.cached).length;
    const totalSize = mediaLibrary.reduce((sum, m) => sum + (m.cached ? m.size : 0), 0);
    const totalEnergy = mediaLibrary.reduce((sum, m) => sum + (m.cached ? m.energyCost : 0), 0);
    const cacheHitRate = Math.round((totalCached / mediaLibrary.length) * 100);
    
    // Update UI
    document.getElementById('cacheSize').textContent = `${totalSize.toFixed(1)} MB`;
    document.getElementById('energySpent').textContent = totalEnergy.toFixed(4);
    document.getElementById('propagations').textContent = totalCached * 3; // Simulated
    document.getElementById('cacheHitRate').textContent = `${cacheHitRate}%`;
}

// Attach Event Listeners
function attachEventListeners() {
    // Category buttons
    categoryButtons.forEach(btn => {
        btn.addEventListener('click', () => filterByCategory(btn.dataset.category));
    });
    
    // Search
    searchInput.addEventListener('input', handleSearch);
    
    // Audio controls
    if (playPauseBtn) playPauseBtn.addEventListener('click', togglePlayPause);
    if (prevBtn) prevBtn.addEventListener('click', playPrevious);
    if (nextBtn) nextBtn.addEventListener('click', playNext);
    if (shuffleBtn) shuffleBtn.addEventListener('click', toggleShuffle);
    if (repeatBtn) repeatBtn.addEventListener('click', toggleRepeat);
    if (progressBar) progressBar.addEventListener('click', seekAudio);
    if (volumeSlider) volumeSlider.addEventListener('input', updateVolume);
    
    // Audio player events
    if (audioPlayer) {
        audioPlayer.addEventListener('timeupdate', updateProgress);
        audioPlayer.addEventListener('ended', playNext);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
