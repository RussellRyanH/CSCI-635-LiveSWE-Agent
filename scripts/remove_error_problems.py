'''In the event that certain problems error out during execution, 
this script removes trajectories and json entry from the resutls folder.
In particular, I have set up to remove rate limit errors runs, so I can rerun the failed ones.'''

import os
import shutil
import yaml
import json

def parse_yaml_list(file_path, key):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    value = data.get("instances_by_exit_status").get(key)

    if not isinstance(value, list):
        raise ValueError(f"The key '{key}' does not contain a YAML list.")

    return value

def remove_subdirs(parent_directory, subdirs_to_remove):
    # List of subdirectories to remove
    for subdir in subdirs_to_remove:
        full_path = os.path.join(parent_directory, subdir)

        if os.path.isdir(full_path):
            try:
                shutil.rmtree(full_path)
                print(f"Removed: {full_path}")
            except Exception as e:
                print(f"Error removing {full_path}: {e}")
        else:
            print(f"Not found or not a directory: {full_path}")

def delete_preds_entries(file_path, keys_to_remove):

    with open(file_path, "r") as f:
        data = json.load(f)

    # Remove keys
    for key in keys_to_remove:
        if key in data:
            del data[key]

    # Overwrite original file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Updated file: {file_path}")


def main ():
    # Parent directory that contains the subdirectories
    parent_directory = "../results/llm-ablation/gpt-5-mini/"
    exit_stat_file = "exit_statuses_1773615734.5967455.yaml"
    key = "RateLimitError"

    subdirs_to_remove = parse_yaml_list(parent_directory + exit_stat_file, key)
    remove_subdirs(parent_directory, subdirs_to_remove)
    delete_preds_entries(parent_directory + "preds.json", subdirs_to_remove)


if __name__ == '__main__':
    main()
