from pathlib import Path


def extract_acronyms(root_directory: str) -> int:

    from ....rev import ExtractAcronyms

    acronyms = (
        ExtractAcronyms().where_root_directory(root_directory=root_directory).run()
    )

    filepath = Path(root_directory) / "refine" / "word_lists" / "acronyms.txt"

    with open(filepath, "w", encoding="utf-8") as file:
        sorted_acronyms = sorted(acronyms.keys())
        for acronym in sorted_acronyms:
            print(acronym, file=file)
            for definition in sorted(acronyms[acronym]):
                print(f"    {definition}", file=file)

    return len(acronyms)
