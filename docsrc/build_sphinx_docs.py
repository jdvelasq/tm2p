import os
from pathlib import Path

PACKAGE_NAME = "tm2p"
PACKAGE_ROOT = PACKAGE_NAME
SOURCE_DIR = "docsrc/source"


def read_directory_tree(path):
    files = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isdir(full_path):
            files.extend(read_directory_tree(full_path))
        else:
            files.append(full_path)
    return files


def read_package_directories():
    directories = [
        f"{PACKAGE_ROOT}/ingest",
        f"{PACKAGE_ROOT}/refine",
        f"{PACKAGE_ROOT}/discov",
        f"{PACKAGE_ROOT}/anal",
        f"{PACKAGE_ROOT}/innov",
        f"{PACKAGE_ROOT}/synthes",
        f"{PACKAGE_ROOT}/rep",
    ]
    files = []
    for directory in directories:
        files.extend(read_directory_tree(directory))
    files = sorted(files)
    return files


def clean_file_names(files):
    files = [str(Path(f).relative_to(PACKAGE_ROOT)) for f in files]
    files = [f for f in files if "_internals" not in f]
    files = [f for f in files if "_helpers" not in f]
    files = [f for f in files if ".DS_Store" not in f]
    files = [f for f in files if "/_" not in f]
    return files


def generate_index_mapping(files):
    files = [file for file in files if not file.endswith("__init__.py")]
    mapping = {}
    for file in files:
        parts = file.split("/")
        path = ".".join(parts[:-1])
        filename = parts[-1]
        if path not in mapping:
            mapping[path] = []
        mapping[path].append(filename)
    return mapping


def build_hierarchical_mapping(mapping):

    new_mapping = {**mapping}
    for key in mapping:
        if "." in key:

            key_parts = key.split(".")

            for i in range(1, len(key_parts)):
                key_part = ".".join(key_parts[:i])
                if key_part not in new_mapping:
                    new_mapping[key_part] = []

            for i in range(1, len(key_parts)):
                parts = key_parts[: i + 1]
                parent = ".".join(parts[:-1])
                child = parts[-1]
                if child not in new_mapping[parent]:
                    new_mapping[parent].append(child)

    return new_mapping


def generate_files(mapping):
    for key, children in mapping.items():
        generate_index_file(key, children)
    for key, children in mapping.items():
        generate_final_files(key, children)


def generate_final_files(key, children):
    for child in children:
        generate_final_file(key, child)


def generate_final_file(key, child):

    if not child.endswith(".py"):
        return

    child = child.replace(".py", "")
    filename = f"{SOURCE_DIR}/{key}.{child}.rst"
    automodule = f"{PACKAGE_NAME}.{key}.{child}"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f".. automodule:: {automodule}\n")
        f.write("     :members:\n")
        f.write("     :undoc-members:\n")
        f.write("     :show-inheritance:\n\n")


def delete_existent_files_in_source():
    files = read_directory_tree(SOURCE_DIR)
    for file in files:
        if file.endswith(".rst"):
            os.remove(file)


def generate_index_file(key, children):

    filename = f"{SOURCE_DIR}/{key}.rst"

    with open(filename, "w", encoding="utf-8") as f:
        title = key.split(".")[-1].replace("_", " ").capitalize()
        f.write(title + "\n")
        f.write("#" * 80 + "\n\n")
        f.write(".. toctree::\n")
        f.write("    :maxdepth: 1\n")
        f.write("    :hidden:\n\n")

        for child in children:
            if child.endswith(".py"):
                child = child[:-3]
            f.write(f"    {key}.{child}\n")


def run():

    files = read_package_directories()
    files = clean_file_names(files)
    mapping = generate_index_mapping(files)
    mapping = build_hierarchical_mapping(mapping)
    delete_existent_files_in_source()
    generate_files(mapping)


if __name__ == "__main__":
    run()
