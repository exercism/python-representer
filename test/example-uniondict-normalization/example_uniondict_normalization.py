
"""
 This exmple comes from ChatGPT
 Prompt: Write a python function that 
       reads user settings from a toml file and 
       merges them with a dictionary of default 
       settings to create a single dictionary. 
       If there are any conflicts between the 
       two sources of settings, the data from 
       the toml file should be used.
"""
import toml

def merge_settings(default_settings, toml_file_path):
    # Load settings from TOML file
    with open(toml_file_path, 'r') as f:
        toml_settings = toml.load(f)

    # Merge default settings with settings from TOML file
    merged_settings = default_settings | toml_settings
    
    return merged_settings

# Example usage:
default_settings = {
    'timeout': 30,
    'retry_count': 3,
    'log_level': 'INFO'
}
toml_file_path = 'settings.toml'  # Path to the TOML file

final_settings = merge_settings(default_settings, toml_file_path)
print("Final Settings:", final_settings)




""" Examples from PEP584 - Add Union Operators To dict"""
d = {'spam': 1, 'eggs': 2, 'cheese': 3}
e = {'cheese': 'cheddar', 'aardvark': 'Ethel'}
# d | e   # Representer fails, result must be assigned. # TODO Fix this ????
# e | d   # Representer fails
x = d | e   # {'spam': 1, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}
y = e | d   # {'cheese': 3, 'aardvark': 'Ethel', 'spam': 1, 'eggs': 2}
d |= e  # {'spam': 1, 'eggs': 2, 'cheese': 'cheddar', 'aardvark': 'Ethel'}





""" Examples from the Cpython unit tests"""
a = {0: 0, 1: 1, 2: 1}
b = {1: 1, 2: 2, 3: 3}

c = a.copy()
c |= b

assert a | b == {0: 0, 1: 1, 2: 2, 3: 3}
assert c == {0: 0, 1: 1, 2: 2, 3: 3}

c = b.copy()
c |= a

assert b | a == {1: 1, 2: 1, 3: 3, 0: 0}
assert c == {1: 1, 2: 1, 3: 3, 0: 0}

c = a.copy()
c |= [(1, 1), (2, 2), (3, 3)]

assert c == {0: 0, 1: 1, 2: 2, 3: 3}




""" Example from `alphametrics` exercise """
def assign(letters, selections, lefty, righty):
    while letters:
        new_selections = []

        for selection in selections:
            slc, choices = selection

            if letters[0] in [lefty, righty]:
                curr_choices = choices - set([0])

            else:
                curr_choices = choices

            for i in curr_choices:
                actual = slc | {letters[0]: i}  # combine two dictionaries
                new_selections.append((actual, choices - set([i])))

        selections = new_selections
        letters = letters[1:]
    return [slc for slc, _ in selections]

