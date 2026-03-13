import pandas as pd  # type: ignore


def process_asjc_raw():

    df = pd.read_csv("tm2p/_intern/packag_data/csv/data/asjc_raw.csv", sep=";")

    ajsc = df.columns[3:]

    records = []
    for _, row in df.iterrows():

        journal_asjc = []
        for i, col in enumerate(ajsc):
            if not pd.isna(row[col]):
                journal_asjc.append(row[col].strip())

        if journal_asjc and (not pd.isna(row["ISSN"]) or not pd.isna(row["EISSN"])):
            journal_asjc = "; ".join(journal_asjc)
            record = {
                "ISSN": row["ISSN"],
                "ISSNE": row["EISSN"],
                "ASJC": journal_asjc,
            }
            records.append(record)

    df_asjc = pd.DataFrame(records)
    df_asjc.to_csv("tm2p/_intern/packag_data/csv/data/asjc.csv", index=False)


process_asjc_raw()
