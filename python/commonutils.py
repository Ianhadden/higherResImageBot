import os, json

# open a file in the repository using relative path from the root of the repository
def open_file_from_repo_root(relative_path):
    parent_directory = os.path.dirname(os.path.dirname(__file__))
    return open(parent_directory + relative_path)

def get_api_keys():
    return json.load(open_file_from_repo_root('/keys/api-keys.json'))