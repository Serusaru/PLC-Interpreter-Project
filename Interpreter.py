import sys

program_filepath = sys.argv[1]


program_lines = []
with open(program_filepath,"r") as program_file:
    program_lines = [line.strip() for line in program_file.readlines()]

program =[]
token_counter = 0
label_traker = {}
for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue

    if opcode.endswith(":"):
        label_traker[opcode[:-1]] = token_counter
        continue

    program.append(opcode)
    token_counter += 1

    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    
    elif opcode == "PRINT":

        string_literal = ' '.join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "JUMP.EQ.0": # Checks if top of stack is equal to 0

        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "JUMP.GT.0": # Checks if top of stack is greater than 0

        label = parts[1]
        program.append(label)
        token_counter += 1
    

class Stack:
    
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp  = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number
    
    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number
    
    def top(self):
        return self.buf[self.sp]
    
pc = 0
stack = Stack(256)

while program[pc] != "HALT":
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH": # Appends a value to the stack
        number = program[pc]
        pc += 1

        stack.push(number)
    elif opcode == "POP": # Removes the top value of the stack and holds it for usage
        stack.pop()
    elif opcode == "MULT": # Multiplies the top two integers in the stack
        a = stack.pop()
        b = stack.pop()
        stack.push(a*b)
    elif opcode == "DIV": # Divides the second highest integer in the stack by the top integer in the stack
        a = stack.pop()
        b = stack.pop()
        stack.push(b/a)
    elif opcode == "ADD": # Adds the top two integers in the stack
        a = stack.pop()
        b = stack.pop()
        stack.push(a+b)
    elif opcode == "SUB": # Subtracts the second highest integer in the stack by the top integer in the stack
        a = stack.pop()
        b = stack.pop()
        stack.push(b-a)
    elif opcode == "PRINT": # Prints the given string literal in the terminal
        string_literal = program[pc]
        pc += 1 
        print(string_literal)
    elif opcode == "READ": # Prompts user input
        number = int(input())
        stack.push(number)
    elif opcode == "JUMP.EQ.0": # Conditonal to check if the top value of the stack is equal to 0
        number = stack.top()
        if number == 0:
            pc = label_traker[program[pc]]
    elif opcode == "JUMP.GT.0": # Conditonal to check if the top value of the stack is greater than 0
        number = stack.top()
        if number > 0:
            pc = label_traker[program[pc]]
        else:
            pc += 1
    elif opcode == "RETURN": # Returns the top value of the stack in the terminal
        number = stack.top()
        print(number)



'''
Test Files

Test by typing python (or python 3) commands into the terminal when running
python3 interpreter.py (test file name).oll
Enter variables for READ calls
Verify intended output

equaltest.oll

Enter 2 integer
Returns "not equal" if they are unequal, prints "equal" otherwise 
(Checks if second variable - first variable is equal to 0)

eventtest.oll

Enter 1 integer
Returns "odd" if the number is odd, prints "even" otherwise
(Subtracts the number you enter by 2 until you reach 0, proving the number even, or until you are below 0, returning an odd number)

tripletest.oll

Enter 1 integer
Returns the integer you entered multiplied by 3, then the original integer (as a result of dividing by 3), then the original number + 3
'''