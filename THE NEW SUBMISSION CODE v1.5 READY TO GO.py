import sys
class AdderALU: #used for pc+4 as well as offset calculations
    def __init__(self):
        self.input1 = 0
        self.input2 = 0

    def adder(self, input1, input2):
        self.input1 = input1
        self.input2 = input2
        return self.input1 + self.input2

class mainALU: # usage is equal, result = mainALU(input1, input2, data_signal).execute()
    def __init__(self):
        self.input1 = 0b0
        self.input2 = 0b0
        self.data_signal = 0b0
    
    def execute(self, input1, input2, data_signal):
        self.input1 = input1
        self.input2 = input2
        self.data_signal = data_signal
        lessthan = input1 < input2 #i have to do if statements here since python doesnt accept dynamic operation insertion
        if   self.data_signal == 0b000: result = self.input1 + self.input2 # Addition
        elif self.data_signal == 0b001: result = self.input1 - self.input2 # Subtraction
        elif self.data_signal == 0b010: result = self.input1 ^ self.input2 # XOR (bitwise)
        elif self.data_signal == 0b011: result = self.input1 < self.input2 # Less than comparison     
        elif self.data_signal == 0b100: result = self.input1 >> self.input2 # SRA (Arithmetic Right Shift)  
        elif self.data_signal == 0b101: result = self.input1 & self.input2 # AND Immediate (andi)
        else: raise ValueError("Invalid data signal")
        return lessthan, result
    
class ALUctrl: #usage: result = ALUctrl(aluop=1, imm30=1, funct3=0b000, opcode).execute()
    def __init__(self):
        self.imm30 = 0
        self.funct3 = 0
        self.opcode = 0
        self.aluop = 0

    def execute(self, alu_ctrl_in, aluop):
        self.imm30 = (alu_ctrl_in >> 10) & 0x1
        self.funct3 = (alu_ctrl_in >> 7) & 0x7
        self.opcode = alu_ctrl_in & 0x7F
        self.aluop = aluop

        if self.aluop == 1:
            if self.opcode == 0b0110011: #r type
                if self.funct3 == 0b000:
                    if self.imm30 == 0b0: return 0b000 # add
                    elif self.imm30 == 0b1: return 0b001 # sub
                elif self.funct3 == 0b100: return 0b010 # xor
                elif self.funct3 == 0b101: return 0b100 # sra
            elif self.opcode == 0b0010011: #i type
                if self.funct3 == 0b000: return 0b000 #reusing the 000 instr because adding two lines tgt. this is addi
                elif self.funct3 == 0b111: return 0b101 # andi
            elif self.opcode == 0b0000011: #lw
                if self.funct3 == 0b010: return 0b000 #reusing the 000 instr because adding two lines tgt
            elif self.opcode == 0b0100011: #sw
                if self.funct3 == 0b010: return 0b000 #again reusing 000 adding instr because we can 
            elif self.opcode == 0b1100011: #b type
                if self.funct3 == 0b100: return 0b011 #branch less than
            elif self.opcode == 0b1100111: #jalr
                if self.funct3 == 0b000: return 0b000 #jalr running a no op basically

        raise ValueError("Invalid ALU control signals")

class Mux: #usage is output = Mux(input0, input1).select(data_in)
    def __init__(self):
        self.input0 = 0
        self.input1 = 0
        self.data_signal = 0

    def select(self, input0, input1, data_signal):
        self.input0 = input0
        self.input1 = input1
        self.data_signal = data_signal
        if self.data_signal == 0: return self.input0
        elif self.data_signal == 1: return self.input1
        else: raise ValueError("Data signal must be 0 or 1")

