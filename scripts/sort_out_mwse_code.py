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

def contains_openmw(path):
    if 'openmw' in path.lower():
        return True
    
    if os.path.isfile(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return 'openmw' in file.read().lower()
        except Exception:
            return False
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            if any('openmw' in item.lower() for item in dirs + files):
                return True
            for file in files:
                file_path = os.path.join(root, file)
                if contains_openmw(file_path):
                    return True
    return False

def should_process_folder(folder_path, mod_name, index_data):
    # Check if the mod is in the index and after January 1st, 2024
    mod_entry = index_data.get(mod_name)
    if not mod_entry or not is_after_january_2024(mod_entry.get('indexed_timestamp', 0)):
        return False
    
    # Check for exclusions
    if 'mwse' in mod_name.lower() or 'tes3mp' in mod_name.lower():
        return False
    
    # Check for OpenMW mention
    return contains_openmw(folder_path)

def safe_copy(src, dst):
    if os.path.exists(dst):
        if os.path.isdir(dst):
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                safe_copy(s, d)
        else:
            os.remove(dst)
            shutil.copy2(src, dst)
    else:
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