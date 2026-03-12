from pathlib import Path


def extract_section_headers(root_directory: str) -> int:

    from ....rev import ExtractSectionHeaders

    text = (
        ExtractSectionHeaders()
        .where_root_directory(root_directory=root_directory)
        .run()
    )

    filepath = (
        Path(root_directory) / "refine" / "word_lists" / "abstract_section_headers.txt"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        for t in text:
            f.write(t + "\n")

    return len(text)
