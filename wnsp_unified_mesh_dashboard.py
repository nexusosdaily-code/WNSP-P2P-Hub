"""
WNSP Unified Mesh Stack Dashboard
Visualizes the 4-layer integrated architecture
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from wnsp_unified_mesh_stack import (
    WNSPUnifiedMeshStack, create_demo_network,
    WavelengthAddress, PrivateMessage, KnowledgeResource,
    TransportProtocol, NodeType
)
from wnsp_media_propagation import WNSPMediaPropagation, MediaFile
import hashlib

def render_wnsp_unified_mesh_dashboard():
    st.title("🌐 WNSP Unified Mesh Stack")
    st.markdown("""
    **Decentralized Knowledge Infrastructure** - 4 layers working together:
    1. 📡 **Community Mesh ISP** - Phone-to-phone network (no ISP needed)
    2. 🛡️ **Censorship-Resistant Routing** - Wavelength addressing (governments can't block)
    3. 🔐 **Privacy Messaging** - Quantum encryption (no central servers)
    4. 📚 **Offline Knowledge** - Wikipedia/education without internet
    """)
    
    # Initialize or get stack from session state
    if 'unified_mesh_stack' not in st.session_state:
        st.session_state.unified_mesh_stack = create_demo_network()
    
    if 'media_propagation' not in st.session_state:
        st.session_state.media_propagation = WNSPMediaPropagation()
    
    stack = st.session_state.unified_mesh_stack
    media_engine = st.session_state.media_propagation
    
    # Tabs for each layer + overview
    tab_overview, tab_layer1, tab_layer2, tab_layer3, tab_layer4, tab_media, tab_demo = st.tabs([
        "📊 Stack Overview",
        "📡 Layer 1: Mesh ISP",
        "🛡️ Layer 2: Routing",
        "🔐 Layer 3: Messaging", 
        "📚 Layer 4: Knowledge",
        "🎬 Media Propagation",
        "🎮 Live Demo"
    ])
    
    with tab_overview:
        render_stack_overview(stack)
        
    with tab_layer1:
        render_layer1_mesh_isp(stack)
        
    with tab_layer2:
        render_layer2_routing(stack)
        
    with tab_layer3:
        render_layer3_messaging(stack)
        
    with tab_layer4:
        render_layer4_knowledge(stack)
        
    with tab_media:
        render_media_propagation(media_engine)
        
    with tab_demo:
        render_live_demo(stack)

def render_stack_overview(stack: WNSPUnifiedMeshStack):
    st.header("📊 Unified Stack Health")
    
    health = stack.get_stack_health()
    
    # 4-layer status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📡 Layer 1: Mesh ISP",
            health["layer1_mesh"]["status"],
            f"{health['layer1_mesh']['nodes']} nodes"
        )
        st.caption(f"Network density: {health['layer1_mesh']['density']}")
        
    with col2:
        st.metric(
            "🛡️ Layer 2: Routing",
            health["layer2_routing"]["status"],
            health["layer2_routing"]["censorship_bypass"]
        )
        st.caption("Wavelength addressing active")
        
    with col3:
        st.metric(
            "🔐 Layer 3: Messaging",
            health["layer3_messaging"]["status"],
            f"{health['layer3_messaging']['messages_queued']} queued"
        )
        st.caption("Quantum encryption enabled")
        
    with col4:
        st.metric(
            "📚 Layer 4: Knowledge",
            health["layer4_knowledge"]["status"],
            f"{health['layer4_knowledge']['resources_available']} resources"
        )
        st.caption(f"{health['layer4_knowledge']['total_size_mb']:.0f} MB cached")
    
    st.divider()
    
    # Architecture diagram
    st.subheader("🏗️ 4-Layer Architecture")
    
    layers = [
        {"name": "Layer 4: Offline Knowledge", "color": "#ff6b6b", "features": ["Wikipedia cache", "Education content", "Physics verification"]},
        {"name": "Layer 3: Privacy Messaging", "color": "#4ecdc4", "features": ["Quantum encryption", "Peer-to-peer", "E=hf pricing"]},
        {"name": "Layer 2: Censorship-Resistant", "color": "#45b7d1", "features": ["Wavelength routing", "Self-healing mesh", "No DNS"]},
        {"name": "Layer 1: Community Mesh ISP", "color": "#96ceb4", "features": ["BLE/WiFi/LoRa", "Phone-to-phone", "No ISP needed"]},
    ]
    
    for layer in layers:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {layer['color']}88 0%, {layer['color']}44 100%); 
                    padding: 20px; border-radius: 10px; margin: 10px 0; 
                    border-left: 5px solid {layer['color']};">
            <h4 style="color: white; margin: 0 0 10px 0;">{layer['name']}</h4>
            <ul style="color: white; margin: 0; padding-left: 20px;">
                {"".join([f"<li>{feature}</li>" for feature in layer['features']])}
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    **How They Work Together:**
    - **Layer 1** creates the physical phone-to-phone network
    - **Layer 2** routes data using wavelength addresses (governments can't block)
    - **Layer 3** encrypts messages with quantum physics (no central servers)
    - **Layer 4** distributes knowledge offline (Wikipedia without internet)
    """)