class ANDgate: #usage: result = ANDgate(branch1, branch2).check()
    def __init__(self):
        self.value1 = 0b0
        self.value2 = 0b0

    def check(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        return self.value1 == 0b1 and self.value2 == 0b1

class ORgate: # Usage: result = ORgate(branch1, branch2).check()
    def __init__(self):
        self.value1 = 0b0
        self.value2 = 0b0

    def check(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        return self.value1 == 0b1 or self.value2 == 0b1

class ImmGen: #usage: result = ImmGen(instruction).execute()
    def __init__(self):
        pass

    def execute(self, instruction):
        imm = 0
        opcode = instruction & 0x7F
        if opcode == 0x13 or opcode == 0x3 or opcode == 0x67:
            imm = instruction >> 20
            imm = imm if imm & (1 << 11) == 0 else imm - (1 << 12)
                # i dont see why imm has to be standardized into 64 so i wont be doing that
        imm = ((instruction >> 25) & 0x1) << 5 | ((instruction >> 7) & 0x1F) << 0 if opcode == 0x23 else imm #s-type
        imm = ((instruction >> 31) & 0x1) << 20 | ((instruction >> 21) & 0xA) << 1 | ((instruction >> 20) & 0x1) << 11 | ((instruction >> 12) & 0xFF) << 12 if opcode == 0x6F else imm #j-type
        imm = ((instruction >> 31) & 1) << 12 | ((instruction >> 25) & 0x3F) << 5 | ((instruction >> 7) & 1) << 11 | ((instruction >> 8) & 0xF) << 1 if opcode == 0x63 else imm #b-type
        return imm #dont need to specifically say 32bit return since this is python

class ShiftLeft1: #usage: result = ShiftLeft1(initial_value)
    def __init__(self):
        self.value = 0

    def execute(self, value):
        self.value = value
        return self.value << 0 #this is set to 0 because we already shifted in the immgen

class PC: #usage pc.write(new_pc_value), or pc.read() to read
    def __init__(self, initial_value=0):
        self.value = initial_value

    def read(self):
        return self.value

    def write(self, new_value):
        self.value = new_value

#instantiate these below, below are memory
class Registers: #instantiate this, registers = Registers(), but afterwards `read_data_1, read_data_2 = registers.read(5, 15)` or `registers.write(5, 123, RegWrite)`
    def __init__(self):
        # Initialize 32 registers with zero values
        self.registers = [0] * 32

    def read(self, read_register1, read_register2):
        # Read data from the registers based on the read_register values
        read_data_1 = self.registers[read_register1]
        read_data_2 = self.registers[read_register2]
        return read_data_1, read_data_2

    def write(self, write_register, write_data, RegWrite):
        # Write data to the register if RegWrite is enabled
        if RegWrite: self.registers[write_register] = write_data

class InstructionMemory: # instruction = instruction_memory.read(pc_to_read), or, when initializing, write by doing instruction_memory.write(hex_instructions)
    def __init__(self):
        self.instructions = {}

    def write(self, hex_instructions):
        # Append the provided hex instructions to the instruction dictionary
        pc = len(self.instructions) * 4
        for instruction in hex_instructions:
            self.instructions[pc] = instruction
            pc += 4

    def read(self, pc):
        #pc = pc & -4  # Ensure the PC is aligned to a multiple of 4
        if pc not in self.instructions:
            raise IndexError("Invalid program counter (PC) value")
        return self.instructions[pc]

class DataMemory: #usage: define ``data_memory = DataMemory()`` first then ``data_memory.write(4, 123, memwrite=True)``or ``read_data = data_memory.read_data(4)``
    def __init__(self):
        self.memory = {}
        self.size = 32

    def read(self, address, memread):
        if memread:
            if address % 4 == 0 and 0 <= address < self.size:
                return self.memory.get(address, 0) #defaults to 0
            else:
                raise ValueError("Invalid memory address")

    def write(self, address, write_data, memwrite):
        if memwrite:
            if address % 4 == 0 and 0 <= address < self.size:
                self.memory[address] = write_data

class Control:
    def __init__(self):
        pass

    def control_unit(self, opcode):
        self.jump = 0b0
        self.branch = 0b0 #this takes the place of blt instead of beq, because we dont need beq so...
        self.memread = 0b0
        self.memtoreg = 0b0
        self.aluop = 0b0
        self.memwrite = 0b0
        self.alusrc = 0b0
        self.regwrite = 0b0
        # Determine control signals based on the opcode
        if opcode == 0x13:  # I-Type instructions
            self.alusrc = 0b1
            self.aluop = 0b1
            self.regwrite = 0b1

        elif opcode == 0x3:  # I-Type Load instructions (e.g., lw)
            self.aluop = 0b1
            self.memread = 0b1
            self.memtoreg = 0b1
            self.alusrc = 0b1 #takes it from imm
            self.regwrite = 0b1

        elif opcode == 0x23:  # S-Type or Store instructions (e.g., sw)
            self.aluop = 0b1
            self.memwrite = 0b1
            self.alusrc = 0b1 #oll korrect

        elif opcode == 0x33:  # R-Type instructions (e.g., add, sub)
            self.aluop = 0b1  # For ALU control, e.g., for add, sub
            self.regwrite = 0b1 #gud
            
        elif opcode == 0x63:  # B-Type instructions (e.g., blt)
            self.branch = 0b1
            self.aluop = 0b1
    
        elif opcode == 0x67:  # I-Type JALR instruction #you would access instr memory not data memory
            self.jump = 0b1
            self.aluop = 0b1
            self.alusrc = 0b1
            self.regwrite = 0b1
            

        return self.jump, self.branch, self.memread, self.memtoreg, self.aluop, self.memwrite, self.alusrc, self.regwrite

class Decoder:
    def __init__(self):
        pass

    def decode(self, instruction):
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        inst30 = (instruction >> 30) & 0x1
        funct3 = (instruction >> 12) & 0x7

        # Combine inst30, funct3, and opcode into alu_ctrl_in
        alu_ctrl_in = (inst30 << 10) | (funct3 << 7) | opcode

        return opcode, rs1, rs2, rd, instruction, alu_ctrl_in

def parse_instructions(filename):
    instructions = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 4:
                try: instructions.append(int(parts[1], 16))
                except (ValueError, IndexError): pass

    return instructions


def run(filename):

    #fetch stage components
    pc = PC()
    instruction_memory = InstructionMemory()
    side_alu_plus_4 = AdderALU()

    #decode stage components
    decoder = Decoder()
    registers = Registers()
    immgen = ImmGen()
    control_unit = Control()

    #execute stage components
    slt = ShiftLeft1()
    mux_pre_alu = Mux() 
    mux_pc = Mux() 
    mux_mem = Mux() 
    mux_wb = Mux() 
    mux_jump = Mux()
    aluctrl = ALUctrl()
    main_alu = mainALU()
    side_alu = AdderALU()
    andgate = ANDgate()
    orgate = ORgate()

    #memory stage components
    data_memory = DataMemory()
    

    hex_instructions = parse_instructions(filename)
    instruction_memory.write(hex_instructions)

    while pc.read() != len(hex_instructions)*4:
        #instruction fetch
        pc_wire = pc.read()
        instruction_wire = instruction_memory.read(pc_wire)
        pc_plus_4_wire = side_alu_plus_4.adder(pc.read(),4)
        
        #instruction decode (would normally be in fetch stage but just for clarity this is in decode)
        opcode_wire, rs1_wire, rs2_wire, rd_wire, instruction_wire, alu_ctrl_in= decoder.decode(instruction_wire) 
        #i know its bad practice to say instruction wire comes out of decode but it doesnt change so its okay here


        #instruction decode pt2 (for standard decode)
        jump_wire, branch_wire, memread_wire, memtoreg_wire, aluop_wire, memwrite_wire, alusrc_wire, regwrite_wire = control_unit.control_unit(opcode_wire)

        rs1_out, rs2_out = registers.read(rs1_wire, rs2_wire)

        imm_wire_out = immgen.execute(instruction_wire)
        
        #execute stage
        slt_wire_out = slt.execute(imm_wire_out)

        alu_in_wire_1 = rs1_out
        alu_in_wire_2 = mux_pre_alu.select(rs2_out, imm_wire_out, alusrc_wire)

        alu_ctrl_out = aluctrl.execute(alu_ctrl_in, aluop_wire)

        #execute pt2
        rear_alu_out = side_alu.adder(pc.read(), slt_wire_out)
        alu_lessthan_out, alu_result = main_alu.execute(alu_in_wire_1,
        alu_in_wire_2, alu_ctrl_out)

        #execute pt3
        and_out = andgate.check(branch_wire, alu_lessthan_out)
        
        #memory stage
        data_memory.write(alu_result, rs2_out, memwrite_wire)
        memory_out = data_memory.read(alu_result, memread_wire)

        write_data_wire = mux_mem.select(alu_result, memory_out, memtoreg_wire)

        #writeback stage
        mux_wb_out = mux_wb.select(write_data_wire,pc_plus_4_wire, jump_wire)
        registers.write(rd_wire,mux_wb_out,regwrite_wire)

        mux_pc_out = mux_pc.select(pc_plus_4_wire, rear_alu_out, and_out)
        new_pc = mux_jump.select(mux_pc_out, alu_result, jump_wire)
        pc.write(new_pc)

    print("Register Values:")
    print(f"x10: {registers.registers[10]}")
    print(f"x11: {registers.registers[11]}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py file.txt")
        sys.exit(1)

    filename = sys.argv[1]
    run(filename)