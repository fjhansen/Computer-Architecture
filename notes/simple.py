import sys
# define function with OP code of 1

PRINT_FRAN = 1
HALT       = 2
PRINT_NUM  = 3
SAVE       = 4 # SAVING VALUE TO A REGISTER
PRINT_REG  = 5 # PRINT A VALUE FROM A REGISTER
ADD        = 6 # regA += regB



memory = [None] * 256

##
##memory = [
##
##    PRINT_FRAN,
##    SAVE,
##    65,
##    2,
##    SAVE,
##    20,
##    3,
##    ADD,
##    2,
##    3,
##    PRINT_REG,
##    2,
##    HALT
##
##    
####    PRINT_FRAN,
####    PRINT_NUM,
####    1,
####    PRINT_NUM,
####    12,
####    PRINT_FRAN,
####    PRINT_NUM,
####    37,
####    PRINT_FRAN,
####    PRINT_FRAN,
####    HALT
##    
##]


# holding 8 bit values 
register = [0] * 8

# Create program 
pc = 0

# To check if our program is still running
running = True




def load_memory(filename):
    address = 0
    try:
        with open(filename) as f:
            
            for line in f:
                #print(line)

                # Ignore comments
                comment_split = line.split("#")

                # strip whitespace
                num = comment_split[0].strip()

                # Ignore blank lines
                if num == '':
                    continue
                #print(num)
                val = int(num)
                memory[address] = val
                address += 1

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)

if len(sys.argv) !=2:
    print("usage: simple.py filename")
    sys.exit(1)

filename = sys.argv[1]
load_memory(filename)


#file.py add.simple









# Repl

while running:
    # shows which instruction is being pointed to
    command = memory[pc]

    if command == PRINT_FRAN:
        print("Fran!")
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == PRINT_NUM:
        num = memory[pc +1]
        print(num)
        pc += 2

    elif command == SAVE:
        num = memory[pc+1]
        reg = memory[pc+2] # reg is a num between 0-7
        register[reg] = num
        pc += 3

    elif command == PRINT_REG:
        reg = memory[pc+1]
        print(register[reg])
        pc+=2

    elif command == ADD:
        reg_a = memory[pc+1]
        reg_b = memory[pc+2]
        register[reg_a] += register[reg_b]
        pc += 3

    else:
        print(f"Unknown Instruction: {command}")
        sys.exit(1)

    

