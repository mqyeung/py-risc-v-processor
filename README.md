# RISC-V Single-Cycle Processor Simulator

This is a Python-based simulator for a single-cycle RISC-V processor. It's designed to execute RISC-V assembly language programs.

## Components

The simulator is divided into different components representing the different stages of a processor:

- **PC (Program Counter)**: Tracks the current instruction to fetch.
- **Instruction Memory**: Stores and reads instructions.
- **AdderALU**: An ALU (Arithmetic Logic Unit) component for adding and other arithmetic operations.
- **mainALU**: Another ALU for more complex arithmetic operations.
- **ALUctrl**: ALU control unit to determine the operation to be performed.
- **Mux**: Multiplexers for selecting between two data inputs.
- **ANDgate and ORgate**: Logical gates for performing bitwise AND and OR operations.
- **ImmGen**: Generates immediate values used in instructions.
- **ShiftLeft1**: Shifts a value left by 1.
- **Registers**: Simulates registers in a processor.
- **Control Unit**: Determines the control signals for different stages.
- **Decoder**: Decodes instruction to extract fields.

## Running the Simulator

1. Make sure you have Python installed.
2. Run the simulator using the following command:
   ```
   python script.py file.txt
   ```
   Replace `file.txt` with the path to your RISC-V assembly code file.

## How to Use

- The simulator reads RISC-V assembly instructions from the input file.
- It executes the instructions and simulates the behavior of a single-cycle processor.
- The final register values are displayed as the output.

## Example

An example of running the simulator:

```
python script.py my_program.txt
```

## License

This project is open-source and available under the MIT License.

## Author

- Matt Yeung
