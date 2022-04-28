
import sys
import pickle
from utils import alphanumeric

global my_dfa

def read(file_dir):
    current_file = open(file_dir, "r", encoding="latin-1")
    lines = current_file.read()
    characters = []
    for line in lines:
        for char in line:
            characters.append(char)
    return characters

my_dfa = pickle.load(open("./temporal", "rb"))

file_name = None
if len(sys.argv) > 1: 
    file_name = sys.argv[1]
if not file_name:
    raise Exception('Use: python3 generated_lexer.py <FILE>')
characters = read(file_name)
current_state = alphanumeric[0]
value = ""
for index, character in enumerate(characters):
    if character in my_dfa.to_ignore and index > len(characters)-1:
        pass
    if character in my_dfa.transitions[current_state]:
        value += character
        current_state = my_dfa.transitions[current_state][character]
        continue
    else:
        if(character not in my_dfa.to_ignore):
            value += character
    if current_state in my_dfa.final_states:
        token = list(
            filter(
                lambda node: "#-" in node.value and node._id 
                in my_dfa.accepting_dictionary[current_state], my_dfa.nodes))[0]
        node_type = token.value.split("#-")[1]
                        
        if node_type == "{token.ident}" and value in my_dfa.keywords_values:
            keyword = list(filter(lambda x: x.value.value == value, my_dfa.keywords))[0]
            node_type = keyword.value.value
                                
        if value:
            print(f"Token:",repr(value[:-1]), "Type:", node_type)
        value = character
        if not character in my_dfa.transitions[alphanumeric[0]]:
            print(f"Token:",repr(value[:-1]), "Type: None")
            value = ""
            current_state = alphanumeric[0]
            continue
        current_state = my_dfa.transitions[alphanumeric[0]][character]
