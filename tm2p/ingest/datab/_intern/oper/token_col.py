# CODE_REVIEW: 2026-01-23

import unicodedata

import contractions  # type: ignore
import pandas as pd  # type: ignore
from nltk.tokenize import word_tokenize  # type: ignore

from tm2p import Field
from tm2p._intern.packag_data import load_builtin_mapping

from ._file_dispatch import get_file_operations

_URL_PATTERN: str = (
    r"http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
)

_FULL_WIDTH_TO_ASCII = {
    "。": ".",  # Full-width period
    "，": ",",  # Full-width comma
    "：": ":",  # Full-width colon
    "；": ";",  # Full-width semicolon
    "！": "!",  # Full-width exclamation mark
    "？": "?",  # Full-width question mark
    "（": "(",  # Full-width opening parenthesis
    "）": ")",  # Full-width closing parenthesis
    "“": '"',  # Full-width double quote
    "”": '"',  # Full-width double quote
    "‘": "'",  # Full-width single quote
    "’": "'",  # Full-width single quote
}


_NOUN_PHRASE_CORRECTIONS = [
    (
        "architectural , engineering , construction , and operation",
        "architectural engineering construction and operation",
    ),
    (
        "agriculture , forestry , and other land use",
        "agriculture forestry and other land use",
    ),
    (
        "combined cooling , heating , and power systems",
        "combined cooling heating and power systems",
    ),
    (
        "energy consumption , carbon emission and cost",
        "energy consumption carbon emission and cost",
    ),
    (
        "environmental , social , governance",
        "environmental social and governance",
    ),
    (
        "green building council south africa",
        "green building council of south africa",
    ),
    (
        "political , economic , social , technological , environmental , and legal",
        "political economic social technological environmental and legal",
    ),
    (
        "repair , maintenance and improvement",
        "repair maintenance and improvement",
    ),
    (
        "swedish national board of housing , building , and planning",
        "swedish national board of housing building and planning",
    ),
]


def tokenize_column(
    source: Field,
    target: Field,
    root_directory: str,
    na_action: str = "ignore",
) -> int:

    load_data, save_data, get_path = get_file_operations()

    dataframe = load_data(root_directory=root_directory, usecols=None)

    if source.value not in dataframe.columns:
        if na_action == "ignore":
            return 0
        raise KeyError(
            f"Source column '{source.value}' not found in {get_path(root_directory).name}"
        )

    if source.value in dataframe.columns and not dataframe[source.value].dropna().empty:
        dataframe[target.value] = _tokenize(dataframe[source.value])

    non_null_count = int(dataframe[target.value].notna().sum())

    save_data(df=dataframe, root_directory=root_directory)

    return non_null_count


