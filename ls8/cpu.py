"""CPU functionality."""

import sys

HLT = 0b00000001 #1
LDI = 0b10000010 #130
PRN = 0b01000111 #71
MUL = 0b10100010 #162
POP = 0b01000110 #70
PUSH = 0b01000101 #69
CALL = 0b01010000 #80
RET = 0b00010001 #17

class CPU:
    """Main CPU class."""

    def __init__(self):

        self.pc = 0         # We need a counter to keep the index of the current instruction
    
        self.reg = [0] * 8  # We need the maximum number of registers. 8
    
        self.ram = [0] * 256 # We need the max ram

        self.SP = 7
        
        self.reg[self.SP] = 0xF4 #244

        # setup jumptable

        self.jumptable={}

        self.jumptable[LDI] = self.handle_ldi

        self.jumptable[PRN] = self.handle_prn

        self.jumptable[MUL] = self.handle_mul

        self.jumptable[PUSH] = self.handle_push # ls8.py examples/stack.ls8

        self.jumptable[POP] = self.handle_pop

        self.jumptable[HLT] = self.handle_HLT

        self.jumptable[CALL] = self.handle_CALL

        self.jumptable[RET] = self.handle_RET

    def __repr__(self):
        return str(self.jumptable)
        
        

        

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


    def handle_push(self):
        self.reg[self.SP]-=1
        
        regA = self.ram[self.pc+1]
        
        value = self.reg[regA]
        
        stack_reg = self.reg[self.SP] # stack pointer hold address
        self.ram[stack_reg] = value
        self.pc +=2
        
    def handle_pop(self):
        if self.reg[self.SP] == 0xF4:
            
            #print("Empty!!")
            
            return "Empty!!!"
        regA = self.ram_read(self.pc+1)
        
        self.reg[regA] = self.ram[self.reg[self.SP]]
        
        self.reg[self.SP]+=1
        self.pc+=2


    # for HLT

    def handle_HLT(self):
        self.pc +=1
        self.running = False
        return self.running

    def handle_CALL(self):
        # jump to any address with CALL... create address to return to
        # do this with pop in RET
        # edit cpu_run handler
        # ADD JMP
        pass

        
        

    def handle_RET(self):
        # deal with subroutine
        # POP from stack and save
        # set SP +1
        # set address to jump back
        pass
        
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

        # for multi

        elif op == "MUL":
            self.reg[regA] *= self.reg[regB]
        
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

        self.running = True
        while self.running:
            command = self.ram[self.pc]
            if command in self.jumptable:
                self.jumptable[command]()
                #print("\n PC: \n",self.pc)
                #print(CPU().ram_read(self.pc))
                #print("\n REG: \n",self.reg)
                #print("\n RAM: \n",self.ram)
                

            else:
                print(f"Error: {command}, Address: {self.pc}")
                print("JT: \n",self.jumptable)
                print("PC: \n",self.pc)
                print("REG-E: \n",self.reg)
                print("RAM-E: \n",self.ram)
                
                sys.exit(1)

##        command = LDI
##        self.jumptable[command]()
##
##        command = LDI
##        self.jumptable[command]()
##
##        command = MUL
##        self.jumptable[command]()
##
##        command = PRN
##        self.jumptable[command]()

        
        
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

            

