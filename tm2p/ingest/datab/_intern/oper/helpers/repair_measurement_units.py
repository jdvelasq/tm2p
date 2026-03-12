import pandas as pd  # type: ignore

UNITS = [
    "cad",
    "capex",
    "cent usd",
    "cent",
    "cents",
    "cny",
    "ct",
    "day",
    "dkk",
    "dollars",
    "e",
    "eq.",
    "eq",
    "eur",
    "euro",
    "gwh",
    "h",
    "hr",
    "irr",
    "kg",
    "kw h",
    "kw_hr",
    "kw",
    "kwel",
    "kwh",
    "kwh",
    "kwhr",
    "l",
    "level",
    "m",
    "month",
    "mw",
    "mwh",
    "mwwp",
    "nt",
    "omr",
    "omr",
    "rmb",
    "s",
    "t",
    "ton",
    "tons",
    "twh",
    "unit",
    "us_cents",
    "uscents",
    "usd",
    "year",
    "yr",
    "yuan",
]


def repair_measurement_units(text: str) -> str:
    if pd.isna(text):
        return ""
    text = str(text)
    for unit in UNITS:
        text = text.replace(
            f" {unit.upper().replace(' ', '_')}/",
            f" {unit.lower().replace(' ', '_')}/",
        )
        text = text.replace(
            f" {unit.upper().replace(' ', '_')}_/",
            f" {unit.lower().replace(' ', '_')}/",
        )
        text = text.replace(
            f"/{unit.upper().replace(' ', '_')} ",
            f"/{unit.lower().replace(' ', '_')} ",
        )
        text = text.replace(
            f"/_{unit.upper().replace(' ', '_')} ",
            f"/{unit.lower().replace(' ', '_')} ",
        )
    return text
