"""Dashboard for Wavelength Programming Language (WaveLang)"""

import streamlit as st
import json
from wavelength_code_generator import (
    create_example_wavelength_program,
    WavelengthCodeGenerator,
    WavelengthOpcodes
)

def render_wavelength_code_dashboard():
    """Display wavelength programming concepts and examples"""
    
    st.header("🌊 Wavelength Programming Language (WaveLang)")
    st.markdown("**Write code using electromagnetic wave mechanics instead of traditional syntax**")
    
    st.info("""
    💡 **Revolutionary Concept**: Programs are represented as wavelength patterns where:
    - 🎨 **Spectral Regions** = Code sections (RED=arithmetic, BLUE=logic, GREEN=memory)
    - 📊 **Wavelengths** = Instructions (380nm=ADD, 450nm=AND, 495nm=LOAD, etc.)
    - 📈 **Modulation** = Complexity (OOK=simple, QAM64=complex)
    - 💪 **Amplitude** = Priority (0.5=low, 1.0=high priority)
    - 🔄 **Phase** = Branching (0°=sequential, 90°=if-true, 180°=if-false, 270°=loop)
    - ⚡ **E=hf** = Execution budget (quantum energy determines cost/iterations)
    - 🔗 **DAG** = Control flow (parent messages = dependencies)
    """)
    
    tabs = st.tabs([
        "📚 Concepts",
        "💻 Code Examples",
        "📊 Program Analysis",
        "🔬 Instruction Set"
    ])
    
    with tabs[0]:
        render_concepts_tab()
    
    with tabs[1]:
        render_code_examples_tab()
    
    with tabs[2]:
        render_program_analysis_tab()
    
    with tabs[3]:
        render_instruction_set_tab()


