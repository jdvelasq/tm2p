# CODE_REVIEW: 2026-01-26


from tm2p._intern import Params

from ...step import Step


def build_concept_steps(params: Params) -> list[Step]:

    from .s01_merge_keywords_and_phrases import s01_merge_keywords_and_phrases
    from .s02_create_words import s02_create_words
    from .s03_create_descriptor_thesaurus import s03_create_descriptor_thesaurus
    from .s04_update_builtin_noun_phrases import s04_update_builtin_noun_phrases

    common_kwargs = {"root_directory": params.root_directory}

    return [
        Step(
            name="Merging KW and NP into CONCEPT",
            function=s01_merge_keywords_and_phrases,
            kwargs=common_kwargs,
        ),
        Step(
            name="Creating WORD column",
            function=s02_create_words,
            kwargs=common_kwargs,
        ),
        Step(
            name="Creating concept thesaurus",
            function=s03_create_descriptor_thesaurus,
            kwargs=common_kwargs,
        ),
        Step(
            name="Updating built-in NP with concepts",
            function=s04_update_builtin_noun_phrases,
            kwargs=common_kwargs,
            count_message="{count} records updated",
        ),
    ]
