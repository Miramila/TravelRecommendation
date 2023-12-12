import json

def print_tree(node, indent=0):
    for key, value in node.items():
        if isinstance(value, dict):
            print(' ' * indent + f'{key}:')
            print_tree(value, indent + 2)
        else:
            print(' ' * indent + f'{key}: {value}')

def read_tree_from_json(file_path):
    with open(file_path, 'r') as json_file:
        tree = json.load(json_file)
        return tree

if __name__ == "__main__":
    # Specify the file path where the JSON data is stored
    file_path = "tree_with_states.json"

    # Read the tree from the JSON file
    tree_data = read_tree_from_json(file_path)

    # Print the tree structure neatly
    print_tree(tree_data)
