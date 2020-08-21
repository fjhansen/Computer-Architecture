"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010 
PRN = 0b01000111
MUL = 0b10100010 
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000
CMP = 0b10100111
EQUAL = 0b00000001
LESS = 0b00000100
GREATER = 0b00000010
JMP = 0b01010100
JLT = 0b01011000
JNE = 0b01010110
JEQ = 0b01010101


class CPU:
    """Main CPU class."""

    def __init__(self):

        self.pc = 0         # We need a counter to keep the index of the next instruction to be carried out
    
        self.reg = [0] * 8  # We need the maximum number of registers. 8
    
        self.ram = [0] * 256 # We need the max ram

        self.SP = 7 # Stack pointer. stores location of next location in stack

        self.FL = 0 # Flag, falsey
        
        self.reg[self.SP] = 0xF4 #244

        # setup jumptable

        self.jumptable={}

        # Week's Repo

        self.jumptable[LDI] = self.LDI

        self.jumptable[PRN] = self.PRN

        self.jumptable[MUL] = self.MUL

        self.jumptable[ADD] = self.ADD

        self.jumptable[PUSH] = self.PUSH # ls8.py examples/stack.ls8

        self.jumptable[POP] = self.POP

        self.jumptable[HLT] = self.HLT

        self.jumptable[CALL] = self.CALL

        self.jumptable[RET] = self.RET

        # Sprint

        self.jumptable[CMP] = self.CMP
        
        self.jumptable[JMP] = self.JMP
        
        self.jumptable[JLT] = self.JLT
        
        self.jumptable[JEQ] = self.JEQ 

        self.jumptable[JNE] = self.JNE
        

    def __repr__(self):
        return str(self.jumptable)
        
        

    def ram_read(self, address):
        return self.ram[address] # returns the given address

    def ram_write(self, value, address):
        self.ram[address] = value # writes the value on given address

    # Handlers

    def LDI(self):
        # Basically sets the register to an index and sets the PC ahead
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
        self.pc +=3
        
    def PRN(self):
        # Handles printing
        print(self.reg[self.ram_read(self.pc +1)])
        self.pc += 2

    def ADD(self):
        # Addition
        regA = self.ram_read(self.pc+1)
        regB = self.ram_read(self.pc+2)
        self.alu("ADD", regA, regB)
        self.pc+=3       

    def MUL(self):
        # Multiplication
        regA = self.ram_read(self.pc + 1)
        regB = self.ram_read(self.pc + 2)
        mul = self.reg[regA] * self.reg[regB]
        self.reg[regA] = mul
        self.pc += 3


    def PUSH(self):
        # Decrease stack pointer
        self.reg[self.SP]-=1
        
        regA = self.ram[self.pc+1]
        
        value = self.reg[regA]
        # We save the values to memory and increase PC
        stack_reg = self.reg[self.SP]
        self.ram[stack_reg] = value
        self.pc +=2
        
    def POP(self):
        if self.reg[self.SP] == 0xF4:
            
            #print("Empty!!")
            
            return "Empty!!!"

        # reg to pop
        regA = self.ram_read(self.pc+1)

        # Copy into register
        self.reg[regA] = self.ram[self.reg[self.SP]]

        # Increment stack pointer to new position
        self.reg[self.SP]+=1
        self.pc+=2


    # for HLT

    def HLT(self):
        # Stop operation
        self.pc +=1
        self.running = False
        return self.running

    def CALL(self):
        # Set return address to instruct next after current subroutine completion
        saved_addr = self.pc + 2
        # Decrease Stack Pointer by 1
        self.reg[self.SP] -= 1
        # Saved address goes on stack
        self.ram[self.reg[self.SP]] = saved_addr
        # Set pc to register through ram
        reg_num = self.ram[self.pc + 1]
        # Subroutine to copy content of program in stack
        subroutine = self.reg[reg_num]
        self.pc = subroutine
        
        
    def RET(self):
        # Set PC to address top of the stack
        saved_addr = self.ram[self.reg[self.SP]]
        # Increase Stack Pointer keep on movin and resume
        self.reg[self.SP] +=1
        # Top
        self.pc = saved_addr


    def CMP(self):
        regA = self.ram_read(self.pc +1)
        regB = self.ram_read(self.pc+2)
        self.alu("CMP",regA,regB)
        self.pc +=3
        

    def JMP(self):
        # Where we jump based on ram using pc+1 as idex
        regA = self.ram[self.pc + 1]
        # then set value based on the reg using saved regA as index for jump
        value = self.reg[regA]
        # Set PC aka next instruction to jump address
        self.pc = value
        

    def JEQ(self):
        # Set flag to Equal and make jump
        if self.FL == EQUAL:
            self.JMP()
        # else keep on movin
        else:
            self.pc+= 2 

    def JNE(self):
        # Same as JEQ but if flag is less or greater
        if self.FL == LESS or self.FL == GREATER:
            self.JMP()
        else:
            self.pc += 2

    def JLT(self):
        # If flag is less
        if self.FL == LESS:
            self.JMP()
        else:
            self.pc += 2
        
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

    def alu(self, op, regA, regB):
        """ALU operations."""

        if op == "ADD":
            self.reg[regA] += self.reg[regB]

        # for multi

        elif op == "MUL":
            self.reg[regA] *= self.reg[regB]

        elif op == "CMP":
            # These are using conditional instructions to jump based
            # on the labels of EQUAL, GREATER, LESS
            if self.reg[regA] == self.reg[regB]:
                self.FL = EQUAL
            if self.reg[regA] > self.reg[regB]:
                self.FL = GREATER
            if self.reg[regA] < self.reg[regB]:
                self.FL = LESS            
        
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
                #self.trace()
                self.jumptable[command]()
                #print("\n PC: \n",self.pc)
                #print(CPU().ram_read(self.pc))
                #print("\n REG: \n",self.reg)
                #print("\n RAM: \n",self.ram)
                

            else:
                print(f"Error: {command}, Address: {self.pc}")
                #print("JT: \n",self.jumptable)
                #print("PC: \n",self.pc)
                #print("REG-E: \n",self.reg)
                #print("RAM-E: \n",self.ram)
                
                sys.exit(1)



        #ls8.py examples/mult.ls8
        #ls8.py examples/sctest.ls8

            