def _tokenize(text: pd.Series) -> pd.Series:

    # remove [...]
    text = text.map(
        lambda w: pd.NA if w[0] == "[" and w[-1] == "]" else w, na_action="ignore"
    )

    # -------------------------------------------------------------------------
    # find all URLs in the pandas series

    urls = text.str.findall(_URL_PATTERN).explode().dropna().unique().tolist()

    # Replace URLs with the by "__url{i}__" where i is the index
    # of the URL in the list of unique URLs.
    for i, url in enumerate(urls):
        placeholder = f" . . . url{i} . . . "
        text = text.str.replace(url, placeholder, regex=False)
    # -------------------------------------------------------------------------

    # Normalize unicode
    text = text.map(
        lambda w: unicodedata.normalize("NFKD", w) if isinstance(w, str) else w
    )

    # Replace full-width punctuation with ASCII equivalents
    for full_width, ascii_char in _FULL_WIDTH_TO_ASCII.items():
        text = text.str.replace(full_width, ascii_char)

    # Add spaces around punctuation (e.g., "word.word" -> "word . word")
    text = text.str.replace(r"([a-z])([.,!?;:])", r"\1 \2", regex=True)
    text = text.str.replace(r"([.,!?;:])([a-z])", r"\1 \2", regex=True)

    text = text.str.lower()

    # Remove all HTML tags
    text = text.str.replace("<.*?>", "", regex=True)

    # Standardize "e-mail" to "email" for consistency.
    text = text.str.replace(r"e-mail", r"email", regex=False)

    # Expand contractions (e.g., "don't" -> "do not")
    text = text.apply(lambda x: contractions.fix(x) if isinstance(x, str) else x)

    # Standardize punctuation:
    # Replace curly apostrophes (’) and backticks (`) with straight apostrophes (') for consistency.
    # Replace semicolons (;) with periods (.) to simplify sentence structure.
    # Replace em dashes (—) with hyphens (-) for uniformity.
    text = text.str.replace("’", "'", regex=False)
    text = text.str.replace(";", ".", regex=False)
    text = text.str.replace("`", "'", regex=False)
    text = text.str.replace("—", "-", regex=False)
    text = text.str.replace("-", " ", regex=False)
    text = text.str.replace("&", " and ", regex=False)  # and

    # Tokenize text into individual words:
    # Split each string into tokens (words) using NLTK's word_tokenize.
    # If the value is not a string, it is left unchanged.
    text = text.map(
        lambda w: " ".join(word_tokenize(w)) if isinstance(w, str) else w,
        na_action="ignore",
    )

    # Correction: Standardize URLs and email formatting to preserve entities.
    # Replace "http : //" and "https : //" with "http://" for consistency.
    # Replace "mail : " with "mail:" to standardize email formatting.
    # Replace " @ " with "@" to ensure proper email address formatting.
    text = text.str.replace("http : //", "http://", regex=False)
    text = text.str.replace("https : //", "http://", regex=False)
    text = text.str.replace("mail : ", "mail:", regex=False)
    text = text.str.replace(" @ ", "@", regex=False)

    # Correction: Add spaces around slashes between words for clarity.
    # (e.g., "setting/participants/intervention" becomes "setting / participants / intervention").
    text = text.str.replace(r"([a-z])/([a-z])", r"\1 / \2", regex=True)

    # Correction: Standardize punctuation for edge cases not handled by word_tokenize.
    # Add a space before an opening parenthesis if it follows a period.
    text = text.str.replace(" .(", " . (", regex=False)

    # Correction: Ensure proper spacing around single letters followed by a period
    # (e.g., " A. " becomes " A . ").
    text = text.str.replace(r"\s([a-z])\.\s", r" \1 . ", regex=True)

    text = text.str.replace(":. ", ": . ", regex=False)

    # Correction: Add a space after an apostrophe if followed by alphanumeric
    # characters or a period. (e.g., " 's " becomes " ' s ").
    text = text.str.replace(r" '([a-z0-9\.]+)\s", r" ' \1 ", regex=True)

    # Correction: Add a space after an apostrophe if followed by numeric characters.
    # (e.g., " '123" becomes " ' 123").
    text = text.str.replace(r" '(\d+)", r" ' \1", regex=True)

    # Correction: Add spaces around single-letter acronyms separated by periods.
    # (e.g., " A.B " becomes " A . B ").
    text = text.str.replace(r"\s([a-z])\.([a-z])\s", r" \1 . \2 ", regex=True)

    # Correction: Add spaces around tokens separated by periods.
    # (e.g., "xxx.yyy " becomes " xxx . yyy ").
    text = text.str.replace(r"\s([a-z]+)\.([a-z]+)\s", r" \1 . \2 ", regex=True)

    # Correction: Add spaces around a text separated by a two points.
    # (e.g., "xxx:yyy " becomes "xxx : yyy ").
    text = text.str.replace(r"([a-z]+):([a-z]+)", r"\1 : \2", regex=True)

    # Correction: Add spaces around a text separated by a comma.
    # (e.g., "xxx, " becomes "xxx , ").
    text = text.str.replace(r" ([a-z]+), ", r" \1 , ", regex=True)

    # Correction: Add spaces around a text separated by a comma.
    # (e.g., "xxx,yyy " becomes "xxx , yyy ").
    text = text.str.replace(r" ([a-z]+),([a-z]+) ", r" \1 , \2 ", regex=True)

    # Correction: Add spaces around a text separated by a point.
    # (e.g., "xxx. yyy " becomes "xxx . yyy ").
    text = text.str.replace(r"([a-z]+)\. ([a-z]+)", r"\1 . \2", regex=True)

    # Correction: Add spaces around a text finished with two points.
    # (e.g., "xxx.. " becomes "xxx . . ").
    text = text.str.replace(r"([a-z]+)\.\. ", r"\1 . . ", regex=True)

    # Correction: Add spaces around a text finished with thee points.
    # (e.g., "xxx... " becomes "xxx . . . ").
    text = text.str.replace(r"([a-z]+)\.\.\. ", r"\1 . . . ", regex=True)

    # Correction: add spaces around three-letter acronyms separated by periods.
    # (e.g., " A.B.C " becomes " A . B . C ").
    text = text.str.replace(
        r"\s([a-z])\.([a-z])\.([a-z])\s", r" \1 . \2 . \3 ", regex=True
    )

    # Correction: Add spaces around four-letter acronyms separated by periods.
    # (e.g., " A.B.C.D " becomes " A . B . C . D ").
    text = text.str.replace(
        r"\s([a-z])\.([a-z])\.([a-z])\.([a-z])\s",
        r" \1 . \2 . \3 . \4 ",
        regex=True,
    )

    # Correction: Add spaces around two-letter acronyms followed by a period.
    # (e.g., " AB. " becomes " AB . ").
    text = text.str.replace(r"\s([a-z][a-z])\.\s", r" \1 . ", regex=True)

    # Correction: Add a space before a closing parenthesis if preceded by a word and a period.
    # (e.g., " AB.) " becomes " AB . ) ").
    text = text.str.replace(r"\s([a-z]+)\.\s\)", r" \1 . )", regex=True)

    # Correction: Replace ellipses (" .. ") with spaced periods (" . . ") for consistency.
    text = text.str.replace(r"\s\.\.\s", r" . . ", regex=True)

    # Correction: Add a space before an equals sign if followed by numeric characters.
    # (e.g., " =123" becomes " = 123").
    text = text.str.replace(r"\s=(\d+)", r" = \1", regex=True)

    # Correction: Add a space around a four-digit year followed by a period.
    # (e.g., " 2020. " becomes " 2020 . ").
    text = text.str.replace(r" (\d{4})\. ", r" \1 . ", regex=True)

    # Correction: Add spacing around "et al." for consistency.
    # (e.g., "et al." becomes "et al .").
    text = text.str.replace(" et al. ", " et al . ", regex=False)

    # Correction: Add spacing around "ltd." for consistency.
    # (e.g., "ltd." becomes "ltd .").
    text = text.str.replace(" ltd. ", " ltd . ", regex=False)

    # Correction: Add spacing around "inc." for consistency.
    # (e.g., "inc." becomes "inc .").
    text = text.str.replace(" inc. ", " inc . ", regex=False)

    # Correction: Remove possessive "'s" when surrounded by underscores
    # for consistency. (e.g., "_'s_" becomes "_").
    text = text.str.replace("_'s_", "_", regex=False)
    text = text.str.replace(" 's ", " ", regex=False)

    # Correction: Replace double quotes (" '' " and " `` ") with single
    # quotes (" ' ' ") for consistency.
    text = text.str.replace(" '' ", " ' ' ", regex=False)
    text = text.str.replace(" `` ", " ' ' ", regex=False)

    # Correction: Replace ellipses (" .. ") with spaced periods (" . . ")
    # for uniformity.
    text = text.str.replace(" .. ", " . . ", regex=False)

    # Correction: Replace trailing ellipses (" ..") at the end of a sentence
    # with spaced periods (" . .").
    text = text.str.replace(r" \.\.$", " . .", regex=True)

    # Correction: Add spacing between the point and the letter in " .LETTER"
    text = text.str.replace(r" \.([a-z])", r" . \1", regex=True)

    # Correction: Replace "trial registration :" with "trial_registration:"
    # to standardize the format.
    text = text.str.replace(
        " trial registration : ", " trial_registration :", regex=True
    )

    # Correction: energy units
    text = text.str.replace(" g / kwh ", " g/kwh ", regex=False)
    text = text.str.replace("/mw h ", "/mwh ", regex=False)
    text = text.str.replace("/kw h ", "/kwh ", regex=False)
    text = text.str.replace("/kw hr ", "/kwh ", regex=False)
    text = text.str.replace(" us cents/kwh ", " uscents/kwh ", regex=False)

    # Remove all non-ASCII characters:
    # Normalize text to NFKD form, encode to ASCII (ignoring errors), and decode back to UTF-8.
    text = text.str.normalize("NFKD")
    text = text.str.encode("ascii", errors="ignore")
    text = text.str.decode("utf-8")

    # Remove multiple spaces and trim leading/trailing whitespace.
    text = text.str.replace(r"\s+", r" ", regex=True)
    text = text.str.strip()

    # URLs
    urls = [url.replace("_", "-") for url in urls]

    for i, url in enumerate(urls):

        #
        if url.endswith(")."):
            url = url[:-2] + " ) ."
            urls[i] = url
            continue

        if url.endswith("),"):
            url = url[:-2] + " ) ,"
            urls[i] = url
            continue

        if url.endswith(","):
            url = url[:-1] + " ,"
            urls[i] = url
            continue

        if url.endswith("."):
            url = url[:-1] + " ."
            urls[i] = url
            continue

        if url.endswith(")"):
            url = url[:-1] + " )"
            urls[i] = url
            continue

    # Restore URLs
    for i, url in enumerate(urls):
        placeholder = f". . . url{i} . . ."
        text = text.str.replace(placeholder, url, regex=False)

    text = text.str.replace(" :http", " : http", regex=False)

    for old, new in _NOUN_PHRASE_CORRECTIONS:
        text = text.str.replace(old, new, regex=False)

    british_to_american = load_builtin_mapping("british_to_american.json")
    for british, american in british_to_american.items():
        if isinstance(american, str):
            text = text.str.replace(f" {british} ", f" {american} ", regex=False)

    return text
