import re
from typing import List

_AMBIGUOUS_INDICATOR = [
    "institute of",
    "institut de",
    "instituto de",
    "institutt for",
    "center for",
    "centre for",
    "centro de",
    "centro para",
    "laboratory of",
    "lab of",
    "laboratoire de",
    "laboratorio de",
    "school of",
    "école de",
    "escuela de",
    "escola de",
    "graduate school",
    "doctoral school",
]

_CORPORATE_SUFFIX = [
    "ltd",
    "limited",
    "inc",
    "incorporated",
    "corp",
    "corporation",
    "gmbh",
    "s.a.",
    "s.l.",
    "srl",
    "s.r.l.",
    "spa",
    "s.p.a.",
    "bv",
    "b.v.",
    "llc",
    "l.l.c.",
    "ag",
    "plc",
    "co.",
    "company",
]


_DEPARTMENT_INDICATOR = [
    "department of",
    "dept of",
    "dept.",
    "faculty of",
    "school of",
    "college of",
    "division of",
    "unit of",
    "section of",
    "chair of",
    "professorship",
    "lehrstuhl",
    "departamento de",
    "département de",
    "facoltà di",
    "facultad de",
    "dipartimento di",
    "departement",
    "división de",
]

_GOVERNMENT_KEYWORD = [
    "ministry",
    "government",
    "agency",
    "council",
    "commission",
    "authority",
    "department of",
    "bureau",
    "office of",
]


_ORGANIZATION_KEYWORD = [
    "university",
    "universidad",
    "université",
    "universität",
    "università",
    "universiteit",
    "yliopisto",
    "univerza",
    "univerzita",
    "universitas",
    "universiti",
    "universitet",
    "universitāte",
    "rijksuniversiteit",
    "polytechnic",
    "politecnico",
    "politechnika",
    "polytechnique",
    "institute",
    "instituto",
    "institut",
    "institutt",
    "college",
    "school",
    "academy",
    "academia",
    "hospital",
    "clinic",
    "klinik",
    "medical center",
    "medical centre",
    "research center",
    "research centre",
    "national laboratory",
    "foundation",
    "fundación",
    "fondation",
    "stiftung",
]


def _clean_part(part: str) -> str:
    part = part.strip()
    part = re.sub(r"\s*\([^)]*\)\s*$", "", part)
    return part.strip()


def _contains_corporate_suffix(text: str) -> bool:
    if not text or not text.strip():
        return False
    text_lower = text.lower()
    return any(
        re.search(r"\b" + re.escape(suffix) + r"\b", text_lower)
        for suffix in _CORPORATE_SUFFIX
    )


def _contains_government_keyword(text: str) -> bool:
    if not text or not text.strip():
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in _GOVERNMENT_KEYWORD)


def _contains_org_keyword(text: str) -> bool:
    if not text or not text.strip():
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in _ORGANIZATION_KEYWORD)


def _has_multiple_words(text: str) -> bool:
    return len(text.split()) >= 2


def _is_acronym(text: str) -> bool:
    return text.isupper() and len(text) >= 2 and text.isalpha()


def _is_organization(text: str) -> bool:
    if not text or not text.strip():
        return False
    return (
        _contains_org_keyword(text)
        or _contains_corporate_suffix(text)
        or _contains_government_keyword(text)
        or _has_multiple_words(text)
        or _is_acronym(text)
    )


def _remove_duplicate_segments(parts: List[str]) -> List[str]:
    if len(parts) < 2:
        return parts
    result = []
    for i, part in enumerate(parts):
        if i == 0 or part.lower() != parts[i - 1].lower():
            result.append(part)
    return result


def _starts_with_ambiguous_indicator(text: str) -> bool:
    if not text or not text.strip():
        return False
    text_lower = text.lower().strip()
    return any(text_lower.startswith(indicator) for indicator in _AMBIGUOUS_INDICATOR)


def _starts_with_department(text: str) -> bool:
    if not text or not text.strip():
        return False
    text_lower = text.lower().strip()
    return any(text_lower.startswith(indicator) for indicator in _DEPARTMENT_INDICATOR)


def extract_org_name_from_string(affiliation: str) -> str:

    # organizations = load_builtin_word_list("organizations.txt")
    # for org in organizations:
    #     if org.lower() in affiliation.lower():
    #         return org

    parts = [_clean_part(p) for p in affiliation.split(",")]
    parts = [p for p in parts if p]

    if not parts:
        return "[n/a]"

    parts = _remove_duplicate_segments(parts)

    if len(parts) >= 2:
        first = parts[0]
        second = parts[1]

        if _starts_with_ambiguous_indicator(first) and _is_organization(second):
            return second

        if _starts_with_department(first) and _is_organization(second):
            return second

    if len(parts) >= 1:
        first = parts[0]
        if not _starts_with_department(first) and _is_organization(first):
            return first

    if len(parts) >= 2 and _is_organization(parts[1]):
        return parts[1]

    if len(parts) >= 1 and _is_organization(parts[0]):
        return parts[0]

    return "[n/a]"