def render_concepts_tab():
    """Explain WaveLang concepts"""
    
    st.subheader("1️⃣ Spectral Regions = Code Organization")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Violet (380-450nm)**: Arithmetic
        - ADD (380nm), SUBTRACT (386nm)
        - MULTIPLY (392nm), DIVIDE (398nm)
        
        **Blue (450-495nm)**: Logic
        - AND (450nm), OR (462nm)
        - NOT (474nm), XOR (486nm)
        
        **Green (495-570nm)**: Memory
        - LOAD (495nm), STORE (508nm)
        - PUSH (521nm), POP (534nm)
        """)
    
    with col2:
        st.markdown("""
        **Yellow (570-590nm)**: Control Flow
        - IF (570nm), LOOP (578nm)
        - BREAK (586nm)
        
        **Orange (590-620nm)**: Functions
        - CALL (590nm), RETURN (600nm)
        - DEFINE (610nm)
        
        **Red (620-750nm)**: I/O
        - INPUT (620nm), OUTPUT (635nm)
        - PRINT (650nm)
        """)
    
    st.divider()
    
    st.subheader("2️⃣ Phase-Based Control Flow")
    st.markdown("""
    | Phase | Meaning | Example |
    |-------|---------|---------|
    | 0° (phase=0) | Sequential | Normal execution |
    | 90° (phase=π/2) | IF TRUE | Execute if condition true |
    | 180° (phase=π) | IF FALSE | Execute if condition false |
    | 270° (phase=3π/2) | LOOP | Repeat execution |
    """)
    
    st.subheader("3️⃣ Quantum Energy Cost (E=hf)")
    st.markdown("""
    Each instruction costs quantum energy based on:
    - **Frequency** (from wavelength) determines base cost
    - **Modulation complexity** adds premium
    - **Amplitude** (priority) can increase cost
    
    Higher energy = More computational resources = Longer execution time
    
    Example: RED (650nm) instruction costs less than VIOLET (380nm) instruction
    because red light has lower frequency.
    """)


def render_code_examples_tab():
    """Show code examples"""
    
    program = create_example_wavelength_program()
    
    st.subheader("📝 Example Functions")
    
    selected_func = st.selectbox(
        "Select function to view:",
        list(program.functions.keys())
    )
    
    if selected_func:
        func = program.functions[selected_func]
        func_data = func.to_dict()
        
        st.markdown(f"**Function**: `{func_data['name']}`")
        st.markdown(f"**Input**: {', '.join(func_data['input_params'])}")
        st.markdown(f"**Output Type**: `{func_data['output_type']}`")
        st.markdown(f"**Total Energy**: {func_data['total_energy_joules']:.2e} Joules")
        
        st.divider()
        
        st.markdown("**Instructions**:")
        
        # Display instructions as table
        instructions = []
        for inst in func_data['instructions']:
            instructions.append({
                'Wavelength (nm)': inst['wavelength_nm'],
                'Region': inst['spectral_region'],
                'Operation': inst['opcode'],
                'Modulation': inst['modulation'],
                'Amplitude': f"{inst['amplitude']:.1f}",
                'Phase (°)': f"{inst['phase_degrees']:.0f}",
                'Cost (NXT)': f"{inst['execution_cost_nxt']:.6f}"
            })
        
        st.dataframe(instructions, use_container_width=True)


def render_program_analysis_tab():
    """Analyze the example program"""
    
    program = create_example_wavelength_program()
    summary = program.get_program_summary()
    
    st.subheader("📊 Program Composition")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Functions",
            summary['function_count'],
            help="Number of functions in program"
        )
    
    with col2:
        st.metric(
            "Total Instructions",
            summary['total_instructions'],
            help="Total wavelength instructions"
        )
    
    with col3:
        energy_mj = summary['total_energy_joules'] * 1e6
        st.metric(
            "Total Energy",
            f"{energy_mj:.2f} μJ",
            help="Quantum energy budget"
        )
    
    st.divider()
    
    st.subheader("🎨 Spectral Composition (All Functions)")
    
    # Aggregate spectral usage
    spectral_usage = {}
    for func_name, func_data in summary['functions'].items():
        for region, count in func_data['spectral_composition'].items():
            spectral_usage[region] = spectral_usage.get(region, 0) + count
    
    cols_data = []
    for region, count in sorted(spectral_usage.items()):
        cols_data.append({
            'Spectral Region': region,
            'Instructions': count,
            'Percentage': f"{100 * count / summary['total_instructions']:.1f}%"
        })
    
    st.dataframe(cols_data, use_container_width=True)
    
    st.divider()
    
    st.subheader("💾 Individual Function Energy")
    
    energy_data = []
    for func_name, func_data in summary['functions'].items():
        energy_data.append({
            'Function': func_name,
            'Instructions': func_data['instruction_count'],
            'Energy (J)': f"{func_data['total_energy_joules']:.2e}"
        })
    
    st.dataframe(energy_data, use_container_width=True)


def render_instruction_set_tab():
    """Display complete instruction set"""
    
    st.subheader("🔬 Complete WaveLang Instruction Set")
    
    st.markdown("""
    Each instruction is uniquely identified by its wavelength, which falls into
    one of 8 spectral regions. The instruction set includes 20 opcodes.
    """)
    
    # Build instruction table
    instructions = []
    for opcode in WavelengthOpcodes:
        wavelength = opcode.value
        # Determine region
        if wavelength < 400:
            region = "UV"
        elif wavelength < 450:
            region = "Violet"
        elif wavelength < 495:
            region = "Blue"
        elif wavelength < 570:
            region = "Green"
        elif wavelength < 590:
            region = "Yellow"
        elif wavelength < 620:
            region = "Orange"
        elif wavelength < 750:
            region = "Red"
        else:
            region = "IR"
        
        instructions.append({
            'Opcode': opcode.name,
            'Wavelength (nm)': wavelength,
            'Spectral Region': region,
            'Category': 'Arithmetic' if wavelength < 420 else
                       'Logic' if wavelength < 490 else
                       'Memory' if wavelength < 540 else
                       'Control' if wavelength < 600 else
                       'Function' if wavelength < 630 else
                       'I/O'
        })
    
    st.dataframe(instructions, use_container_width=True)
    
    st.divider()
    
    st.subheader("📊 Opcode Distribution by Category")
    
    categories = {}
    for inst in instructions:
        cat = inst['Category']
        categories[cat] = categories.get(cat, 0) + 1
    
    cat_data = [{'Category': k, 'Count': v} for k, v in sorted(categories.items())]
    st.dataframe(cat_data, use_container_width=True)


if __name__ == "__main__":
    render_wavelength_code_dashboard()
