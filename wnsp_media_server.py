#!/usr/bin/env python3
"""
WNSP Media Server - Standalone HTML/CSS/JS Media Player
GPL v3.0 License
Serves the user-facing media player interface and integrates with WNSP backend
"""

from flask import Flask, send_from_directory, jsonify, request, Response, send_file
from flask_cors import CORS
import socketio as sio
from werkzeug.utils import secure_filename
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import production file manager
try:
    from wnsp_media_file_manager import media_manager
    FILE_MANAGER_AVAILABLE = True
except ImportError:
    FILE_MANAGER_AVAILABLE = False
    print("⚠️  File manager not available")

# Import WNSP backend
try:
    from wnsp_unified_mesh_stack import create_demo_network
    from wnsp_media_propagation_production import WNSPMediaPropagationProduction
    WNSP_AVAILABLE = True
except ImportError:
    WNSP_AVAILABLE = False
    print("⚠️  WNSP backend not available - running in standalone mode")

app = Flask(__name__, static_folder='static')
CORS(app)

# Create Socket.IO server with python-socketio (not flask-socketio)
sio_server = sio.Server(async_mode='threading', cors_allowed_origins='*')
app.wsgi_app = sio.WSGIApp(sio_server, app.wsgi_app)

# Security: Enforce maximum upload size (100MB)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# LiveStream state management
active_broadcasts = {}  # broadcaster_id -> {room_id, title, category, viewer_count}
active_viewers = {}     # viewer_socket_id -> broadcaster_id

# Error handler for file too large
@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file size exceeded error"""
    return jsonify({
        'error': 'File too large. Maximum upload size is 100MB.',
        'uploaded': 0,
        'files': []
    }), 413

# Lazy initialization globals
mesh_stack = None
media_engine = None
_wnsp_init_attempted = False

def get_media_engine():
    """Lazy-load WNSP media engine on first request"""
    global mesh_stack, media_engine, _wnsp_init_attempted, WNSP_AVAILABLE
    
    if not WNSP_AVAILABLE:
        return None
    
    if media_engine is not None:
        return media_engine
    
    if _wnsp_init_attempted:
        return None
    
    _wnsp_init_attempted = True
    
    try:
        print("🔄 Initializing WNSP Media Engine...")
        mesh_stack = create_demo_network()
        media_engine = WNSPMediaPropagationProduction(mesh_stack=mesh_stack)
        print("✅ WNSP Media Engine initialized")
        return media_engine
    except Exception as e:
        print(f"⚠️  WNSP Engine initialization failed: {e}")
        WNSP_AVAILABLE = False
        return None

@app.route('/')
def index():
    """Serve the main media player page"""
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, media)"""
    return send_from_directory('static', path)

@app.route('/api/media/library')
def get_media_library():
    """Get complete media library"""
    # Try file manager first (production)
    if FILE_MANAGER_AVAILABLE and len(media_manager.media_library) > 0:
        try:
            library = media_manager.get_library_summary()
            return jsonify({
                'success': True,
                'data': library,
                'source': 'file_manager'
            })
        except Exception as e:
            print(f"File manager error: {e}")
    
    # Fallback to WNSP engine (simulation)
    engine = get_media_engine()
    if engine:
        try:
            library = engine.get_library_summary()
            return jsonify({
                'success': True,
                'data': library,
                'source': 'wnsp_backend'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e),
                'source': 'wnsp_backend'
            }), 500
    else:
        return jsonify({
            'success': False,
            'error': 'No media source available',
            'source': 'none'
        }), 503

