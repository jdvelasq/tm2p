from pathlib import Path

from tm2p.enum.field import Field

from ._renam_col import renam_col

NAMES_TO_TM2 = {
    "id": Field.RID.value,
    "abstract": Field.ABSTR_RAW.value,
    "authorships.author.display_name": Field.AUTH_FULL_NAME.value,
    "authorships.author.id": Field.AUTHID_RAW.value,
    "authorships.author.orcid": Field.ORCID.value,
    "authorships.countries": Field.CTRY_ISO2.value,
    "authorships.institutions.display_name": Field.ORG_RAW.value,
    "authorships.institutions.id": Field.ORG_ID.value,
    "authorships.is_corresponding": Field.IS_CORRESPOND.value,
    "best_oa_location.license": Field.OA_LICENSE.value,
    "cited_by_count": Field.GCS.value,
    "corresponding_institution_ids": Field.CORRESPOND_ORG_ID.value,
    "display_name": Field.TITLE_RAW.value,
    "doi": Field.DOI.value,
    "funders.display_name": Field.FUND_DET.value,
    "fwci": Field.FWCI.value,
    "ids.pmid": Field.PUBMED.value,
    "is_retracted": Field.IS_RETRACTED.value,
    "language": Field.LANG.value,
    "open_access.is_oa": Field.IS_OA.value,
    "open_access.oa_status": Field.OA.value,
    "primary_location.source.display_name": Field.SRC_RAW.value,
    "primary_location.source.id": Field.SRC_ID.value,
    "primary_location.source.issn_l": Field.ISSN.value,
    "primary_location.source.type": Field.SRC_TYPE.value,
    "primary_topic.display_name": Field.ASJC.value,
    "publication_date": Field.DATE.value,
    "publication_year": Field.YEAR.value,
    "type": Field.DOCTYPE_RAW.value,
}


def s02_renam_openalex_col(root_directory: str) -> int:

    main_file = Path(root_directory) / "ingest" / "process" / "main.csv.zip"
    files_processed = renam_col(main_file, NAMES_TO_TM2)

    return files_processed
