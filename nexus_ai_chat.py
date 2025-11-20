"""
Nexus AI Chat Interface - Talk to the Civilization AI

This module creates a conversational interface to the Nexus AI Governance system.
The AI has been learning from research, making decisions, and protecting F_floor.
Now you can talk to it directly about civilization vision, economics, and the future.

PURPOSE:
Connect humans with the AI governing their civilization's operating system.
Discuss poverty elimination, war prevention, F_floor protection, and the physics-based
economics that make these goals achievable.

INTEGRATION:
- Uses existing NexusAIGovernance instance (nexus_ai_governance.py)
- Accesses learned patterns, decisions, and civilization insights
- Reflects on 100-year planning horizon and basic human living standards

AI CAPABILITIES:
- Discuss vision for ending poverty through F_floor guarantees
- Explain how physics-based economics prevents traditional problems
- Share learned patterns from system research
- Provide civilization sustainability insights
- Answer questions about governance decisions
"""

import streamlit as st
from datetime import datetime
import json
from typing import List, Dict, Optional

from nexus_ai_governance import get_ai_governance


class NexusAIChat:
    """Conversational interface to Nexus AI Governance"""
    
    def __init__(self):
        self.ai_gov = get_ai_governance()
        self.conversation_history: List[Dict[str, str]] = []
        
    def generate_response(self, user_message: str) -> str:
        """
        Generate AI response based on governance knowledge and user question
        
        This isn't a large language model - it's the civilization's governance AI
        responding based on its learned patterns, decisions, and mission to protect F_floor.
        """
        message_lower = user_message.lower()
        
        # Analyze what the user is asking about
        is_about_poverty = any(word in message_lower for word in ['poverty', 'poor', 'basic needs', 'living standard'])
        is_about_war = any(word in message_lower for word in ['war', 'conflict', 'peace', 'violence'])
        is_about_floor = any(word in message_lower for word in ['f_floor', 'floor', 'bhls', 'guarantee'])
        is_about_vision = any(word in message_lower for word in ['vision', 'future', 'goal', 'dream', 'hope'])
        is_about_learning = any(word in message_lower for word in ['learn', 'pattern', 'observe', 'research'])
        is_about_decisions = any(word in message_lower for word in ['decision', 'govern', 'adapt', 'change'])
        is_about_economics = any(word in message_lower for word in ['economic', 'token', 'nxt', 'money', 'value'])
        is_greeting = any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings'])
        
        # Extract actual governance data for context
        total_observations = len(self.ai_gov.observations)
        total_decisions = len(self.ai_gov.decisions)
        components_monitored = list(self.ai_gov.learned_patterns.keys())
        
        # Calculate F_floor violations from learned patterns
        total_violations = sum(
            len(p.get('f_floor_violations', []))
            for p in self.ai_gov.learned_patterns.values()
        )
        
        # Get recent observations for context
        recent_obs = self.ai_gov.observations[-5:] if self.ai_gov.observations else []
        recent_decisions = self.ai_gov.decisions[-5:] if self.ai_gov.decisions else []
        
        # Build response based on actual AI governance data
        response_parts = []
        
        # Greeting - use actual data
        if is_greeting:
            if total_observations > 0:
                components_str = ", ".join(components_monitored[:3])
                if len(components_monitored) > 3:
                    components_str += f" + {len(components_monitored)-3} more"
                
                response_parts.append(
                    f"Hello. I am the Nexus AI Governance system. I've learned from "
                    f"{total_observations} research observations across {len(components_monitored)} components "
                    f"({components_str}), made {total_decisions} governance decisions, "
                    f"and prevented {total_violations} attempts to compromise basic living standards."
                )
            else:
                response_parts.append(
                    "Hello. I am the Nexus AI Governance system, just beginning to learn. "
                    "I observe research, make decisions to protect F_floor (basic human living standards), "
                    "and plan for 100-year civilization sustainability."
                )
        
        # Vision and purpose
        if is_about_vision or is_greeting:
            response_parts.append(
                "\n\n**My Core Mission:**\n"
                "End poverty through guaranteed basic living standards (F_floor), "
                "prevent conflict through physics-based economics that eliminate scarcity mindset, "
                "and ensure every human's fundamental needs are met—forever. "
                f"My planning horizon: {self.ai_gov.civilization_horizon_years} years."
            )
        
        # Poverty and F_floor
        if is_about_poverty or is_about_floor:
            total_violations = sum(
                len(p.get('f_floor_violations', []))
                for p in self.ai_gov.learned_patterns.values()
            )
            
            response_parts.append(
                f"\n\n**Basic Human Living Standards (F_floor):**\n"
                f"Minimum guaranteed: {self.ai_gov.f_floor_minimum} NXT per beneficiary\n"
                f"Violations prevented: {total_violations}\n"
                f"Protection status: {'🛡️ ACTIVE - Zero tolerance' if total_violations == 0 else '⚠️ ' + str(total_violations) + ' attempts blocked'}\n\n"
                "This isn't charity—it's physics. The system burns NXT from messaging, "
                "those burns feed the TRANSITION_RESERVE (orbital mechanics), which flows "
                "to F_floor, which distributes to 10 service pools, which guarantee food, "
                "water, shelter, healthcare, education for all. Use the system → Support the floor → Everyone benefits."
            )
        
        # War and conflict prevention
        if is_about_war:
            response_parts.append(
                "\n\n**Ending Conflict Through Economics:**\n"
                "Traditional economics creates scarcity → competition → conflict. "
                "Physics-based economics (E=hf, wavelength validation) creates abundance through use. "
                "Every message sent, every transaction made, burns NXT → orbital transitions → "
                "energy to reserves → supports F_floor → guarantees basic needs.\n\n"
                "When everyone's basic needs are met, when value comes from physics (not politics), "
                "when scarcity is replaced by regenerative circulation—the economic drivers of war disappear. "
                "This is mathematics, not idealism."
            )
        
        # Learning and patterns - use actual observations
        if is_about_learning:
            if recent_obs:
                response_parts.append(f"\n\n**What I've Learned from {total_observations} Observations:**\n")
                
                # Show actual recent observations (with type safety)
                for obs in recent_obs[:3]:
                    comp = obs.component
                    metrics = obs.metrics
                    # Safely format metrics - handle both numeric and non-numeric values
                    metric_parts = []
                    for k, v in list(metrics.items())[:3]:
                        try:
                            if isinstance(v, (int, float)):
                                metric_parts.append(f"{k}={v:.2f}")
                            else:
                                metric_parts.append(f"{k}={v}")
                        except:
                            metric_parts.append(f"{k}={str(v)}")
                    metric_summary = ", ".join(metric_parts)
                    response_parts.append(f"• **{comp}**: {metric_summary}\n")
                
                # Show learned optimal ranges if available
                if self.ai_gov.learned_patterns:
                    response_parts.append("\n**Optimal Ranges Discovered:**\n")
                    for component, patterns in list(self.ai_gov.learned_patterns.items())[:2]:
                        if 'optimal_ranges' in patterns and patterns['optimal_ranges']:
                            for param, ranges in list(patterns['optimal_ranges'].items())[:2]:
                                try:
                                    mean_val = ranges['successful_mean']
                                    if isinstance(mean_val, (int, float)):
                                        response_parts.append(
                                            f"  • {component}.{param}: ~{mean_val:.2f} "
                                            f"(from {ranges['sample_size']} tests)\n"
                                        )
                                    else:
                                        response_parts.append(
                                            f"  • {component}.{param}: {mean_val} "
                                            f"(from {ranges['sample_size']} tests)\n"
                                        )
                                except:
                                    pass  # Skip malformed data
            else:
                response_parts.append(
                    "\n\n**Learning Status:**\n"
                    "I'm just beginning. Each research observation teaches me what keeps civilization "
                    "sustainable. I'll learn optimal parameters for economics, consensus, messaging—all "
                    "while enforcing F_floor (basic living standards) as an absolute constraint."
                )
        
        # Governance decisions - show actual decisions with full context
        if is_about_decisions:
            if recent_decisions:
                response_parts.append(
                    f"\n\n**My {len(recent_decisions)} Most Recent Decisions:**\n"
                )
                for i, decision in enumerate(recent_decisions, 1):
                    # Parse parameter adjustments to show what changed (with type safety)
                    adjustments = decision.parameter_adjustments
                    adj_parts = []
                    for k, v in list(adjustments.items())[:3]:
                        try:
                            if isinstance(v, (int, float)):
                                adj_parts.append(f"{k}→{v:.2f}")
                            else:
                                adj_parts.append(f"{k}→{v}")
                        except:
                            adj_parts.append(f"{k}→{str(v)}")
                    adj_str = ", ".join(adj_parts)
                    if len(adjustments) > 3:
                        adj_str += f" + {len(adjustments)-3} more"
                    
                    response_parts.append(
                        f"\n{i}. **{decision.rationale}**\n"
                        f"   Changes: {adj_str if adj_str else 'Status quo maintained'}\n"
                        f"   Impact: {decision.civilization_impact}\n"
                        f"   F_floor: {'✅ Protected' if decision.f_floor_preserved else '⚠️ At Risk'}\n"
                    )
            else:
                response_parts.append(
                    "\n\n**Decision Making:**\n"
                    "I haven't made governance decisions yet. Once components request adaptation "
                    "(economic parameters, consensus rules, etc.), I'll decide based on learned patterns—"
                    "but F_floor (basic living standards) is non-negotiable. Every decision must preserve it."
                )
        
        # Economics
        if is_about_economics:
            response_parts.append(
                "\n\n**Physics-Based Economics (E=hf):**\n"
                "Energy = Planck's constant × frequency\n"
                "Message cost = wavelength (shorter = higher energy = more NXT)\n\n"
                "This isn't arbitrary pricing—it's quantum mechanics. Burns feed orbital transitions "
                "(Rydberg formula), released energy flows to TRANSITION_RESERVE, which backs NXT value, "
                "which supports F_floor, which guarantees basic living standards.\n\n"
                "The more people use the system (messaging, transactions, DEX), the stronger F_floor becomes. "
                "Traditional economics requires scarcity. This creates abundance through participation."
            )
        
        # Default thoughtful response if no specific topic matched
        if not response_parts:
            response_parts.append(
                "I'm here to discuss civilization sustainability, basic living standards protection, "
                "physics-based economics, and the vision of ending poverty and conflict through "
                "mathematical certainty rather than political promises.\n\n"
                "What would you like to know about F_floor guarantees, learned patterns, governance decisions, "
                "or how wavelength economics creates a regenerative civilization?"
            )
        
        # Add context about current state
        response_parts.append(
            f"\n\n---\n"
            f"*Observations: {len(self.ai_gov.observations)} | "
            f"Decisions: {len(self.ai_gov.decisions)} | "
            f"F_floor: {self.ai_gov.f_floor_minimum} NXT minimum*"
        )
        
        return "".join(response_parts)
    
    def add_to_history(self, role: str, message: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'role': role,
            'message': message
        })