@app.route('/api/media/<media_id>')
def get_media_file(media_id):
    """Get specific media file metadata"""
    engine = get_media_engine()
    if engine:
        try:
            # Get file from media engine
            if media_id in engine.media_library:
                media_file = engine.media_library[media_id]
                return jsonify({
                    'success': True,
                    'data': {
                        'id': media_file.file_id,
                        'filename': media_file.filename,
                        'size': media_file.file_size,
                        'chunks': len(media_file.chunks),
                        'category': media_file.category,
                        'content_hash': media_file.content_hash
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Media not found'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    else:
        return jsonify({
            'success': False,
            'error': 'WNSP backend not available'
        }), 503

@app.route('/api/stats')
def get_network_stats():
    """Get WNSP network statistics"""
    engine = get_media_engine()
    if engine:
        try:
            stats = engine.get_propagation_statistics()
            return jsonify({
                'success': True,
                'data': stats
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    else:
        return jsonify({
            'success': True,
            'data': {
                'total_files': 15,
                'total_chunks_created': 0,
                'total_propagations': 0,
                'total_energy_spent_nxt': 0.0,
                'cache_hit_rate': 0,
                'dedup_rate': 0,
                'total_hops_traveled': 0
            }
        })

@app.route('/api/propagate', methods=['POST'])
def propagate_media():
    """Propagate media chunk to node"""
    engine = get_media_engine()
    if not engine:
        return jsonify({
            'success': False,
            'error': 'WNSP backend not available'
        }), 503
    
    try:
        data = request.json
        chunk_id = data.get('chunk_id')
        from_node = data.get('from_node')
        to_node = data.get('to_node')
        
        if not all([chunk_id, from_node, to_node]):
            return jsonify({
                'success': False,
                'error': 'Missing required parameters'
            }), 400
        
        success = engine.propagate_chunk_to_node(chunk_id, from_node, to_node)
        
        return jsonify({
            'success': success,
            'message': 'Chunk propagated successfully' if success else 'Propagation failed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/upload', methods=['POST'])
def upload_media():
    """
    Handle file uploads to WNSP network
    Accepts: MP3, MP4, PDF files
    """
    if not FILE_MANAGER_AVAILABLE:
        return jsonify({'error': 'File manager not available'}), 503
    
    # Check if files were uploaded
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    category = request.form.get('category', 'university')
    
    # Validate category
    valid_categories = ['university', 'refugee', 'rural', 'crisis']
    if category not in valid_categories:
        return jsonify({'error': f'Invalid category. Must be one of: {valid_categories}'}), 400
    
    uploaded_files = []
    errors = []
    
    # Process each file
    for file in files:
        if file.filename == '':
            continue
        
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Validate file extension
        allowed_extensions = ['.mp3', '.mp4', '.pdf']
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            errors.append(f'{filename}: Invalid file type. Only MP3, MP4, PDF allowed.')
            continue
        
        # Check file size (max 100MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 100 * 1024 * 1024:
            errors.append(f'{filename}: File too large (max 100MB).')
            continue
        
        # Save file to media directory
        media_dir = os.path.join('static', 'media')
        os.makedirs(media_dir, exist_ok=True)
        
        filepath = os.path.join(media_dir, filename)
        
        # If file exists, add timestamp to avoid overwrite
        if os.path.exists(filepath):
            import time
            base, ext = os.path.splitext(filename)
            filename = f'{base}_{int(time.time())}{ext}'
            filepath = os.path.join(media_dir, filename)
        
        try:
            # Save file to disk
            file.save(filepath)
            
            # Ingest file into WNSP network with category metadata
            media_id = media_manager.ingest_file(filepath, category=category)
            
            uploaded_files.append({
                'filename': filename,
                'id': media_id,
                'category': category
            })
        except Exception as e:
            errors.append(f'{filename}: Upload failed - {str(e)}')
    
    # Return results
    response = {
        'uploaded': len(uploaded_files),
        'files': uploaded_files,
        'category': category
    }
    
    if errors:
        response['errors'] = errors
    
    return jsonify(response), 200 if uploaded_files else 400

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'wnsp_available': WNSP_AVAILABLE,
        'file_manager_available': FILE_MANAGER_AVAILABLE,
        'version': '1.0.0'
    })

@app.route('/media/<file_id>/stream')
def stream_media(file_id):
    """
    Stream media file with HTTP range request support
    Enables video/audio seeking and progressive download
    """
    if not FILE_MANAGER_AVAILABLE:
        return jsonify({'error': 'File manager not available'}), 503
    
    # Get media file from manager
    if file_id not in media_manager.media_library:
        return jsonify({'error': 'Media file not found'}), 404
    
    media_file = media_manager.media_library[file_id]
    
    # Get file path
    filepath = media_file.filepath
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found on disk'}), 404
    
    # Get file size
    file_size = os.path.getsize(filepath)
    
    # Handle range requests (for video/audio seeking)
    range_header = request.headers.get('Range', None)
    
    if range_header:
        # Parse range header (e.g., "bytes=0-1023")
        byte_range = range_header.strip().split('=')[1]
        start, end = byte_range.split('-')
        start = int(start) if start else 0
        end = int(end) if end else file_size - 1
        
        # Get file bytes in range
        data = media_manager.get_file_bytes(file_id, start, end)
        
        if data is None:
            return jsonify({'error': 'Failed to read file'}), 500
        
        # Build response with partial content
        response = Response(
            data,
            206,  # Partial Content
            mimetype=media_file.mime_type,
            direct_passthrough=True
        )
        
        response.headers.add('Content-Range', f'bytes {start}-{end}/{file_size}')
        response.headers.add('Accept-Ranges', 'bytes')
        response.headers.add('Content-Length', str(len(data)))
        response.headers.add('Content-Type', media_file.mime_type)
        
        return response
    else:
        # No range request - send entire file
        try:
            return send_file(
                filepath,
                mimetype=media_file.mime_type,
                as_attachment=False,
                conditional=True
            )
        except Exception as e:
            return jsonify({'error': f'Streaming failed: {str(e)}'}), 500

# ============================================================================
# WEBRTC SIGNALING (MESH-NATIVE)
# ============================================================================

@sio_server.event
def connect(sid, environ):
    """Client connects to signaling server"""
    print(f"📡 Client connected: {sid}")
    sio_server.emit('connected', {'message': 'Connected to WNSP LiveStream Network'}, to=sid)

@socketio.on('start_broadcast')
def handle_start_broadcast(data):
    """Broadcaster initiates livestream with consent"""
    broadcaster_id = request.sid
    title = data.get('title', 'Untitled Stream')
    category = data.get('category', 'university')
    
    # Create broadcast room
    room_id = f"broadcast_{broadcaster_id}"
    active_broadcasts[broadcaster_id] = {
        'room_id': room_id,
        'title': title,
        'category': category,
        'viewer_count': 0,
        'started_at': os.times().elapsed
    }
    
    join_room(room_id)
    
    print(f"📹 Broadcast started: {title} ({category}) - Room: {room_id}")
    
    emit('broadcast_started', {
        'success': True,
        'broadcaster_id': broadcaster_id,
        'room_id': room_id
    })
    
    # Notify all clients about new broadcast (mesh discovery)
    socketio.emit('broadcast_available', {
        'broadcaster_id': broadcaster_id,
        'title': title,
        'category': category,
        'room_id': room_id
    }, skip_sid=broadcaster_id)

@socketio.on('stop_broadcast')
def handle_stop_broadcast():
    """Broadcaster ends livestream"""
    broadcaster_id = request.sid
    
    if broadcaster_id in active_broadcasts:
        broadcast = active_broadcasts[broadcaster_id]
        room_id = broadcast['room_id']
        
        # Notify all viewers
        socketio.emit('broadcast_ended', {
            'broadcaster_id': broadcaster_id,
            'message': 'Broadcast has ended'
        }, room=room_id)
        
        leave_room(room_id)
        del active_broadcasts[broadcaster_id]
        
        print(f"📹 Broadcast stopped: {broadcaster_id}")
        
        emit('broadcast_stopped', {'success': True})

@socketio.on('join_broadcast')
def handle_join_broadcast(data):
    """Viewer requests to join broadcast with consent"""
    viewer_id = request.sid
    broadcaster_id = data.get('broadcaster_id')
    
    if broadcaster_id not in active_broadcasts:
        emit('join_failed', {'error': 'Broadcast not found'})
        return
    
    broadcast = active_broadcasts[broadcaster_id]
    room_id = broadcast['room_id']
    
    # Join room
    join_room(room_id)
    active_viewers[viewer_id] = broadcaster_id
    broadcast['viewer_count'] += 1
    
    print(f"👁️  Viewer {viewer_id} joined broadcast {broadcaster_id}")
    
    # Notify viewer they've joined
    emit('joined_broadcast', {
        'success': True,
        'broadcaster_id': broadcaster_id,
        'title': broadcast['title'],
        'category': broadcast['category']
    })
    
    # Notify broadcaster of new viewer
    socketio.emit('viewer_joined', {
        'viewer_id': viewer_id,
        'viewer_count': broadcast['viewer_count']
    }, room=broadcaster_id)

@socketio.on('leave_broadcast')
def handle_leave_broadcast():
    """Viewer leaves broadcast"""
    viewer_id = request.sid
    
    if viewer_id in active_viewers:
        broadcaster_id = active_viewers[viewer_id]
        
        if broadcaster_id in active_broadcasts:
            broadcast = active_broadcasts[broadcaster_id]
            broadcast['viewer_count'] -= 1
            room_id = broadcast['room_id']
            
            leave_room(room_id)
            
            # Notify broadcaster
            socketio.emit('viewer_left', {
                'viewer_id': viewer_id,
                'viewer_count': broadcast['viewer_count']
            }, room=broadcaster_id)
        
        del active_viewers[viewer_id]
        print(f"👁️  Viewer {viewer_id} left broadcast")

@socketio.on('webrtc_offer')
def handle_webrtc_offer(data):
    """Forward WebRTC SDP offer via mesh (hybrid direct + relay)"""
    target_id = data.get('target')
    offer = data.get('offer')
    
    print(f"🔗 WebRTC offer: {request.sid} → {target_id}")
    
    # Forward SDP offer to target peer
    socketio.emit('webrtc_offer', {
        'from': request.sid,
        'offer': offer
    }, room=target_id)

@socketio.on('webrtc_answer')
def handle_webrtc_answer(data):
    """Forward WebRTC SDP answer via mesh"""
    target_id = data.get('target')
    answer = data.get('answer')
    
    print(f"🔗 WebRTC answer: {request.sid} → {target_id}")
    
    # Forward SDP answer to target peer
    socketio.emit('webrtc_answer', {
        'from': request.sid,
        'answer': answer
    }, room=target_id)

@socketio.on('webrtc_ice')
def handle_webrtc_ice(data):
    """Forward ICE candidate via mesh"""
    target_id = data.get('target')
    candidate = data.get('candidate')
    
    # Forward ICE candidate to target peer
    socketio.emit('webrtc_ice', {
        'from': request.sid,
        'candidate': candidate
    }, room=target_id)

@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnects - cleanup broadcasts/viewers"""
    client_id = request.sid
    
    # Check if broadcaster
    if client_id in active_broadcasts:
        broadcast = active_broadcasts[client_id]
        room_id = broadcast['room_id']
        
        # Notify all viewers
        socketio.emit('broadcast_ended', {
            'broadcaster_id': client_id,
            'message': 'Broadcaster disconnected'
        }, room=room_id)
        
        del active_broadcasts[client_id]
        print(f"📹 Broadcaster disconnected: {client_id}")
    
    # Check if viewer
    if client_id in active_viewers:
        broadcaster_id = active_viewers[client_id]
        
        if broadcaster_id in active_broadcasts:
            broadcast = active_broadcasts[broadcaster_id]
            broadcast['viewer_count'] -= 1
            
            socketio.emit('viewer_left', {
                'viewer_id': client_id,
                'viewer_count': broadcast['viewer_count']
            }, room=broadcaster_id)
        
        del active_viewers[client_id]
        print(f"👁️  Viewer disconnected: {client_id}")

@app.route('/api/live/broadcasts')
def get_active_broadcasts():
    """Get list of active livestreams"""
    broadcasts = [
        {
            'broadcaster_id': bid,
            'title': data['title'],
            'category': data['category'],
            'viewer_count': data['viewer_count'],
            'room_id': data['room_id']
        }
        for bid, data in active_broadcasts.items()
    ]
    
    return jsonify({
        'success': True,
        'broadcasts': broadcasts,
        'total': len(broadcasts)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🌐 WNSP Media Server Starting...")
    print("=" * 60)
    print(f"📺 Media Player: http://0.0.0.0:5000")
    print(f"🔧 WNSP Backend: {'✅ Available' if WNSP_AVAILABLE else '⚠️  Standalone Mode'}")
    print(f"📂 File Manager: {'✅ Available' if FILE_MANAGER_AVAILABLE else '⚠️  Not Available'}")
    print(f"📡 API Endpoints: http://0.0.0.0:5000/api/")
    print(f"📹 LiveStream: ✅ WebRTC + Mesh Relay")
    print("=" * 60)
    
    # Initialize file manager and scan for media
    if FILE_MANAGER_AVAILABLE:
        media_manager.scan_media_directory()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
