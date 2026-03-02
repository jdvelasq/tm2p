from tm2p import Field


def _get_existent_columns(records, candiate_columns):
    columns_to_report = []
    for criterion in candiate_columns:
        if criterion in records.columns:
            columns_to_report.append(criterion)
    return columns_to_report


def _filter_columns(records, selected_columns):
    records = records[selected_columns]
    return records


def _rename_columns(records, names_mapping):
    records = records.rename(columns=names_mapping)
    return records


def _build_dicts(records):
    return records.to_dict(orient="records")


def records_to_dicts(dataframe):

    names_mapping = {
        Field.RNO.value: "UT",
        Field.RID.value: "AR",
        Field.TITLE_RAW.value: "TI",
        Field.AUTH_NORM.value: "AU",
        Field.GCS.value: "TC",
        Field.SRC_ISO4_NORM.value: "SO",
        Field.YEAR.value: "PY",
        Field.ABSTR_UPPER.value: "AB",
        Field.AUTHKW_RAW.value: "DE",
        Field.IDXKW_RAW.value: "ID",
    }

    candiate_columns = names_mapping.keys()

    # dataframe = dataframe.copy()

    columns = _get_existent_columns(dataframe, candiate_columns)
    filtered_df = _filter_columns(dataframe, columns)
    renamed_df = _rename_columns(filtered_df, names_mapping)
    dicts = _build_dicts(renamed_df)

    return dicts
