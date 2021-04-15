import os, json

PARENT_DIRECTORY = os.path.dirname(os.path.dirname(__file__))

# open a file in the repository using relative path from the root of the repository
# optionally takes mode to use with the open
def open_file_from_repo_root(relative_path, m="r"):
    return open(PARENT_DIRECTORY + relative_path, m)

def get_api_keys():
    return json.load(open_file_from_repo_root('/keys/api-keys.json'))

def does_file_exist_from_repo_root(relative_path):
    return os.path.exists(PARENT_DIRECTORY + relative_path)

def create_directory_from_repo_root(relative_path):
    os.mkdir(PARENT_DIRECTORY + relative_path)