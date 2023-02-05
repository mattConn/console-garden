import json

null_char = '_'

def make_memory_string(memory):
    memory_string = ''
    for row in memory:
        for col in row:
            if col is None:
                col = null_char
            memory_string += col
        memory_string += '\n'

    return (True, memory_string)

def validate_address(address_row, address_col):
    try:
        address_row = int(address_row)
        address_col = int(address_col)
    except ValueError:
        return (False, 'Address must be a number.')

    def valid_address(address):
        return 0 <= address < 10

    if not valid_address(address_row) or not valid_address(address_col):
        return (False, 'Address must be between 0 and 9.')

    return (True, 'Address is valid.')

def scroll(_):
    for i in range(10):
        print()
    return (True, None)

def memory_operator(num_operands=2):
    def operator(func):
        def validate_operands(memory, *operands):
            if not operands:
                return (False, 'No operands given.')

            if len(operands) != num_operands:
                return (False, 'Wrong number of operands.')

            address_row, address_col, *_ = operands
            address_is_valid = validate_address(address_row, address_col)
            if not address_is_valid[0]:
                return address_is_valid

            return func(memory, *operands)
        return validate_operands
    return operator

@memory_operator()
def show(memory, *operands):
    address_row, address_col, *_ = operands
    value = memory[int(address_row)][int(address_col)]
    if not value:
        value = 'Empty.'

    return (True, value)

@memory_operator(num_operands=3)
def make(memory, *operands):
    address_row, address_col, value, *_ = operands

    if len(value) > 1:
        return (False, 'Value must be a single character.')

    memory[int(address_row)][int(address_col)] = value 

    return (True, 'Wrote to memory.')

@memory_operator()
def clear(memory, *operands):
    address_row, address_col, *_ = operands
    memory[int(address_row)][int(address_col)] = None

    return (True, 'Cleared memory.')


def save_memory(memory):
    with open('memory.txt', 'w') as f:
        for row in memory:
            for col in row:
                if not col:
                    col = null_char 
                f.write(col)
            f.write('\n')

    return (True, 'Saved to memory.txt.')

def load_memory(memory):
    with open('memory.txt', 'r') as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line):
                if char == '\n':
                    break
                if char == null_char:
                    char = None
                memory[i][j] = char

    return (True, 'Loaded from memory.txt.')

def load_state(state_dict):
    # load state from state.json
    with open('state.json', 'r') as f:
        state = json.load(f)

    state_dict['time'] = state['time']
    return (True, 'Loaded state from state.json.')

def save_state(state_dict):
    # save state to state.json
    with open('state.json', 'w') as f:
        json.dump(state_dict, f)

    return (True, 'Saved state to state.json.')

def time(_, state_dict):
    return (True, state_dict['time'])

operators_dict = {
    'make': (make, 'Make a new variable.'),
    'show': (show, 'Show value in memory.'),
    'save': (save_memory, 'Save memory to file.'),
    'load': (load_memory, 'Load memory from file.'),
    'clear': (clear, 'Clear a variable.'),
    'scroll': (scroll, 'Scroll the screen.'),
    'memory': (make_memory_string, 'Show the memory.'),
    'time': (time, 'Show the time.'),
}