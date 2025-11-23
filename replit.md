# NexusOS Civilization Operating System

## Overview
NexusOS is a civilization architecture founded on physics, replacing traditional binary computation with electromagnetic wave states and basing economics on quantum energy (E=hf). It aims to guarantee basic living standards through a Basic Human Living Standards (BHLS) floor system. The project's core ambition is to build a self-sustaining, physics-based civilization that ensures prosperity and stability for all citizens by moving beyond speculative economic and computational systems. A key feature is the Economic Loop System, a 5-milestone economic architecture where messaging burns create real economic value through orbital transitions, DEX liquidity allocation, supply chain monetization, community ownership, and crisis protection.

## User Preferences
-   **Communication Style**: Simple, everyday language
-   **Technical Approach**: Physics-first, quantum-inspired economics
-   **Architecture**: Wavelength-based validation over traditional cryptographic hashing
-   **Licensing**: GPL v3 (GNU General Public License v3.0) to ensure community ownership and prevent corporate exploitation

## System Architecture

### UI/UX Decisions
The system provides a Unified Dashboard Launcher (`app.py`) offering access to multiple modules. The **Mobile Blockchain Hub** (`mobile_blockchain_hub.py`) serves as the central blockchain interface, integrating all core blockchain operations into a unified mobile-first application including a Web3 Wallet, Mobile DAG Messaging, Blockchain Explorer, DEX, Validator Economics, Wavelength Economics, Network modules, Civic Governance, and Mobile Connectivity. Additional modules include a Civilization Dashboard, WNSP Protocol v2.0, WNSP Protocol v3.0 (Architecture), WNSP Unified Mesh Stack, Payment Layer, AI Management Control, Talk to Nexus AI, and the WaveLang ecosystem.

