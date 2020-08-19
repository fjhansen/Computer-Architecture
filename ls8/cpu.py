"""CPU functionality."""

import sys

HLT = 0b00000001 #1
LDI = 0b10000010 #130
PRN = 0b01000111 #71
MUL = 0b10100010 #162

class CPU:
    """Main CPU class."""

    def __init__(self):

        self.pc = 0         # We need a counter to keep the index of the current instruction
    
        self.reg = [0] * 8  # We need the maximum number of registers. 8
    
        self.ram = [0] * 256 # We need the max ram

        # setup jumptable

        self.jumptable={}

        self.jumptable[LDI] = self.handle_ldi

        self.jumptable[PRN] = self.handle_prn

        self.jumptable[MUL] = self.handle_mul
        
        

        

    def ram_read(self, address):
        return self.ram[address] # returns the given address

    def ram_write(self, value, address):
        self.ram[address] = value # writes the value on given address

    # Handlers

    def handle_ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc +=3
        
    def handle_prn(self):
        print(self.reg[self.ram_read(self.pc +1)])
        self.pc += 2

    def handle_mul(self):
        regA = self.ram_read(self.pc + 1)
        regB = self.ram_read(self.pc + 2)
        mul = self.reg[regA] * self.reg[regB]
        self.reg[regA] = mul
        self.pc += 3

        
    # Loading

    def load(self):
        filename = sys.argv[1]
        address = 0
        with open(filename) as filehandle:
            for line in filehandle:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(v, address)
                address += 1
      

##        address = 0
##
##        # For now, we've just hardcoded a program:
##
##        program = [
##            # From print8.ls8
##            0b10000010, # LDI R0,8
##            0b00000000,
##            0b00001000,
##            0b01000111, # PRN R0
##            0b00000000,
##            0b00000001, # HLT
##        ]
##
##        for instruction in program:
##            self.ram[address] = instruction
##            address += 1


    def alu(self, op, regA, regB):
        """ALU operations."""

        if op == "ADD":
            self.reg[regA] += self.reg[regB]
        
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):

        command = LDI
        self.jumptable[command]()

        command = LDI
        self.jumptable[command]()

        command = MUL
        self.jumptable[command]()

        command = PRN
        self.jumptable[command]()
        
##        """Run the CPU."""
##        HLT = 0b00000001 #1
##        LDI = 0b10000010 #2
##        PRN = 0b01000111 #PRN R0
##
##        running = True
##
##        while running:
##            command = self.ram_read(self.pc)
##            regA = self.ram_read(self.pc +1)
##            regB = self.ram_read(self.pc +2)
##
##        if command == HLT:
##            running = False
##            self.pc +=1
##
##        elif command == LDI:
##            self.reg[regA] = regB
##            self.pc +=3
##
##        elif command == PRN:
##            print(self.registers[register_1])
##            self.pc +=2
##
##        else:
##            print(f"Unknown Instruction: {command}")
##            sys.exit(1)


        #ls8.py examples/mult.ls8

            

