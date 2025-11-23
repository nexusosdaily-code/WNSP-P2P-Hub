# WNSP Media Player - User Interface

This directory contains the HTML/CSS/JavaScript user-facing media player for WNSP.

## Architecture

```
static/
├── index.html           # Main media player interface
├── css/
│   └── media_player.css # Styling (Netflix/Spotify-inspired)
├── js/
│   └── media_player.js  # Interactivity and media controls
├── media/               # Media files (videos, audio, documents)
│   ├── video/
│   ├── audio/
│   └── docs/
└── thumbnails/          # Preview images
```

## Features

### Current Implementation (Demo/Frontend Only)
✅ **Modern UI/UX**
- Netflix-inspired video player interface
- Spotify-inspired audio player with playlist support
- Responsive mobile-first design
- Dark theme with smooth animations

✅ **Media Browsing**
- Category filtering (University, Refugee, Rural, Crisis)
- Search functionality
- Grid layout with thumbnails
- Media metadata display

✅ **Playback Controls**
- Video player with fullscreen support
- Audio player with play/pause, skip, shuffle, repeat
- Progress bar and time tracking
- Volume control
- Document viewer (PDF support)

✅ **Network Status Display**
- Mesh network connectivity indicator
- Node count display
- Cache statistics
- Energy cost tracking (E=hf)

### Next Steps (Backend Integration)
🔄 **WNSP Integration Required**
- Connect media files to actual WNSP chunk streaming
- Implement progressive download with buffering
- Real-time cache status from mesh nodes
- Live energy cost calculation during playback
- Multi-hop propagation path visualization

## Usage

### Standalone Mode (Demo)
```bash
python wnsp_media_server.py
```
Visit: http://0.0.0.0:5000

### With WNSP Backend (Production)
The server automatically detects WNSP backend availability and integrates:
- Real media library from `wnsp_media_propagation_production.py`
- Live propagation statistics
- Actual chunk-based streaming
- Mesh network topology integration

## API Endpoints

- `GET /` - Media player interface
- `GET /api/media/library` - Get media library
- `GET /api/media/<id>` - Get specific media file
- `GET /api/stats` - Get network statistics
- `POST /api/propagate` - Propagate media chunk
- `GET /api/health` - Health check

## Design Philosophy

**User-First Approach:**
- Beautiful, intuitive interface that people want to use
- Real human interaction generates real data (not simulations)
- Mobile-optimized for phone-based mesh networking
- Offline-first design for intermittent connectivity

**Physics-Based Foundation:**
- E=hf energy costs displayed transparently
- Wavelength-based chunk validation
- Mesh topology routing visualization
- Conservation laws enforced

## License

GPL v3.0 - Community ownership, no corporate exploitation
