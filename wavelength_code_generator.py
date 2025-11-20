"""
Wavelength Programming Language (WaveLang) - Write code using electromagnetic wave mechanics

Revolutionary concept: Code structure mapped to spectral regions and wave properties.
Instead of traditional syntax, programs are represented as wavelength patterns.

Key Ideas:
1. Spectral Regions = Code sections (RED=arithmetic, BLUE=logic, GREEN=memory)
2. Wavelengths = Instructions (specific wavelengths = specific operations)
3. Modulation = Computational complexity (OOK=simple, QAM64=complex)
4. Amplitude = Priority (higher amplitude = higher priority execution)
5. Phase = Conditional branching (phase shift determines if/else)
6. DAG = Execution flow (parent messages = dependencies)
7. E=hf = Energy budget (quantum energy determines loop iterations)
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import math
from wavelength_validator import SpectralRegion, ModulationType, WaveProperties

# Physical constants
PLANCK_CONSTANT = 6.626e-34  # J·s
SPEED_OF_LIGHT = 3e8  # m/s

# Wavelength to instruction mapping
class WavelengthOpcodes(Enum):
    """Wavelength-to-instruction mapping"""
    # Arithmetic operations (Violet: 380-450nm)
    ADD = 380.0          # Addition
    SUBTRACT = 386.0     # Subtraction
    MULTIPLY = 392.0     # Multiplication
    DIVIDE = 398.0       # Division
    MODULO = 404.0       # Modulo
    POWER = 410.0        # Exponentiation
    
    # Logical operations (Blue: 450-495nm)
    AND = 450.0          # Logical AND
    OR = 462.0           # Logical OR
    NOT = 474.0          # Logical NOT
    XOR = 486.0          # Logical XOR
    
    # Memory operations (Green: 495-570nm)
    LOAD = 495.0         # Load from memory
    STORE = 508.0        # Store to memory
    PUSH = 521.0         # Push to stack
    POP = 534.0          # Pop from stack
    
    # Control flow (Yellow: 570-590nm)
    IF = 570.0           # Conditional jump
    LOOP = 578.0         # Loop start
    BREAK = 586.0        # Loop break
    
    # Function operations (Orange: 590-620nm)
    CALL = 590.0         # Function call
    RETURN = 600.0       # Return from function
    DEFINE = 610.0       # Define function
    
    # I/O operations (Red: 620-750nm)
    INPUT = 620.0        # Read input
    OUTPUT = 635.0       # Write output
    PRINT = 650.0        # Print value


class ControlFlowMode(Enum):
    """Phase-based conditional branching"""
    SEQUENTIAL = 0.0       # Phase 0: straight execution
    IF_TRUE = math.pi / 2  # Phase 90°: if condition true
    IF_FALSE = math.pi     # Phase 180°: if condition false
    LOOP_WHILE = 3*math.pi/2  # Phase 270°: while loop


class DataType(Enum):
    """Data types encoded via modulation"""
    INTEGER = ModulationType.OOK      # Simple 1-bit data
    FLOAT = ModulationType.PSK        # Phase-based precision
    STRING = ModulationType.QAM16     # 4-bit per symbol
    COMPLEX = ModulationType.QAM64    # 6-bit per symbol (max complexity)


@dataclass
class WavelengthInstruction:
    """Single instruction represented as a wavelength"""
    opcode: WavelengthOpcodes
    wavelength_nm: float
    spectral_region: SpectralRegion
    modulation: ModulationType
    amplitude: float = 0.5  # 0=low priority, 1=high priority
    phase: float = 0.0     # 0=sequential, π/2=if-true, π=if-false, 3π/2=loop
    operand1: Optional[Any] = None
    operand2: Optional[Any] = None
    
    def get_quantum_energy(self) -> float:
        """E = hf - quantum energy determines execution cost"""
        frequency = SPEED_OF_LIGHT / (self.wavelength_nm * 1e-9)
        return PLANCK_CONSTANT * frequency
    
    def get_execution_cost_nxt(self) -> float:
        """Convert quantum energy to NXT economic units"""
        energy = self.get_quantum_energy()
        BASE_JOULES_PER_NXT = 1e-15
        return energy / BASE_JOULES_PER_NXT
    
    def to_dict(self) -> Dict:
        """Serialize instruction"""
        return {
            'opcode': self.opcode.name,
            'wavelength_nm': self.wavelength_nm,
            'spectral_region': self.spectral_region.name,
            'modulation': self.modulation.display_name,
            'amplitude': self.amplitude,
            'phase_degrees': math.degrees(self.phase),
            'quantum_energy_eV': self.get_quantum_energy() / 1.602176634e-19,
            'execution_cost_nxt': self.get_execution_cost_nxt(),
            'operand1': str(self.operand1),
            'operand2': str(self.operand2)
        }


@dataclass
class WaveLangFunction:
    """Function represented as a sequence of wavelength instructions"""
    name: str
    instructions: List[WavelengthInstruction]
    input_params: List[str]
    output_type: DataType
    
    def get_total_energy_budget(self) -> float:
        """Calculate total quantum energy (execution budget) for function"""
        return sum(inst.get_quantum_energy() for inst in self.instructions)
    
    def get_spectral_composition(self) -> Dict[str, int]:
        """Show which spectral regions this function uses"""
        composition = {}
        for inst in self.instructions:
            region = inst.spectral_region.name
            composition[region] = composition.get(region, 0) + 1
        return composition
    
    def to_dict(self) -> Dict:
        """Serialize function"""
        return {
            'name': self.name,
            'instruction_count': len(self.instructions),
            'input_params': self.input_params,
            'output_type': self.output_type.name,
            'total_energy_joules': self.get_total_energy_budget(),
            'spectral_composition': self.get_spectral_composition(),
            'instructions': [inst.to_dict() for inst in self.instructions]
        }


class WavelengthCodeGenerator:
    """Generate code using wavelength mechanics"""
    
    def __init__(self):
        self.functions: Dict[str, WaveLangFunction] = {}
        self.memory_map: Dict[str, Any] = {}
        self.execution_log: List[str] = []
    
    def map_wavelength_to_opcode(self, wavelength_nm: float) -> Optional[WavelengthOpcodes]:
        """Map wavelength to nearest opcode"""
        min_diff = float('inf')
        closest_opcode = None
        
        for opcode in WavelengthOpcodes:
            diff = abs(opcode.value - wavelength_nm)
            if diff < min_diff:
                min_diff = diff
                closest_opcode = opcode
        
        return closest_opcode if min_diff < 10 else None  # Allow ±10nm tolerance
    
    def get_spectral_region(self, wavelength_nm: float) -> SpectralRegion:
        """Determine spectral region from wavelength"""
        if wavelength_nm < 400:
            return SpectralRegion.UV
        elif wavelength_nm < 450:
            return SpectralRegion.VIOLET
        elif wavelength_nm < 495:
            return SpectralRegion.BLUE
        elif wavelength_nm < 570:
            return SpectralRegion.GREEN
        elif wavelength_nm < 590:
            return SpectralRegion.YELLOW
        elif wavelength_nm < 620:
            return SpectralRegion.ORANGE
        elif wavelength_nm < 750:
            return SpectralRegion.RED
        else:
            return SpectralRegion.IR
    
    def create_arithmetic_function(
        self,
        name: str,
        operation: str,  # 'add', 'multiply', etc.
        param1: float = 0,
        param2: float = 0,
        amplitude: float = 0.8
    ) -> WaveLangFunction:
        """
        Create arithmetic function as wavelength sequence.
        
        Example: add(5, 3)
        - LOAD param1 (wavelength 495nm) - load 5
        - LOAD param2 (wavelength 495nm) - load 3
        - ADD (wavelength 380nm) - add them
        - RETURN (wavelength 600nm) - return result
        """
        
        op_map = {
            'add': (WavelengthOpcodes.ADD, 380.0),
            'subtract': (WavelengthOpcodes.SUBTRACT, 386.0),
            'multiply': (WavelengthOpcodes.MULTIPLY, 392.0),
            'divide': (WavelengthOpcodes.DIVIDE, 398.0),
        }
        
        opcode, wavelength = op_map.get(operation, (WavelengthOpcodes.ADD, 380.0))
        
        instructions = [
            # Load parameters
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=495.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=amplitude,
                operand1=param1
            ),
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=508.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=amplitude,
                operand1=param2
            ),
            # Perform operation
            WavelengthInstruction(
                opcode=opcode,
                wavelength_nm=wavelength,
                spectral_region=SpectralRegion.VIOLET,
                modulation=ModulationType.PSK,
                amplitude=amplitude,
                operand1=param1,
                operand2=param2
            ),
            # Return result
            WavelengthInstruction(
                opcode=WavelengthOpcodes.RETURN,
                wavelength_nm=600.0,
                spectral_region=SpectralRegion.ORANGE,
                modulation=ModulationType.OOK,
                amplitude=amplitude
            ),
        ]
        
        return WaveLangFunction(
            name=name,
            instructions=instructions,
            input_params=[str(param1), str(param2)],
            output_type=DataType.FLOAT
        )
    
    def create_conditional_function(
        self,
        name: str,
        condition_wavelength: float = 450.0  # Blue (logic)
    ) -> WaveLangFunction:
        """
        Create conditional function using phase-based branching.
        
        Phase encoding:
        - 0° (phase=0): normal execution
        - 90° (phase=π/2): if true branch
        - 180° (phase=π): if false branch
        - 270° (phase=3π/2): loop
        """
        
        instructions = [
            # Load condition value
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=495.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
            # IF statement (phase=π/2 means true branch)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.IF,
                wavelength_nm=570.0,
                spectral_region=SpectralRegion.YELLOW,
                modulation=ModulationType.PSK,
                amplitude=0.9,
                phase=math.pi / 2  # 90° phase = IF TRUE
            ),
            # True branch: output result
            WavelengthInstruction(
                opcode=WavelengthOpcodes.OUTPUT,
                wavelength_nm=635.0,
                spectral_region=SpectralRegion.RED,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1="true"
            ),
            # False branch (phase=π)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.IF,
                wavelength_nm=570.0,
                spectral_region=SpectralRegion.YELLOW,
                modulation=ModulationType.PSK,
                amplitude=0.9,
                phase=math.pi  # 180° phase = IF FALSE
            ),
            # False branch: output result
            WavelengthInstruction(
                opcode=WavelengthOpcodes.OUTPUT,
                wavelength_nm=635.0,
                spectral_region=SpectralRegion.RED,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1="false"
            ),
            # Return
            WavelengthInstruction(
                opcode=WavelengthOpcodes.RETURN,
                wavelength_nm=600.0,
                spectral_region=SpectralRegion.ORANGE,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
        ]
        
        return WaveLangFunction(
            name=name,
            instructions=instructions,
            input_params=["condition"],
            output_type=DataType.INTEGER
        )
    
    def create_loop_function(
        self,
        name: str,
        iterations: int = 5
    ) -> WaveLangFunction:
        """
        Create loop function using phase-based iteration.
        
        Phase = 3π/2 (270°) indicates loop construct.
        Quantum energy (E=hf) determines loop iterations:
        - Higher frequency = more iterations (RED=750nm freq is lower than VIOLET=380nm)
        - Lower frequency = fewer iterations
        """
        
        instructions = [
            # Initialize counter
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=495.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1=0
            ),
            # Loop start (phase=3π/2 = 270°)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOOP,
                wavelength_nm=578.0,
                spectral_region=SpectralRegion.YELLOW,
                modulation=ModulationType.PSK,
                amplitude=0.9,
                phase=3 * math.pi / 2  # 270° phase = LOOP
            ),
            # Body: increment
            WavelengthInstruction(
                opcode=WavelengthOpcodes.ADD,
                wavelength_nm=380.0,
                spectral_region=SpectralRegion.VIOLET,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1=1,
                operand2=0
            ),
            # Print iteration
            WavelengthInstruction(
                opcode=WavelengthOpcodes.PRINT,
                wavelength_nm=650.0,
                spectral_region=SpectralRegion.RED,
                modulation=ModulationType.OOK,
                amplitude=0.7
            ),
            # Loop end check (energy budget determines remaining iterations)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.BREAK,
                wavelength_nm=586.0,
                spectral_region=SpectralRegion.YELLOW,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
            # Return
            WavelengthInstruction(
                opcode=WavelengthOpcodes.RETURN,
                wavelength_nm=600.0,
                spectral_region=SpectralRegion.ORANGE,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
        ]
        
        return WaveLangFunction(
            name=name,
            instructions=instructions,
            input_params=[f"iterations={iterations}"],
            output_type=DataType.INTEGER
        )
    
    def create_complex_algorithm(self, name: str) -> WaveLangFunction:
        """Create complex algorithm: Fibonacci sequence using wavelength mechanics"""
        
        instructions = [
            # Initialize a=0, b=1
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=495.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1=0  # a
            ),
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOAD,
                wavelength_nm=508.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=0.8,
                operand1=1  # b
            ),
            # Loop (calculate next Fibonacci number)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.LOOP,
                wavelength_nm=578.0,
                spectral_region=SpectralRegion.YELLOW,
                modulation=ModulationType.PSK,
                amplitude=0.9,
                phase=3 * math.pi / 2  # Loop with 270° phase
            ),
            # temp = a + b
            WavelengthInstruction(
                opcode=WavelengthOpcodes.ADD,
                wavelength_nm=380.0,
                spectral_region=SpectralRegion.VIOLET,
                modulation=ModulationType.PSK,
                amplitude=0.85
            ),
            # a = b, b = temp (swap via memory)
            WavelengthInstruction(
                opcode=WavelengthOpcodes.STORE,
                wavelength_nm=521.0,
                spectral_region=SpectralRegion.GREEN,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
            # Output Fibonacci number
            WavelengthInstruction(
                opcode=WavelengthOpcodes.OUTPUT,
                wavelength_nm=635.0,
                spectral_region=SpectralRegion.RED,
                modulation=ModulationType.OOK,
                amplitude=0.7
            ),
            # Return
            WavelengthInstruction(
                opcode=WavelengthOpcodes.RETURN,
                wavelength_nm=600.0,
                spectral_region=SpectralRegion.ORANGE,
                modulation=ModulationType.OOK,
                amplitude=0.8
            ),
        ]
        
        return WaveLangFunction(
            name=name,
            instructions=instructions,
            input_params=["n"],
            output_type=DataType.INTEGER
        )
    
    def register_function(self, func: WaveLangFunction) -> None:
        """Register a function"""
        self.functions[func.name] = func
    
    def get_program_summary(self) -> Dict[str, Any]:
        """Get summary of all registered functions"""
        total_energy = sum(f.get_total_energy_budget() for f in self.functions.values())
        total_instructions = sum(len(f.instructions) for f in self.functions.values())
        
        return {
            'function_count': len(self.functions),
            'total_instructions': total_instructions,
            'total_energy_joules': total_energy,
            'functions': {name: func.to_dict() for name, func in self.functions.items()}
        }


# Example: Create a complete wavelength program
def create_example_wavelength_program() -> WavelengthCodeGenerator:
    """Create example program demonstrating all wavelength programming concepts"""
    
    gen = WavelengthCodeGenerator()
    
    # Arithmetic function: add two numbers
    add_func = gen.create_arithmetic_function("add", "add", 5, 3)
    gen.register_function(add_func)
    
    # Arithmetic function: multiply
    mult_func = gen.create_arithmetic_function("multiply", "multiply", 4, 7)
    gen.register_function(mult_func)
    
    # Conditional function
    if_func = gen.create_conditional_function("conditional_check")
    gen.register_function(if_func)
    
    # Loop function
    loop_func = gen.create_loop_function("count_up", iterations=10)
    gen.register_function(loop_func)
    
    # Complex algorithm: Fibonacci
    fib_func = gen.create_complex_algorithm("fibonacci")
    gen.register_function(fib_func)
    
    return gen


if __name__ == "__main__":
    program = create_example_wavelength_program()
    summary = program.get_program_summary()
    
    print("=" * 80)
    print("WAVELENGTH PROGRAMMING LANGUAGE (WaveLang) - EXAMPLE PROGRAM")
    print("=" * 80)
    print(f"Functions: {summary['function_count']}")
    print(f"Total Instructions: {summary['total_instructions']}")
    print(f"Total Quantum Energy: {summary['total_energy_joules']:.2e} Joules")
    print()
    
    for func_name, func_data in summary['functions'].items():
        print(f"\n{func_name.upper()}")
        print("-" * 40)
        print(f"  Instructions: {func_data['instruction_count']}")
        print(f"  Energy Budget: {func_data['total_energy_joules']:.2e} J")
        print(f"  Spectral Composition: {func_data['spectral_composition']}")
