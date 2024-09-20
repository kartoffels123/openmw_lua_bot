import os
import json

def process_lua_files(directory):
    result = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    result[relative_path] = content
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")
    return result

def create_master_json(base_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for folder in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            lua_files = process_lua_files(folder_path)
            if lua_files:
                output_file = os.path.join(output_directory, f"{folder}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "folder_name": folder,
                        "lua_files": lua_files
                    }, f, indent=2, ensure_ascii=False)
                print(f"Created JSON for {folder}")
            else:
                print(f"No Lua files found in {folder}")

# Usage
base_directory = 'data-actual-code/openmw'  # The directory containing the mod folders
output_directory = 'data-actual-code/openmw_lua_json'  # Where to save the JSON files

create_master_json(base_directory, output_directory)