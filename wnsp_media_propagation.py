# WNSP Unified Mesh Stack - Wavelength-Native Signaling Protocol
# Copyright (C) 2025 WNSP Project Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
WNSP Media Propagation Engine - Demonstration Module
Shows the concept of how WNSP could distribute media files (MP3, MP4, PDF, images) across mesh networks

NOTE: This is a conceptual demonstration. Production implementation would require:
1. Real mesh topology integration (not simulated hop counts)
2. Content-based hashing for true deduplication across different files
3. Actual chunk propagation tracking (not percentage-based buffering)
4. Per-hop energy accounting with realistic multi-hop cost calculation
"""

import hashlib
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import math

@dataclass
class MediaChunk:
    """Represents a chunk of a media file for DAG propagation"""
    chunk_id: str
    file_id: str
    chunk_index: int
    total_chunks: int
    data_size: int  # bytes
    content_hash: str
    wavelength: float  # nm (for energy calculation)
    energy_cost: float  # NXT
    hop_count: int = 0
    propagation_path: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

@dataclass
class MediaFile:
    """Represents a complete media file in the mesh network"""
    file_id: str
    filename: str
    file_type: str  # mp3, mp4, pdf, jpg, png, etc.
    file_size: int  # bytes
    content_hash: str
    description: str
    category: str  # university, refugee, rural, crisis
    chunks: List[MediaChunk] = field(default_factory=list)
    total_chunks: int = 0
    total_energy_cost: float = 0.0
    upload_timestamp: float = field(default_factory=time.time)
    downloaded_chunks: int = 0
    
    @property
    def download_progress(self) -> float:
        """Calculate download progress percentage"""
        if self.total_chunks == 0:
            return 0.0
        return (self.downloaded_chunks / self.total_chunks) * 100

class WNSPMediaPropagation:
    """
    WNSP Media Propagation Engine
    Handles chunking, distribution, and reassembly of media files across mesh network
    """
    
    # Physics constants
    PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
    SPEED_OF_LIGHT = 299792458  # m/s
    
    # Network configuration
    CHUNK_SIZE = 65536  # 64 KB per chunk (optimal for BLE/WiFi)
    MIN_WAVELENGTH = 350  # nm (UV limit)
    MAX_WAVELENGTH = 1033  # nm (IR limit)
    
    # Energy pricing (NXT per joule)
    # Calibrated so 100 MB ≈ 1 NXT across 5 hops
    ENERGY_MULTIPLIER = 6.7e9  # Scale quantum energy to reasonable NXT values
    
    def __init__(self):
        self.media_library: Dict[str, MediaFile] = {}
        self.chunk_cache: Dict[str, MediaChunk] = {}
        self.persistent_chunk_store: Dict[str, MediaChunk] = {}  # Persistent cache keyed by SHA-256
        self.propagation_stats = {
            'total_files': 0,
            'total_chunks_distributed': 0,
            'total_bytes_transmitted': 0,
            'total_energy_spent': 0.0,
            'avg_hop_count': 0.0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        
        # Initialize sample content library
        self._initialize_content_library()
    
    def _initialize_content_library(self):
        """Create sample media files for different community types"""
        sample_files = [
            # University Campus
            {
                'filename': 'Quantum_Mechanics_Lecture_01.mp4',
                'file_type': 'mp4',
                'file_size': 524288000,  # 500 MB
                'description': 'Physics lecture on wave-particle duality',
                'category': 'university'
            },
            {
                'filename': 'Calculus_Textbook_Chapter3.pdf',
                'file_type': 'pdf',
                'file_size': 15728640,  # 15 MB
                'description': 'Differential equations and applications',
                'category': 'university'
            },
            {
                'filename': 'Chemistry_Lab_Safety.mp4',
                'file_type': 'mp4',
                'file_size': 104857600,  # 100 MB
                'description': 'Laboratory safety procedures',
                'category': 'university'
            },
            
            # Refugee Populations
            {
                'filename': 'Asylum_Rights_Guide.pdf',
                'file_type': 'pdf',
                'file_size': 5242880,  # 5 MB
                'description': 'Legal rights and asylum procedures',
                'category': 'refugee'
            },
            {
                'filename': 'English_Basics_Audio.mp3',
                'file_type': 'mp3',
                'file_size': 10485760,  # 10 MB
                'description': 'Basic English language lessons',
                'category': 'refugee'
            },
            {
                'filename': 'Safe_Routes_Map.png',
                'file_type': 'png',
                'file_size': 2097152,  # 2 MB
                'description': 'Updated safe passage routes',
                'category': 'refugee'
            },
            
            # Rural Communities
            {
                'filename': 'Crop_Management_Tutorial.mp4',
                'file_type': 'mp4',
                'file_size': 209715200,  # 200 MB
                'description': 'Sustainable farming techniques',
                'category': 'rural'
            },
            {
                'filename': 'Medical_First_Aid.pdf',
                'file_type': 'pdf',
                'file_size': 8388608,  # 8 MB
                'description': 'Emergency medical procedures',
                'category': 'rural'
            },
            {
                'filename': 'Market_Prices_Weekly.mp3',
                'file_type': 'mp3',
                'file_size': 3145728,  # 3 MB
                'description': 'Weekly commodity price updates',
                'category': 'rural'
            },
            
            # Crisis Response
            {
                'filename': 'Evacuation_Instructions.mp4',
                'file_type': 'mp4',
                'file_size': 52428800,  # 50 MB
                'description': 'Hurricane evacuation procedures',
                'category': 'crisis'
            },
            {
                'filename': 'Emergency_Contacts.pdf',
                'file_type': 'pdf',
                'file_size': 1048576,  # 1 MB
                'description': 'Critical contact information',
                'category': 'crisis'
            },
            {
                'filename': 'Rescue_Coordination_Map.jpg',
                'file_type': 'jpg',
                'file_size': 4194304,  # 4 MB
                'description': 'Real-time rescue operation map',
                'category': 'crisis'
            }
        ]
        
        for file_data in sample_files:
            file_id = self._generate_file_id(file_data['filename'])
            content_hash = hashlib.sha256(file_data['filename'].encode()).hexdigest()[:16]
            
            media_file = MediaFile(
                file_id=file_id,
                filename=file_data['filename'],
                file_type=file_data['file_type'],
                file_size=file_data['file_size'],
                content_hash=content_hash,
                description=file_data['description'],
                category=file_data['category']
            )
            
            # Create chunks for this file
            media_file.total_chunks = math.ceil(file_data['file_size'] / self.CHUNK_SIZE)
            media_file.chunks, media_file.total_energy_cost = self._create_chunks(media_file)
            
            self.media_library[file_id] = media_file
            self.propagation_stats['total_files'] += 1
    
    def _generate_file_id(self, filename: str) -> str:
        """Generate unique file ID from filename"""
        return hashlib.sha256(filename.encode()).hexdigest()[:12]
    
    def _create_chunks(self, media_file: MediaFile) -> Tuple[List[MediaChunk], float]:
        """Split media file into chunks for DAG propagation"""
        chunks = []
        total_energy = 0.0
        
        for i in range(media_file.total_chunks):
            # Calculate chunk size (last chunk may be smaller)
            if i == media_file.total_chunks - 1:
                chunk_size = media_file.file_size - (i * self.CHUNK_SIZE)
            else:
                chunk_size = self.CHUNK_SIZE
            
            # Assign wavelength based on chunk index (distribute across spectrum)
            wavelength = self._assign_wavelength(i, media_file.total_chunks)
            
            # Calculate energy cost using E = hf, where f = c/λ
            energy_cost = self._calculate_energy_cost(chunk_size, wavelength)
            
            chunk_id = f"{media_file.file_id}_chunk_{i}"
            content_hash = hashlib.sha256(chunk_id.encode()).hexdigest()[:16]
            
            chunk = MediaChunk(
                chunk_id=chunk_id,
                file_id=media_file.file_id,
                chunk_index=i,
                total_chunks=media_file.total_chunks,
                data_size=chunk_size,
                content_hash=content_hash,
                wavelength=wavelength,
                energy_cost=energy_cost
            )
            
            chunks.append(chunk)
            total_energy += energy_cost
            self.chunk_cache[chunk_id] = chunk
            
            # Store in persistent cache for deduplication
            self.persistent_chunk_store[content_hash] = chunk
        
        return chunks, total_energy
    
    def _assign_wavelength(self, chunk_index: int, total_chunks: int) -> float:
        """Assign wavelength to chunk (distribute across visible spectrum)"""
        if total_chunks == 1:
            return (self.MIN_WAVELENGTH + self.MAX_WAVELENGTH) / 2
        
        # Linear distribution across spectrum
        wavelength_range = self.MAX_WAVELENGTH - self.MIN_WAVELENGTH
        wavelength = self.MIN_WAVELENGTH + (chunk_index / (total_chunks - 1)) * wavelength_range
        
        return round(wavelength, 2)
    
    def _calculate_energy_cost(self, data_size: int, wavelength: float) -> float:
        """Calculate E=hf energy cost in NXT"""
        # Convert wavelength to meters
        wavelength_m = wavelength * 1e-9
        
        # Calculate frequency: f = c/λ
        frequency = self.SPEED_OF_LIGHT / wavelength_m
        
        # Calculate photon energy: E = hf
        photon_energy = self.PLANCK_CONSTANT * frequency
        
        # Scale by data size and multiplier to get reasonable NXT cost
        energy_cost = photon_energy * data_size * self.ENERGY_MULTIPLIER
        
        return round(energy_cost, 6)
    
    def propagate_chunk(self, chunk_id: str, node_id: str, use_cache: bool = True) -> bool:
        """Propagate chunk through mesh network with real deduplication"""
        if chunk_id not in self.chunk_cache:
            return False
        
        chunk = self.chunk_cache[chunk_id]
        
        # Check if chunk already cached (deduplication)
        if use_cache and chunk.content_hash in self.persistent_chunk_store:
            cached_chunk = self.persistent_chunk_store[chunk.content_hash]
            if node_id in cached_chunk.propagation_path:
                # Cache hit - no need to retransmit
                self.propagation_stats['cache_hits'] += 1
                return True
        
        # Cache miss - propagate chunk
        self.propagation_stats['cache_misses'] += 1
        chunk.hop_count += 1
        chunk.propagation_path.append(node_id)
        
        # Update stats
        self.propagation_stats['total_chunks_distributed'] += 1
        self.propagation_stats['total_bytes_transmitted'] += chunk.data_size
        self.propagation_stats['total_energy_spent'] += chunk.energy_cost
        
        # Update persistent store
        self.persistent_chunk_store[chunk.content_hash] = chunk
        
        return True
    
    def simulate_download(self, file_id: str, progress: float = 0.0) -> Optional[Dict]:
        """Simulate progressive download of media file with buffering logic"""
        if file_id not in self.media_library:
            return None
        
        media_file = self.media_library[file_id]
        
        # Simulate download progress (0-100%)
        chunks_downloaded = int((progress / 100) * media_file.total_chunks)
        media_file.downloaded_chunks = chunks_downloaded
        
        # Progressive streaming thresholds
        STREAMING_THRESHOLD = 10  # Need 10% buffered to start playback
        SAFE_BUFFER = 20  # 20% recommended for smooth playback
        
        can_stream = progress >= STREAMING_THRESHOLD
        has_safe_buffer = progress >= SAFE_BUFFER
        is_complete = progress >= 100
        
        return {
            'file': media_file,
            'progress': progress,
            'chunks_downloaded': chunks_downloaded,
            'total_chunks': media_file.total_chunks,
            'can_stream': can_stream,
            'has_safe_buffer': has_safe_buffer,
            'is_complete': is_complete,
            'buffered_mb': (chunks_downloaded * self.CHUNK_SIZE) / 1048576,
            'total_mb': media_file.file_size / 1048576
        }
    
    def get_files_by_category(self, category: str) -> List[MediaFile]:
        """Get all media files for a specific community category"""
        return [
            file for file in self.media_library.values()
            if file.category == category
        ]
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        """Get detailed information about a media file"""
        if file_id not in self.media_library:
            return None
        
        media_file = self.media_library[file_id]
        
        return {
            'file_id': media_file.file_id,
            'filename': media_file.filename,
            'file_type': media_file.file_type,
            'file_size': media_file.file_size,
            'file_size_mb': round(media_file.file_size / 1048576, 2),
            'description': media_file.description,
            'category': media_file.category,
            'total_chunks': media_file.total_chunks,
            'total_energy_cost': round(media_file.total_energy_cost, 4),
            'avg_chunk_size_kb': round(self.CHUNK_SIZE / 1024, 2),
            'download_progress': media_file.download_progress,
            'estimated_time': self._estimate_download_time(media_file),
            'chunks': [
                {
                    'index': chunk.chunk_index,
                    'size_kb': round(chunk.data_size / 1024, 2),
                    'wavelength': chunk.wavelength,
                    'energy_cost': chunk.energy_cost,
                    'hop_count': chunk.hop_count
                }
                for chunk in media_file.chunks[:10]  # Show first 10 chunks
            ]
        }
    
    def _estimate_download_time(self, media_file: MediaFile) -> Dict[str, float]:
        """Estimate download time based on network type"""
        file_size_mb = media_file.file_size / 1048576
        
        # Network speeds (Mbps)
        ble_speed = 1  # 1 Mbps
        wifi_speed = 50  # 50 Mbps
        lora_speed = 0.05  # 50 Kbps
        
        return {
            'ble_minutes': round((file_size_mb * 8) / ble_speed / 60, 2),
            'wifi_minutes': round((file_size_mb * 8) / wifi_speed / 60, 2),
            'lora_minutes': round((file_size_mb * 8) / lora_speed / 60, 2)
        }
    
    def get_propagation_statistics(self) -> Dict:
        """Get overall mesh network propagation statistics"""
        if self.propagation_stats['total_chunks_distributed'] > 0:
            avg_hops = sum(
                chunk.hop_count for chunk in self.chunk_cache.values()
            ) / len(self.chunk_cache)
        else:
            avg_hops = 0.0
        
        return {
            'total_files': self.propagation_stats['total_files'],
            'total_chunks': len(self.chunk_cache),
            'total_chunks_distributed': self.propagation_stats['total_chunks_distributed'],
            'total_bytes_transmitted': self.propagation_stats['total_bytes_transmitted'],
            'total_mb_transmitted': round(self.propagation_stats['total_bytes_transmitted'] / 1048576, 2),
            'total_energy_spent_nxt': round(self.propagation_stats['total_energy_spent'], 4),
            'avg_hop_count': round(avg_hops, 2),
            'deduplication_savings': self._calculate_deduplication_savings(),
            'cache_hits': self.propagation_stats['cache_hits'],
            'cache_misses': self.propagation_stats['cache_misses']
        }
    
    def _calculate_deduplication_savings(self) -> str:
        """Calculate bandwidth saved through content deduplication"""
        total_requests = self.propagation_stats['cache_hits'] + self.propagation_stats['cache_misses']
        
        if total_requests > 0:
            savings_percent = (self.propagation_stats['cache_hits'] / total_requests) * 100
            return f"{savings_percent:.1f}%"
        
        return "0% (no data yet)"
    
    def get_content_library_summary(self) -> Dict[str, int]:
        """Get summary of content library by category"""
        summary = {
            'university': 0,
            'refugee': 0,
            'rural': 0,
            'crisis': 0
        }
        
        for media_file in self.media_library.values():
            if media_file.category in summary:
                summary[media_file.category] += 1
        
        return summary
