from operators import * 
from config import *
from aliases import *

memory = [[None for i in range(10)] for j in range(10)]
state = {
    'time': 0,
}
exit_command = 'quit'

print('-- Console Garden --')

if config_dict['autoload']:
    print(load_memory(memory)[1])
    print(load_state(state)[1])

while True:
    current_time = state['time']
    user_input = input(str(current_time)+": ")
    if not user_input:
        state['time'] += 1
        continue

    user_input_words = user_input.split()

    operator_key = user_input_words[0]
    # resolve alias
    if operator_key in aliases_dict:
        operator_key = aliases_dict[operator_key]

    operands = user_input_words[1:]
    if operator_key == exit_command:
        if config_dict['autosave']:
            print(save_memory(memory)[1])
            print(save_state(state)[1])
        print("Goodbye!")
        break

    if operator_key not in operators_dict:
        print("I don't know how to do that.")
        continue

    operator = operators_dict[operator_key][0]

    result_tuple = operator(memory, *operands)
    if not result_tuple[0]:
        print("Error: "+result_tuple[1])
        continue

    if result_tuple[1]:
        print(result_tuple[1])

    state['time'] += 1
    
