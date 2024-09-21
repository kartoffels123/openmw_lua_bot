import os
import shutil
import json
import datetime

def load_index(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return {mod['name']: mod for mod in data['lua_mods']}

def is_after_january_2024(timestamp):
    return datetime.datetime.fromtimestamp(timestamp) > datetime.datetime(2024, 1, 1)

def contains_openmw_require(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if "require('openmw" in line:
                    return True
    except Exception:
        pass
    return False

def should_process_folder(folder_path, mod_name, index_data):
    mod_entry = index_data.get(mod_name)
    if not mod_entry or not is_after_january_2024(mod_entry.get('indexed_timestamp', 0)):
        return False
    
    if 'mwse' in mod_name.lower() or 'tes3mp' in mod_name.lower():
        return False
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.lua'):
                if contains_openmw_require(os.path.join(root, file)):
                    return True
    return False

def safe_copy(src, dst):
    if os.path.exists(dst):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        else:
            os.remove(dst)
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

def process_directory(source_dir, target_dir, index_path):
    index_data = load_index(index_path)
    
    for mod_folder in os.listdir(source_dir):
        mod_path = os.path.join(source_dir, mod_folder)
        if os.path.isdir(mod_path):
            if should_process_folder(mod_path, mod_folder, index_data):
                target_path = os.path.join(target_dir, mod_folder)
                safe_copy(mod_path, target_path)
                print(f"Copied: {mod_folder}")
            else:
                print(f"Skipped: {mod_folder}")

# Usage
source_directory = 'data-actual-code/morrowind-nexus-lua-dump-master/lua'
target_directory = 'data-actual-code/openmw'
index_file = 'data-actual-code/morrowind-nexus-lua-dump-master/index.json'
process_directory(source_directory, target_directory, index_file)