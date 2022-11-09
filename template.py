# Creating the basic layout of the project manually.

import os

# directories name
dirs = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "notebooks",
    "saved_models",
    "logs",
    "src"
]

# creating the directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

    # just creating a `.gitkeep` file under each dir so that the dir can be pushed to Github.
    with open(os.path.join(dir, ".gitkeep"), "w") as f:
        pass

# files to be created
files = [
    "params.yaml",
    "requirements.txt",
    os.path.join("src", "__init__.py")
]

# creating the files
for file in files:
    with open(file, "w") as f:
        f.close()
