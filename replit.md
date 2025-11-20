# NexusOS Civilization Operating System

## Overview
NexusOS is a civilization architecture based on physics, replacing binary computation with electromagnetic wave states and anchoring economics to quantum energy (E=hf). It guarantees basic living standards through the BHLS floor system. The project's vision is to build a self-sustaining, physics-based civilization, moving beyond speculative systems to ensure prosperity and stability for all citizens.

## User Preferences
- **Communication Style**: Simple, everyday language
- **Technical Approach**: Physics-first, quantum-inspired economics
- **Architecture**: Wavelength-based validation over traditional cryptographic hashing

## System Architecture

### UI/UX Decisions
The system features a Unified Dashboard Launcher (`app.py`) providing access to 17 comprehensive modules: Civilization Dashboard (with Wave Computation, BHLS Floor, Circular Economy, Civilization Simulator, Governance, Supply Chain, and Mobile Wallet), Web3 Wallet, WNSP Protocol v2.0, Mobile DAG Messaging, Blockchain Explorer, DEX (Decentralized Exchange), GhostDAG System, Payment Layer, Proof of Spectrum, Validator Economics, Wavelength Economics, Nexus Consensus, Mobile Connectivity, Long-term Supply, AI Management Control, Talk to Nexus AI, and **Offline Mesh Network**. The Mobile Wallet tab integrates global debt backing metrics with messaging/transaction functionality.

### Technical Implementations & Feature Specifications
Core technical implementations include:
-   **Economic Simulation Engine**: Comprehensive simulator with self-regulating issuance/burn, PID control, and conservation constraints.
-   **WNSP v2.0 Protocol (Optical Mesh Networking)**: Quantum cryptography-enabled optical communication with DAG messaging, 64-character encoding, and NXT payment integration (E=hf pricing).
-   **Wavelength-Economic Validation System**: Physics-based blockchain validation replacing SHA-256, utilizing Maxwell equation solvers, wave superposition, and 5D wave signature validation with Spectral Diversity Consensus for quantum resistance.
-   **Mobile DAG Messaging System**: Optimized platform with wavelength validation, E=hf cost estimation, interactive DAG visualization, and NXT payment integration.
-   **Proof of Spectrum (PoS) Consensus**: Wavelength-inspired consensus using spectral regions and wave interference for validation.
-   **GhostDAG Ecosystem Optimization**: Parallel block processing for increased throughput.
-   **Nexus Consensus Engine**: Unifies GhostDAG, Proof of Spectrum, and an AI-optimized economic layer.
-   **DEX (Decentralized Exchange)**: Layer 2 Automated Market Maker using NXT, with liquidity pools and fees directed to the validator pool. Includes a "Pool Ecosystem" tab visualizing the hierarchical pool structure (Reserve Pools → F_floor → Service Pools).
-   **Native Payment Layer - NexusToken (NXT)**: Bitcoin-style tokenomics with a fixed supply, deflationary mechanics via messaging burns, and AI-controlled validator rewards.
-   **Orbital Transition Engine**: Replaces token burns with quantum physics-inspired orbital transitions using the Rydberg formula, feeding energy to a TRANSITION_RESERVE pool.
-   **Mobile DAG Messaging Protocol**: A complete connectivity loop involving AI-controlled message routing (spectral region selection, E=hf pricing), secure wallet connection, E=hf cost calculation, production-grade personal data encryption (ECDH, AES-256-GCM), and mobile-first DAG processing. An **AI Message Security Controller** intelligently moderates message security by selecting optimal wavelengths and encryption levels.
-   **Hierarchical Pool Ecosystem**: Architecture comprising Reserve Pools, F_floor, and 10 distinct Service Pools, all supported by the F_floor and integrated with the DEX.
-   **Mobile Wallet with Global Debt Backing**: Displays NXT balance, debt backing per token, total backed value, and daily floor support, demonstrating the economic backing of NXT by global debt.
-   **AI Management Control Dashboard**: Centralized governance dashboard for all AI systems, monitoring status, governance controls, decision history, component integration, learning analytics, and real-time AI activity, with critical F_floor protection.
-   **Talk to Nexus AI**: Conversational governance interface with comprehensive codebase knowledge and report generation capabilities for researchers, investors, members, and general audiences.
-   **Offline Mesh Network with Hybrid AI Routing** (`offline_mesh_transport.py`, `offline_mesh_dashboard.py`, `hybrid_routing_controller.py`): **PEER-TO-PEER INTERNET INFRASTRUCTURE WITHOUT WiFi/CELLULAR DATA**. Revolutionary transport layer enabling direct phone-to-phone communication using Bluetooth LE (~100m range), WiFi Direct (~200m range), and NFC (<10cm, secure pairing). Integrates seamlessly with existing WNSP v2.0 DAG messaging - instead of transmitting WNSP messages over HTTP/internet, they're sent via Bluetooth/WiFi Direct. **Hybrid AI Routing Controller** (`hybrid_routing_controller.py`) extends existing AI routing from `messaging_routing.py` WITHOUT breaking changes - intelligently selects between online (internet/HTTP) and offline (Bluetooth/WiFi mesh) paths based on: (1) Network availability, (2) Message priority (CRITICAL messages use both paths for redundancy), (3) Peer proximity (nearby recipients prefer offline), (4) Cost optimization (E=hf quantum pricing, offline typically 30% cheaper), (5) Security requirements (censorship resistance). Multi-hop routing algorithm intelligently forwards messages through the mesh using signal strength and spectral diversity. Complete dashboard with 6 tabs: (1) Nearby Peers - real-time discovery, signal strength, distance metrics, (2) Network Topology - interactive Plotly graph, (3) Offline Messaging - send WNSP messages through mesh, **(4) Hybrid AI Routing - intelligent path selection dashboard showing online vs offline routing stats**, (5) Mesh Statistics - comprehensive metrics, (6) Transport Settings - protocol toggles. Architecture ready for native mobile implementation (iOS: CoreBluetooth, Android: BluetoothLeScanner). **ENABLES CRITICAL USE CASES**: Communication during disasters (no cell towers), banking/messaging in remote areas (zero infrastructure), censorship-resistant networking (cannot be blocked), emergency coordination, offline NXT transactions. Transforms NexusOS into a true decentralized internet replacement that works WITHOUT traditional infrastructure.

### Technology Stack
-   **Frontend**: Streamlit, Plotly
-   **Backend**: Python 3.11, NumPy, Pandas, SciPy, NetworkX, Numba
-   **Database**: PostgreSQL, SQLAlchemy
-   **Optimization**: scikit-optimize, bcrypt, passlib

## External Dependencies
-   **PostgreSQL**: Primary database.
-   **SQLAlchemy**: Python ORM.
-   **Plotly**: Interactive data visualizations.
-   **Streamlit**: Web application framework.
-   **Numba**: JIT compilation.
-   **scikit-optimize**: Bayesian optimization.
-   **bcrypt**: Password hashing.
-   **passlib**: Password hashing utility.
-   **Replit**: Cloud hosting platform.
-   **External REST APIs/WebSockets**: Integrated via Oracle Integration Framework.