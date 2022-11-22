# Creating the basic layout of the project manually.

import os

# Directories to be created
dirs = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "notebooks",
    ".logs",
    "saved_models",
    "saved_transformation_objects",
    "src"
]

# Creating the directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

    # just creating a `.gitkeep` file under each dir so that the dir can be pushed to Github.
    with open(os.path.join(dir, ".gitkeep"), "w") as f:
        pass

# Files to be created
files = [
    "params.yaml",
    "requirements.txt",
    os.path.join("src", "__init__.py")
]

# Creating the files
for file in files:
    with open(file, "w") as f:
        f.close()