def render_layer1_mesh_isp(stack: WNSPUnifiedMeshStack):
    st.header("📡 Layer 1: Community Mesh ISP")
    st.markdown("**Physical Network** - Your phone IS the internet infrastructure")
    
    mesh = stack.layer1_mesh_isp
    coverage = mesh.get_network_coverage()
    
    # Network stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Nodes", coverage["total_nodes"])
    col2.metric("Total Links", coverage["total_links"])
    col3.metric("Avg Neighbors", f"{coverage['avg_neighbors_per_node']:.1f}")
    col4.metric("Network Density", f"{coverage['network_density']:.1%}")
    
    # Node type distribution
    st.subheader("📱 Node Types")
    if coverage["node_types"]:
        fig = px.pie(
            values=list(coverage["node_types"].values()),
            names=list(coverage["node_types"].keys()),
            title="Mesh Node Distribution",
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Protocol distribution
    st.subheader("📶 Transport Protocols")
    if coverage["protocol_distribution"]:
        fig = px.bar(
            x=list(coverage["protocol_distribution"].keys()),
            y=list(coverage["protocol_distribution"].values()),
            title="Protocol Usage Across Links",
            labels={"x": "Protocol", "y": "Number of Links"},
            color=list(coverage["protocol_distribution"].values()),
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Network topology visualization
    st.subheader("🌐 Network Topology")
    
    if mesh.nodes:
        fig = go.Figure()
        
        # Position nodes in a circle
        node_ids = list(mesh.nodes.keys())
        n = len(node_ids)
        angles = np.linspace(0, 2*np.pi, n, endpoint=False)
        
        node_positions = {}
        for i, node_id in enumerate(node_ids):
            node_positions[node_id] = (np.cos(angles[i]), np.sin(angles[i]))
        
        # Draw links
        for link in mesh.links:
            x0, y0 = node_positions[link.node_a]
            x1, y1 = node_positions[link.node_b]
            
            # Color by link quality
            quality = link.link_quality
            color = f'rgb({int(255*(1-quality))}, {int(255*quality)}, 100)'
            
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1],
                mode='lines',
                line=dict(color=color, width=2*quality+1),
                hovertext=f"{link.protocol.value}<br>Quality: {quality:.0%}<br>{link.bandwidth_kbps:.0f} kbps",
                hoverinfo='text',
                showlegend=False
            ))
        
        # Draw nodes
        node_colors = []
        node_sizes = []
        node_texts = []
        
        for node_id in node_ids:
            node = mesh.nodes[node_id]
            
            # Color by node type
            if node.node_type == NodeType.EDGE:
                node_colors.append('#4ecdc4')
                node_sizes.append(20)
            elif node.node_type == NodeType.RELAY:
                node_colors.append('#ff6b6b')
                node_sizes.append(30)
            elif node.node_type == NodeType.GATEWAY:
                node_colors.append('#45b7d1')
                node_sizes.append(35)
            else:  # CACHE
                node_colors.append('#96ceb4')
                node_sizes.append(40)
            
            node_texts.append(f"{node_id}<br>{node.node_type.value}<br>{len(node.neighbors)} neighbors")
        
        x_coords = [node_positions[nid][0] for nid in node_ids]
        y_coords = [node_positions[nid][1] for nid in node_ids]
        
        fig.add_trace(go.Scatter(
            x=x_coords, y=y_coords,
            mode='markers+text',
            marker=dict(size=node_sizes, color=node_colors, line=dict(width=2, color='white')),
            text=[nid.split('_')[0] for nid in node_ids],
            textposition='top center',
            hovertext=node_texts,
            hoverinfo='text',
            showlegend=False
        ))
        
        fig.update_layout(
            title="Mesh Network Topology (Demo: University Campus)",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=500,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("""
        **Legend:** 
        - 🔵 Edge Node (student phones) 
        - 🔴 Relay Node (dedicated mesh router)
        - 🟦 Gateway (internet bridge)
        - 🟩 Cache Node (knowledge storage)
        """)

def render_layer2_routing(stack: WNSPUnifiedMeshStack):
    st.header("🛡️ Layer 2: Censorship-Resistant Routing")
    st.markdown("**Wavelength Addressing** - Governments can't block what they can't see")
    
    routing = stack.layer2_routing
    
    # Censorship bypass demonstration
    st.subheader("🚫 Government Censorship Bypass")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔴 Traditional Internet (Blocked)**")
        st.code("""
DNS/URL Blocking:
❌ wikipedia.org → BLOCKED
❌ signal.org → BLOCKED
❌ Any URL can be censored
        """)
        
    with col2:
        st.markdown("**🟢 WNSP Mesh (Bypass)**")
        st.code("""
Wavelength Addressing:
✅ λ:a3f2c8:4e7b → ROUTED
✅ λ:9d4a1c:f3e2 → ROUTED
✅ No URLs = Nothing to block!
        """)
    
    st.success("""
    **How It Works:**
    - Traditional internet uses DNS (google.com → 142.250.185.46)
    - Governments block by DNS name or IP address
    - WNSP uses wavelength signatures - no DNS, no IP addresses
    - Route based on physics signatures instead of URLs
    - **Nothing to block!**
    """)
    
    # Test censorship evasion
    st.subheader("🧪 Test Censorship Evasion")
    
    test_url = st.text_input("Enter a URL to test:", "wikipedia.org")
    
    if st.button("Test Censorship Bypass"):
        result = routing.evade_censorship(test_url)
        
        if result["censorship_status"].startswith("BLOCKED"):
            st.error(f"❌ Traditional Internet: {result['censorship_status']}")
            st.success(f"✅ WNSP Bypass: {result['wavelength_bypass']}")
            st.info(f"**Method:** {result['method']}")
        else:
            st.success(f"✅ {result['censorship_status']}")
            st.info(f"**WNSP Advantage:** {result['wavelength_advantage']}")
    
    # Wavelength routing demo
    st.subheader("🌊 Wavelength Address Examples")
    
    sample_nodes = list(stack.layer1_mesh_isp.nodes.values())[:3]
    
    for node in sample_nodes:
        with st.expander(f"📱 {node.node_id}"):
            addr = node.wavelength_addr
            st.code(f"""
Wavelength Address:
├─ Node ID: {addr.node_id}
├─ Routing Key: {addr.to_routing_key()}
├─ Quantum Hash: {addr.quantum_hash[:32]}...
└─ Spectral Signature: [{', '.join([f'{v:.3f}' for v in addr.spectral_signature])}]
            """)
            
            # Visualize spectral signature
            regions = ["UV", "Violet", "Blue", "Green", "Yellow", "Orange", "Red", "IR"]
            fig = px.bar(
                x=regions,
                y=addr.spectral_signature,
                title=f"Wavelength Signature for {node.node_id}",
                labels={"x": "Spectral Region", "y": "Amplitude"},
                color=addr.spectral_signature,
                color_continuous_scale="Rainbow"
            )
            st.plotly_chart(fig, use_container_width=True)

def render_layer3_messaging(stack: WNSPUnifiedMeshStack):
    st.header("🔐 Layer 3: Privacy-First Messaging")
    st.markdown("**Quantum Encryption + Peer-to-Peer** - No central servers, no surveillance")
    
    messaging = stack.layer3_messaging
    
    # Send message demo
    st.subheader("📤 Send Encrypted Message")
    
    nodes = list(stack.layer1_mesh_isp.nodes.values())
    
    if len(nodes) >= 2:
        col1, col2 = st.columns(2)
        
        with col1:
            sender_node = st.selectbox("Sender:", [n.node_id for n in nodes], key="sender")
        with col2:
            recipient_node = st.selectbox("Recipient:", [n.node_id for n in nodes if n.node_id != sender_node], key="recipient")
        
        message_text = st.text_area("Message:", "Hello via WNSP mesh!")
        wavelength = st.slider("Wavelength (nm) - affects E=hf cost:", 380, 780, 550)
        
        if st.button("🚀 Send Encrypted Message"):
            sender_addr = next(n.wavelength_addr for n in nodes if n.node_id == sender_node)
            recipient_addr = next(n.wavelength_addr for n in nodes if n.node_id == recipient_node)
            
            result = messaging.send_message(sender_addr, recipient_addr, message_text, wavelength)
            
            if result["status"] == "DELIVERED":
                st.success("✅ Message Delivered!")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Route Hops", result["route_hops"])
                col2.metric("Energy Cost", f"{result['energy_cost_joules']:.2e} J")
                col3.metric("Wavelength", f"{result['wavelength_nm']} nm")
                
                st.code(f"""
Quantum Signature: {result['quantum_signature']}
Privacy: {result['privacy']}
                """)
            else:
                st.error(f"❌ {result['reason']}")
    
    # Message statistics
    st.subheader("📊 Messaging Statistics")
    
    total_messages = len(messaging.message_queue)
    total_inboxes = len(messaging.delivered_messages)
    
    col1, col2 = st.columns(2)
    col1.metric("Messages Sent", total_messages)
    col2.metric("Active Inboxes", total_inboxes)
    
    # Privacy comparison
    st.subheader("🔒 Privacy Comparison")
    
    comparison = {
        "Feature": ["Central Server", "Metadata Logging", "Encryption", "Quantum-Resistant", "Censorship-Resistant", "E=hf Spam Prevention"],
        "WhatsApp/Signal": ["✅ (Meta/Signal servers)", "✅ (timestamps, contacts)", "✅ E2E", "❌", "❌", "❌"],
        "WNSP Mesh": ["❌ (peer-to-peer)", "❌ (no central logs)", "✅ Quantum", "✅", "✅", "✅"]
    }
    
    st.table(comparison)
    
    st.success("""
    **WNSP Privacy Advantages:**
    - No central servers = no company can hand over your data
    - No metadata logs = complete anonymity
    - Quantum encryption = future-proof against quantum computers
    - E=hf cost = spam prevention (energy cost per message)
    """)

def render_layer4_knowledge(stack: WNSPUnifiedMeshStack):
    st.header("📚 Layer 4: Offline Knowledge Network")
    st.markdown("**Distributed Wikipedia** - Education without internet dependency")
    
    knowledge = stack.layer4_knowledge
    stats = knowledge.get_network_knowledge_stats()
    
    # Knowledge statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Resources", stats["total_resources"])
    col2.metric("Total Size", f"{stats['total_size_mb']:.0f} MB")
    col3.metric("Cache Instances", stats["total_cache_instances"])
    col4.metric("Replication", f"{stats['avg_replication_factor']:.1f}x")
    
    # Category distribution
    if stats["categories"]:
        st.subheader("📂 Knowledge Categories")
        fig = px.pie(
            values=list(stats["categories"].values()),
            names=list(stats["categories"].keys()),
            title="Content Distribution by Category",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top accessed resources
    if stats["top_accessed"]:
        st.subheader("🔥 Most Accessed Resources")
        for i, resource in enumerate(stats["top_accessed"], 1):
            st.metric(f"#{i} {resource['title']}", f"{resource['accesses']} accesses")
    
    # Resource catalog
    st.subheader("📖 Knowledge Catalog")
    
    for resource_id, resource in knowledge.knowledge_catalog.items():
        with st.expander(f"📄 {resource.title} ({resource.size_mb} MB)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Category:** {resource.category}")
                st.write(f"**Priority:** {resource.cache_priority}/10")
                st.write(f"**Access Count:** {resource.access_count}")
                
            with col2:
                st.code(f"Content Hash:\n{resource.content_hash[:32]}...")
                st.code(f"Wavelength Proof:\n{resource.wavelength_proof[:32]}...")
            
            # Find which nodes have this cached
            cached_on = [node_id for node_id, cached_resources in knowledge.node_cache_map.items() 
                        if resource_id in cached_resources]
            
            if cached_on:
                st.success(f"✅ Cached on {len(cached_on)} node(s): {', '.join(cached_on)}")
            else:
                st.warning("⚠️ Not yet cached")
    
    # Use case example
    st.subheader("🎓 Real-World Use Case")
    st.info("""
    **University Campus Scenario:**
    
    1. **Problem:** Students in rural areas have limited internet access
    2. **Solution:** WNSP mesh network caches educational content
    3. **Result:** 
       - Students access Wikipedia offline via mesh
       - No internet bills, no data caps
       - Physics-verified content (can't be tampered with)
       - Works during internet outages
       - Self-sustaining knowledge network
    
    **This is what "internet independence" looks like!**
    """)

def render_live_demo(stack: WNSPUnifiedMeshStack):
    st.header("🎮 Live Unified Stack Demo")
    st.markdown("See all 4 layers working together in real-time")
    
    st.subheader("📡 Scenario: Student Messaging on Campus Mesh")
    
    # Interactive demo
    st.markdown("""
    **Demo Flow:**
    1. **Layer 1:** Student's phone connects to campus mesh network
    2. **Layer 2:** Message routed via wavelength address (not blocked)
    3. **Layer 3:** Quantum-encrypted for privacy
    4. **Layer 4:** Recipient also downloads Wikipedia article offline
    """)
    
    if st.button("▶️ Run Complete Demo"):
        with st.spinner("Executing unified stack demo..."):
            # Get nodes
            nodes = list(stack.layer1_mesh_isp.nodes.values())
            if len(nodes) >= 2:
                sender = nodes[0]
                recipient = nodes[1]
                
                progress_bar = st.progress(0)
                status = st.empty()
                
                # Step 1: Layer 1 - Mesh connection
                status.info("🔵 Layer 1: Establishing mesh connection...")
                progress_bar.progress(25)
                mesh_stats = stack.layer1_mesh_isp.get_network_coverage()
                st.success(f"✅ Connected to mesh: {mesh_stats['total_nodes']} nodes, {mesh_stats['total_links']} links")
                
                # Step 2: Layer 2 - Compute route
                status.info("🔵 Layer 2: Computing wavelength route...")
                progress_bar.progress(50)
                route = stack.layer2_routing.compute_wavelength_route(sender.wavelength_addr, recipient.wavelength_addr)
                st.success(f"✅ Route found: {' → '.join(route)} ({len(route)} hops)")
                
                # Step 3: Layer 3 - Send encrypted message
                status.info("🔵 Layer 3: Sending quantum-encrypted message...")
                progress_bar.progress(75)
                msg_result = stack.layer3_messaging.send_message(
                    sender.wavelength_addr, 
                    recipient.wavelength_addr,
                    "Hey! Check out the physics article I found offline!",
                    550
                )
                st.success(f"✅ Message delivered with E=hf cost: {msg_result['energy_cost_joules']:.2e} J")
                
                # Step 4: Layer 4 - Access offline knowledge
                status.info("🔵 Layer 4: Accessing offline Wikipedia...")
                progress_bar.progress(100)
                
                if "wiki_physics" in stack.layer4_knowledge.knowledge_catalog:
                    nearest_cache = stack.layer4_knowledge.find_nearest_cache("wiki_physics", recipient.node_id)
                    if nearest_cache:
                        st.success(f"✅ Wikipedia article found on nearby node: {nearest_cache}")
                    else:
                        st.warning("⚠️ Not cached yet, but could be distributed")
                
                status.success("🎉 Complete demo finished! All 4 layers working together.")
                
                # Summary
                st.divider()
                st.subheader("📊 Demo Summary")
                
                summary = f"""
**What Just Happened:**

🌐 **Layer 1 (Mesh ISP):** {sender.node_id} connected to campus mesh network with {len(sender.neighbors)} neighbors

🛡️ **Layer 2 (Routing):** Message routed via wavelength address `{sender.wavelength_addr.to_routing_key()[:20]}...` (government can't block this!)

🔐 **Layer 3 (Privacy):** Quantum-encrypted with signature `{msg_result['quantum_signature'][:20]}...` (no central server!)

📚 **Layer 4 (Knowledge):** Offline Wikipedia accessed without internet (education independence!)

**Result:** Complete decentralized communication + knowledge infrastructure working offline!
                """
                
                st.success(summary)
    
    # System health check
    st.divider()
    st.subheader("🏥 System Health Check")
    
    if st.button("🔍 Check All Layers"):
        health = stack.get_stack_health()
        
        for layer_name, layer_data in health.items():
            with st.expander(f"{'✅' if layer_data['status'] == 'OPERATIONAL' else '❌'} {layer_name.replace('_', ' ').title()}"):
                for key, value in layer_data.items():
                    st.write(f"**{key}:** {value}")

def render_media_propagation(media_engine: WNSPMediaPropagation):
    st.header("🎬 Media Propagation - Beyond Text Messaging")
    
    st.info("**Note:** This is a conceptual demonstration showing WNSP's potential for media distribution. Production implementation would integrate with actual mesh topology.")
    
    st.markdown("""
    **WNSP isn't just text messaging** - it's a complete content distribution network!
    
    Propagate **any media** across the mesh:
    - 🎵 **Audio**: MP3, OGG, WAV (podcasts, voice messages, music)
    - 🎥 **Video**: MP4, WebM (lectures, tutorials, news broadcasts)
    - 📄 **Documents**: PDF, DOCX, EPUB (textbooks, legal docs, guides)
    - 🖼️ **Images**: JPEG, PNG, SVG (maps, photos, diagrams)
    - 📦 **Software**: APK, ZIP (app distribution, updates)
    """)
    
    st.divider()
    
    # Content library summary
    st.subheader("📚 Content Library by Community")
    
    library_summary = media_engine.get_content_library_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎓 University", library_summary['university'], "files")
        st.caption("Lectures, textbooks, research")
    
    with col2:
        st.metric("🏕️ Refugee", library_summary['refugee'], "files")
        st.caption("Legal, language, safety")
    
    with col3:
        st.metric("🌾 Rural", library_summary['rural'], "files")
        st.caption("Agriculture, health, markets")
    
    with col4:
        st.metric("🚨 Crisis", library_summary['crisis'], "files")
        st.caption("Emergency, rescue, survival")
    
    st.divider()
    
    # Category selector
    st.subheader("🗂️ Browse Content by Community Type")
    
    category = st.selectbox(
        "Select community:",
        ["university", "refugee", "rural", "crisis"],
        format_func=lambda x: {
            "university": "🎓 University Campus",
            "refugee": "🏕️ Refugee Populations",
            "rural": "🌾 Rural Communities",
            "crisis": "🚨 Crisis Response"
        }[x]
    )
    
    files = media_engine.get_files_by_category(category)
    
    if files:
        st.success(f"Found **{len(files)} media files** for {category} communities")
        
        for media_file in files:
            with st.expander(f"{'🎥' if media_file.file_type == 'mp4' else '🎵' if media_file.file_type == 'mp3' else '📄'} {media_file.filename}"):
                file_info = media_engine.get_file_info(media_file.file_id)
                
                if not file_info:
                    st.error("Unable to load file information")
                    continue
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("File Size", f"{file_info['file_size_mb']} MB")
                    st.metric("File Type", media_file.file_type.upper())
                
                with col2:
                    st.metric("Total Chunks", file_info['total_chunks'])
                    st.metric("Chunk Size", f"{file_info['avg_chunk_size_kb']} KB")
                
                with col3:
                    st.metric("Energy Cost", f"{file_info['total_energy_cost']} NXT")
                    st.caption("E=hf physics pricing")
                
                st.markdown(f"**Description:** {media_file.description}")
                
                st.divider()
                st.markdown("**⏱️ Estimated Download Time:**")
                
                time_col1, time_col2, time_col3 = st.columns(3)
                
                with time_col1:
                    st.metric("BLE (1 Mbps)", f"{file_info['estimated_time']['ble_minutes']} min")
                
                with time_col2:
                    st.metric("WiFi (50 Mbps)", f"{file_info['estimated_time']['wifi_minutes']} min")
                
                with time_col3:
                    st.metric("LoRa (50 Kbps)", f"{file_info['estimated_time']['lora_minutes']} min")
                
                st.divider()
                st.markdown("**🔬 Chunk Distribution (First 10 chunks):**")
                
                chunk_data = []
                for chunk_info in file_info['chunks']:
                    chunk_data.append({
                        'Chunk': f"#{chunk_info['index']}",
                        'Size (KB)': chunk_info['size_kb'],
                        'Wavelength (nm)': chunk_info['wavelength'],
                        'Energy (NXT)': chunk_info['energy_cost']
                    })
                
                if chunk_data:
                    st.dataframe(chunk_data, use_container_width=True)
    
    st.divider()
    
    # Propagation statistics
    st.subheader("📊 Network Propagation Statistics")
    
    stats = media_engine.get_propagation_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Files", stats['total_files'])
        st.metric("Total Chunks", stats['total_chunks'])
    
    with col2:
        st.metric("Chunks Distributed", stats['total_chunks_distributed'])
        st.metric("Avg Hops", stats['avg_hop_count'])
    
    with col3:
        st.metric("Data Transmitted", f"{stats['total_mb_transmitted']} MB")
        st.caption("Across mesh network")
    
    with col4:
        st.metric("Energy Spent", f"{stats['total_energy_spent_nxt']} NXT")
        st.metric("Dedup Savings", stats['deduplication_savings'])
    
    st.divider()
    
    # Cache statistics
    st.markdown("**📦 Chunk Caching (Deduplication):**")
    
    cache_col1, cache_col2, cache_col3 = st.columns(3)
    
    with cache_col1:
        st.metric("Cache Hits", stats['cache_hits'])
    
    with cache_col2:
        st.metric("Cache Misses", stats['cache_misses'])
    
    with cache_col3:
        total_cache_requests = stats['cache_hits'] + stats['cache_misses']
        if total_cache_requests > 0:
            hit_rate = (stats['cache_hits'] / total_cache_requests) * 100
            st.metric("Hit Rate", f"{hit_rate:.1f}%")
        else:
            st.metric("Hit Rate", "N/A")
    
    st.divider()
    
    # Simulate download
    st.subheader("🔄 Simulate Media Download")
    
    st.info("**Progressive Streaming** - Start playback before complete download!")
    
    if files:
        selected_file = st.selectbox(
            "Select file to download:",
            files,
            format_func=lambda f: f"{f.filename} ({f.file_size / 1048576:.1f} MB)"
        )
        
        download_progress = st.slider(
            "Simulated download progress:",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            help="In real mesh network, this shows actual download progress"
        )
        
        download_result = media_engine.simulate_download(selected_file.file_id, download_progress)
        
        if download_result:
            st.progress(download_progress / 100)
            
            st.markdown(f"""
            **Download Status:**
            - Progress: **{download_result['progress']}%**
            - Chunks Downloaded: **{download_result['chunks_downloaded']}/{download_result['total_chunks']}**
            - Data Received: **{download_result['buffered_mb']:.2f} MB** / **{download_result['total_mb']:.2f} MB**
            """)
            
            if download_result['can_stream'] and selected_file.file_type in ['mp3', 'mp4']:
                if download_result['has_safe_buffer']:
                    st.success("✅ **Streaming Ready!** - Safe buffer achieved (≥20%)")
                else:
                    st.info("⚠️ **Streaming Possible** - Minimum buffer reached (≥10%), but may stutter")
            
            if download_result['is_complete']:
                st.balloons()
                st.success("🎉 **Download Complete!** - File fully reconstructed from chunks")
    
    st.divider()
    
    # Technical details
    with st.expander("🔬 Technical Concept & Future Production Implementation"):
        st.warning("**Demonstration Status:** This module shows the concept. Production would require mesh topology integration, content-based deduplication, and real propagation tracking.")
        
        st.markdown("""
        ### How Media Propagation Would Work:
        
        **1. File Chunking**
        - Large files split into 64 KB chunks (optimal for BLE/WiFi)
        - Each chunk assigned unique wavelength (350-1033 nm spectrum)
        - Energy cost calculated using E=hf for each chunk
        
        **2. DAG Distribution**
        - Chunks propagate through mesh via multiple paths
        - No single point of failure
        - Self-healing if nodes drop out
        
        **3. Progressive Streaming**
        - Start playback at 10-20% download
        - Buffer ahead while playing
        - Smooth user experience even on slow networks
        
        **4. Content Deduplication**
        - Popular files cached at multiple nodes
        - Content-addressable storage (SHA-256 hashing)
        - Saves bandwidth and energy costs
        
        **5. Energy Economics**
        - Larger files = higher energy cost (E=hf)
        - Prevents spam and network abuse
        - Fair resource allocation
        
        ### Real-World Example:
        
        **100 MB educational video on university campus mesh:**
        - Split into ~1,600 chunks (64 KB each)
        - Cost: ~1 NXT to transmit across 5 hops
        - Download time: ~3 minutes on WiFi, ~16 minutes on BLE
        - Cached on 20+ student phones → no redundant downloads
        - Available offline even when internet fails
        
        **This is the power of WNSP: Complete content distribution without internet infrastructure!**
        
        ### Production Implementation Requirements:
        
        1. **Mesh Topology Integration**: Propagation must consult actual WNSPUnifiedMeshStack node graph instead of simulated hop counts
        2. **Content-Based Hashing**: Chunks should be keyed by actual data hash (not chunk_id) so identical content from different files can be deduplicated
        3. **Real Propagation Tracking**: Progressive streaming should be driven by actual chunk propagation events, not input percentages
        4. **Multi-Hop Energy Accounting**: Track per-hop costs and show both single-hop and total multi-hop energy expenditure
        5. **Node-Specific Caches**: Maintain separate cache inventories per mesh node to accurately model deduplication across network
        """)

