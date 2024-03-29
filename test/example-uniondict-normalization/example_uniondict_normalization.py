""" Examples adapted from Mecha Munch Management, Alphametrics, and ChatGPT

    ChatGPT Prompt: Write a python function that
       reads user settings from a toml file and
       merges them with a dictionary of default
       settings to create a single dictionary.
       If there are any conflicts between the
       two sources of settings, the data from
       the toml file should be used.
"""


def update_recipes_tuple(ideas, recipe_updates):
    """Mecha Munch Management Example.

    Update the recipe ideas dictionary.
    :param ideas: dict - The "recipe ideas" dict.
    :param recipe_updates: tuple - tuple with updates for the ideas section.
    :return: dict - updated "recipe ideas" dict.
    """
    
     # recipe_updates here is a tuple.
     # Since this action updates the dict in place, 
     # the dict then needs to be returned separately, otherwise it is a syntax error. 
    ideas |= recipe_updates
    return ideas
    
    
def update_recipes_dict(ideas, recipe_updates):
    """Second Mecha Munch Management Example.

    Update the recipe ideas dictionary.
    :param ideas: dict - The "recipe ideas" dict.
    :param recipe_updates: dict - dictionary with updates for the ideas section.
    :return: dict - updated "recipe ideas" dict.
    """
    
     # Since this action returns a *new* dict, it can go directly on the return line.
    return dict(ideas) | dict(recipe_updates)
    
##Example Usage##
ideas  = {'Banana Bread' : {'Banana': 1, 'Apple': 1, 'Walnuts': 1, 'Flour': 1, 'Eggs': 2, 'Butter': 1}}
    
recipe_updates_tuple= (('Banana Bread', {'Banana': 4,  'Walnuts': 2, 'Flour': 1, 'Eggs': 2, 'Butter': 1, 'Milk': 2, 'Eggs': 3}),)
    
recipe_update_dict= {'Banana Bread': {'Banana': 4,  'Walnuts': 2, 'Flour': 1, 'Eggs': 2, 'Butter': 1, 'Milk': 2, 'Eggs': 3}}
    
update_recipes_tuple(ideas, recipe_updates_tuple)
   # {'Banana Bread': {'Banana': 4, 'Walnuts': 2, 'Flour': 1, 'Eggs': 3, 'Butter': 1, 'Milk': 2}}
   
update_recipes_dict(ideas, recipe_update_dict)
   # {'Banana Bread': {'Banana': 4, 'Walnuts': 2, 'Flour': 1, 'Eggs': 3, 'Butter': 1, 'Milk': 2}}


def assign(letters, selections, lefty, righty):
    """ Example from `alphametrics` exercise """

    while letters:
        new_selections = []

        for selection in selections:
            slc, choices = selection

            if letters[0] in [lefty, righty]:
                curr_choices = choices - set([0])

            else:
                curr_choices = choices

            for item in curr_choices:
                actual = slc | {letters[0]: item}  # combine two dictionaries
                new_selections.append((actual, choices - set([item])))

        selections = new_selections
        letters = letters[1:]
    return [slc for slc, _ in selections]


import tomlib

def merge_settings(default_settings, toml_file_path):
    # Load settings from TOML file
    with open(toml_file_path, 'r') as f:
        toml_settings = tomlib.load(f)

    # Merge default settings with settings from TOML file
    merged_settings = dict(default_settings) | dict(toml_settings)
    
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