### Technical Implementations & Feature Specifications
Key technical components and features include:
-   **Genesis Block**: The world's first physics-based blockchain message deployed, utilizing ultraviolet spectral validation and atomic payment execution.
-   **Avogadro Economics System**: Integrates Avogadro's Number, Boltzmann Constant, and Ideal Gas Law into blockchain economics, bridging quantum mechanics to civilization-scale thermodynamics for physics-grounded metrics.
-   **Economic Loop System**: Orchestrates the NexusOS economic flow from Messaging to Reserve, DEX, Supply Chain, Community, and the F_floor. This includes atomic transfer safety for production-grade transactions and a DAG-based idempotency system for retry safety and preventing double-execution.
-   **Mobile Blockchain Hub**: A unified mobile-first interface integrating all core blockchain modules, designed around the principle that "your phone IS the blockchain node."
-   **Civic Governance Campaign System**: Enables validators to promote innovation campaigns, facilitates community voting, and uses AI for analysis reports.
-   **Economic Simulation Engine**: Features a self-regulating issuance/burn mechanism, PID control, and conservation constraints.
-   **WNSP v2.0 Protocol (Optical Mesh Networking)**: Enables quantum cryptography-enabled optical communication with DAG messaging and 170+ scientific character encoding using unique wavelengths.
-   **WNSP v3.0 Protocol (Architecture Phase)**: Next-generation WNSP roadmap focused on hardware abstraction to enable deployment on current devices (BLE/WiFi/LoRa) without optical transceivers. Key architectural components include: (1) Hardware Abstraction Layer mapping wavelength physics to radio frequencies, (2) Adaptive Encoding System with dual-mode (Scientific/Binary) for 10x throughput, (3) Progressive Validation Tiers (Full/Intermittent/Light/Relay) for diverse device capabilities, (4) Quantum Economics Preservation across radio transmission. **Status**: Conceptual/architectural layer requiring radio stack integration, energy model revision, and measurable benchmarks for production readiness (per architect review, November 2025).
-   **WNSP Unified Mesh Stack**: A complete 4-layer decentralized knowledge infrastructure integrating Community Mesh ISP (Layer 1), Censorship-Resistant Routing (Layer 2), Privacy-First Messaging (Layer 3), and Offline Knowledge Networks (Layer 4). Demonstrates how WNSP enables internet-independent communication and education distribution. Features include wavelength-based addressing to evade DNS/URL blocking, quantum-encrypted peer-to-peer messaging with E=hf spam prevention, distributed Wikipedia caching on mesh nodes, and self-healing topology. Designed for grassroots deployment scenarios (university campuses, refugee populations, rural communities) where centralized internet infrastructure is limited or compromised.
-   **WNSP Media Propagation Engine (Conceptual Demonstration)**: Demonstrates the concept of content distribution beyond text messaging. Shows how WNSP could theoretically propagate media types (MP3/MP4/PDF/images/software) across mesh using 64KB chunking, DAG distribution, progressive streaming, content deduplication, and E=hf energy pricing. Includes community-specific content library examples for universities (lectures, textbooks), refugee populations (legal guides, language lessons), rural communities (agricultural tutorials, medical guides), and crisis response (evacuation instructions, rescue maps). Vision: Transform WNSP into offline alternative to YouTube, Spotify, Google Drive, and WhatsApp. Status: Conceptual demonstration; production would require mesh topology integration, content-based hashing, real propagation tracking, and multi-hop energy accounting.
-   **Wavelength-Economic Validation System**: A physics-based blockchain validation system utilizing Maxwell equation solvers, wave superposition, and 5D wave signature validation for quantum resistance.
-   **Mobile DAG Messaging System**: Optimized with wavelength validation, E=hf cost estimation, interactive DAG visualization, and an AI Message Security Controller.
-   **Proof of Spectrum (PoS) Consensus**: A wavelength-inspired consensus mechanism using spectral regions and wave interference for validation.
-   **Nexus Consensus Engine**: Integrates GhostDAG, Proof of Spectrum, and an AI-optimized economic layer.
-   **DEX (Decentralized Exchange)**: A Layer 2 Automated Market Maker with liquidity pools and fees contributing to the validator pool.
-   **Native Payment Layer - NexusToken (NXT)**: Features Bitcoin-style tokenomics, fixed supply, deflationary mechanics via messaging burns, and AI-controlled validator rewards.
-   **Orbital Transition Engine**: Replaces token burns with quantum physics-inspired orbital transitions.
-   **Hierarchical Pool Ecosystem**: An architecture of Reserve Pools, F_floor, and 10 Service Pools.
-   **Mobile Wallet with Global Debt Backing**: Displays NXT balance, debt backing, total backed value, and daily floor support.
-   **AI Management Control Dashboard**: A centralized governance interface for all AI systems with F_floor protection.
-   **Talk to Nexus AI**: A conversational AI interface for governance and report generation.
-   **Offline Mesh Network with Hybrid AI Routing**: A peer-to-peer internet infrastructure for direct phone-to-phone communication, integrating with WNSP v2.0 DAG messaging and using a Hybrid AI Routing Controller for intelligent path selection.
-   **Comprehensive Security Framework (Production-Integrated)**: A multi-layered defense system with enforcement hooks directly integrated into transaction flows:
    -   **Rate Limiting**: Pre-operation enforcement in native_token.py (10 transfers/60s), mobile_dag_protocol.py (20 messages/60s), and dex_core.py (5 swaps/60s) with exponential backoff
    -   **Authentication Hardening**: 7-day session expiry (reduced from 30 days), automatic token rotation after 24 hours, SHA-256 token hashing
    -   **DEX Security**: Wash trading detection (>30% pair volume flags), liquidity withdrawal protection (10% daily limit), commit-reveal scheme for MEV prevention
    -   **Multi-Oracle Consensus**: 3-source validation with outlier detection and TWAP pricing
    -   **Governance Protection**: Quadratic voting, collusion detection, Sybil resistance
    -   **AI Anomaly Detection**: Real-time monitoring of economic patterns and validator behavior
    -   **Security Command Center**: Real-time monitoring dashboard with live metrics and alerts
    -   **Active Intervention Engine**: AI-powered immune system that automatically detects and neutralizes attacks in real-time:
        - **Oracle Manipulation**: Auto-blacklist sources with >50% price deviation from consensus
        - **Governance Attacks**: Auto-pause voting on >40% vote concentration in 60 seconds
        - **Network DDoS**: Auto-ban IPs flooding >100 req/s (permanent), >50 req/s (1hr temporary)
        - **Wash Trading**: Auto-ban addresses executing >50% of pair volume
        - **Flash Loans**: Auto-ban same-block borrow/repay patterns
        - **Validator Attacks**: Auto-isolate validators exhibiting double-signing or censorship
        - **Emergency Controls**: Kill-switch for governance pause/resume and system shutdown
        - **Real-time Monitoring**: Active Interventions Dashboard with blacklists, bans, and intervention statistics

### WaveLang Ecosystem
A complete quantum-level programming stack:
-   **WaveLang Studio**: A visual code builder with drag-and-drop functionality and real-time energy calculation.
-   **WaveLang AI Teacher**: Converts natural language to WaveLang code, optimizes, compiles, explains, and provides visual execution.
-   **WaveLang Binary Compiler**: Compiles WaveLang through bytecode and assembly to machine code.
-   **Quantum Analyzer**: Applies WaveProperties for six quantum analysis modes to provide optimization recommendations.

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
-   **Oracle Integration Framework**: For external REST APIs/WebSockets.