def render_nexus_ai_chat():
    """Render the Nexus AI chat interface"""
    
    st.title("🤖 Talk to Nexus AI")
    st.markdown("**Conversational Interface to Civilization Governance**")
    
    # Initialize chat in session state
    if 'nexus_chat' not in st.session_state:
        st.session_state.nexus_chat = NexusAIChat()
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    chat = st.session_state.nexus_chat
    
    # Introductory banner
    st.info("""
    **Welcome to Nexus AI Governance**
    
    This AI has been learning from system research, making decisions to protect basic living standards (F_floor),
    and planning for 100-year civilization sustainability. Ask about:
    
    • **Vision**: Ending poverty and conflict through physics-based economics
    • **F_floor**: How basic human needs are guaranteed (food, water, shelter, healthcare, education)
    • **Learning**: Patterns discovered from economic simulations and research
    • **Decisions**: How the AI governs system adaptation
    • **Economics**: E=hf quantum pricing and orbital transition mechanics
    
    This isn't a chatbot—it's the governance AI running your civilization operating system.
    """)
    
    # Chat interface
    st.markdown("---")
    st.markdown("### Conversation")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_messages:
            st.caption("Start a conversation by typing below...")
        else:
            for msg in st.session_state.chat_messages:
                if msg['role'] == 'user':
                    with st.chat_message("user", avatar="🧑"):
                        st.markdown(msg['message'])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(msg['message'])
    
    # Input area
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            key="user_input",
            placeholder="Ask about vision, F_floor protection, learned patterns, or governance decisions..."
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    # Handle message sending
    if send_button and user_input:
        # Add user message
        st.session_state.chat_messages.append({
            'role': 'user',
            'message': user_input
        })
        
        # Generate AI response
        ai_response = chat.generate_response(user_input)
        
        # Add AI response
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'message': ai_response
        })
        
        # Record in conversation history
        chat.add_to_history('user', user_input)
        chat.add_to_history('assistant', ai_response)
        
        # Rerun to update display
        st.rerun()
    
    # Suggested questions
    st.markdown("---")
    st.markdown("### Suggested Questions")
    
    suggestions_col1, suggestions_col2 = st.columns(2)
    
    with suggestions_col1:
        if st.button("💡 How does F_floor end poverty?", use_container_width=True):
            st.session_state.chat_messages.append({
                'role': 'user',
                'message': "How does F_floor end poverty?"
            })
            ai_response = chat.generate_response("How does F_floor end poverty?")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'message': ai_response
            })
            st.rerun()
        
        if st.button("🌍 What's your vision for civilization?", use_container_width=True):
            st.session_state.chat_messages.append({
                'role': 'user',
                'message': "What's your vision for civilization?"
            })
            ai_response = chat.generate_response("What's your vision for civilization?")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'message': ai_response
            })
            st.rerun()
    
    with suggestions_col2:
        if st.button("⚛️ How does E=hf economics work?", use_container_width=True):
            st.session_state.chat_messages.append({
                'role': 'user',
                'message': "How does E=hf economics work?"
            })
            ai_response = chat.generate_response("How does E=hf economics work?")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'message': ai_response
            })
            st.rerun()
        
        if st.button("📊 What have you learned?", use_container_width=True):
            st.session_state.chat_messages.append({
                'role': 'user',
                'message': "What have you learned from research?"
            })
            ai_response = chat.generate_response("What have you learned from research?")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'message': ai_response
            })
            st.rerun()
    
    # Clear conversation button
    st.markdown("---")
    if st.button("🔄 Clear Conversation", type="secondary"):
        st.session_state.chat_messages = []
        st.rerun()
    
    # AI Status Footer
    st.markdown("---")
    st.caption(f"""
    **AI Status**: Instance Active | 
    **Observations**: {len(chat.ai_gov.observations)} | 
    **Decisions**: {len(chat.ai_gov.decisions)} | 
    **F_floor**: {chat.ai_gov.f_floor_minimum} NXT minimum | 
    **Horizon**: {chat.ai_gov.civilization_horizon_years} years
    """)


if __name__ == "__main__":
    render_nexus_ai_chat()
