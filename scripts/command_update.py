import json
import re
import os

# Define the path to your LaTeX file and settings.json
custom_commands_paths = ['./customizedCommands.tex', './glossary.tex']
settings_json_path = os.path.expanduser('~/.config/VSCodium/User/settings.json')

if not (os.path.exists(custom_commands_paths[0]) and os.path.exists(custom_commands_paths[1])):
	exit(0)



def extract_arguments(name, example_line):
    # Regex to match the command/environment followed by its arguments
    pattern = re.compile(r'%\s*\\' + re.escape(name) + r'\s*' + r'({[^}]*})' * 100)  # 100 is arbitrary high number to capture many args
    match = pattern.search(example_line)
    return match.groups() if match else None

# Parse LaTeX file for \zzcommand definitions, capturing preceding comments with arguments
def parse_latex_commands(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    commands = {}
    cmd_pattern = re.compile(r'\\zzcommand{\\(\w+)}(?:\[(\d+)\])?', re.DOTALL)
    env_pattern = re.compile(r'\\newenvironment{(\w+)}')

    for i, line in enumerate(lines):
        env_match = env_pattern.search(line)
        cmd_match = cmd_pattern.search(line)

        if cmd_match:
            cmd_name, num_args = cmd_match.groups()
            example_args = []

            # Prepare regex to find example usage with arguments in the preceding comment
            if i > 0 and lines[i-1].strip().startswith('%'):
                example_line = lines[i-1].strip()
                # Regex to match the command followed by its arguments
                example_pattern = re.compile(r'%\s*\\' + re.escape(cmd_name) + r'\s*' + r'{([^}]*)}' * (int(num_args) if num_args else 0))
                example_match = example_pattern.search(example_line)
                if example_match:
                    # Extract arguments from the example
                    example_args = example_match.groups()


            if example_args:
                args_template = "" if num_args is None else "{" + "}{".join("${" + str(i+1) + ("" if example_args[i].startswith("|") and example_args[i].endswith("|") else ":")  + example_args[i] + "}" for i in range(int(num_args))) + "}"
                snippet = f"{cmd_name}{args_template}"
            else:
                args_template = "" if num_args is None else "{" + "}{".join(f"${i}" for i in range(1, int(num_args) + 1)) + "}"
                snippet = f"{cmd_name}{args_template}"
            commands[cmd_name] = snippet
        
        if env_match:
            env_name = env_match.group(1)
            # Collect multiple preceding comment lines
            j = i - 1
            example_lines = []
            while j >= 0 and lines[j].strip().startswith('%'):
                example_lines.insert(0, lines[j].replace('% ', '') )#.replace("\\\\", ""))
                j -= 1
            example_lines[0] = example_lines[0].lstrip("\\") # Don't know why but I need to remove the initial "\" from begin
            commands[env_name] = "".join(example_lines)  # Join all gathered comment lines as the example

    # exit(0)
    return commands

# Parse JSON with comments
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

# Write JSON with comments
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

# Main process
commands = {}
for tex_file_path in custom_commands_paths:
    commands.update(parse_latex_commands(tex_file_path))
settings, comments = parse_json_with_comments(settings_json_path)

# Update settings with new commands
if "latex-workshop.intellisense.command.user" not in settings:
    settings["latex-workshop.intellisense.command.user"] = {}
settings["latex-workshop.intellisense.command.user"].update(commands)

# Write back to settings.json
write_json_with_comments(settings, comments, settings_json_path)
