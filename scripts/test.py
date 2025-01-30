import json
import re
import os

# Define the path to your settings.json
settings_json_path = os.path.expanduser('~/.config/VSCodium/User/settings.json')

# Function to parse the settings JSON file, preserving comments
def parse_json_with_comments(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    json_lines = []
    comments = {}
    for i, line in enumerate(lines):
        if '//' in line:
            comment_pos = line.index('//')
            comments[i] = line[comment_pos:].strip()
            json_lines.append(line[:comment_pos])
        else:
            json_lines.append(line)

    json_content = json.loads(''.join(json_lines))
    return json_content, comments

# Function to write the settings JSON file, reintroducing comments
def write_json_with_comments(data, comments, file_path):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    lines = json_str.splitlines()

    with open(file_path, 'w') as file:
        comment_keys = sorted(comments.keys())
        comment_idx = 0

        for i, line in enumerate(lines):
            while comment_idx < len(comment_keys) and comment_keys[comment_idx] <= i:
                file.write(comments[comment_keys[comment_idx]] + '\n')
                comment_idx += 1
            file.write(line + '\n')

        # Write remaining comments (if any) at the end of the file
        while comment_idx < len(comment_keys):
            file.write(comments[comment_keys[comment_idx]] + '\n')
            comment_idx += 1

# Parse and re-write the JSON file
settings, comments = parse_json_with_comments(settings_json_path)
write_json_with_comments(settings, comments, settings_json_path)
