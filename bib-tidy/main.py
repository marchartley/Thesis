import re

file_path = '../references_terrain.bib'
# file_path = "test.bib"

with open(file_path, 'r') as file:
    bib_content = file.read()

regex = r"@\w+\{(.*?),\n.*?author .*?{(.*?)},\n.*?title .*?{(.*?)},"
matches = re.finditer(regex, bib_content, re.VERBOSE | re.DOTALL | re.IGNORECASE)


for matchNum, match in enumerate(matches, start=1):
    ID, author, title = match.groups()
    if ID == "":
        print(f"{title}") # by {author}")
