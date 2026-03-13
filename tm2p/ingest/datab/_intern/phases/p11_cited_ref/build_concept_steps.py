# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_concept_steps(params: Params) -> list[Step]:

    from .s01_merge_keywords_and_phrases import s01_merge_keywords_and_phrases
    from .s02_create_concept_thesaurus import s02_create_concept_thesaurus
    from .s03_update_builtin_noun_phrases import s03_update_builtin_noun_phrases

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Merging KW and NP into CONCEPT",
            function=s01_merge_keywords_and_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Creating concept thesaurus",
            function=s02_create_concept_thesaurus,
            kwargs=common_kwargs,
        ),
        Step(
            name="Updating built-in NP with concepts",
            function=s03_update_builtin_noun_phrases,
            kwargs=common_kwargs,
            count_message="{count} records updated",
        ),
    ]
