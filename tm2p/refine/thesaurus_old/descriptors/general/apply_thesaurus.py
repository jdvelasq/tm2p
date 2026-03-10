# mypy: ignore-errors
"""
Apply Thesaurus
===============================================================================


Smoke tests:
    >>> import sys
    >>> from io import StringIO
    >>> from tm2p.refine.thesaurus_old.descriptors import ApplyThesaurus, InitializeThesaurus

    >>> # Redirecting stderr to avoid messages
    >>> original_stderr = sys.stderr
    >>> sys.stderr = StringIO()

    >>> # Create the thesaurus
    >>> InitializeThesaurus(root_directory="examples/fintech/", quiet=True).run()

    >>> applier = (
    ...     ApplyThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... )
    >>> applier.run()

    >>> # Capture and print stderr output
    >>> output = sys.stderr.getvalue()
    >>> sys.stderr = original_stderr
    >>> print(output)
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : author_keywords_raw
      Target field : author_keywords
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : index_keywords_raw
      Target field : index_keywords
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : raw_keywords
      Target field : keywords
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : raw_document_title_nouns_and_phrases
      Target field : document_title_nouns_and_phrases
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : raw_abstract_nouns_and_phrases
      Target field : abstract_nouns_and_phrases
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : raw_nouns_and_phrases
      Target field : nouns_and_phrases
      Application process completed successfully
    <BLANKLINE>
    Applying user thesaurus to database...
              File : examples/fintech/data/thesaurus/descriptors.the.txt
      Source field : raw_descriptors
      Target field : descriptors
      Application process completed successfully
    <BLANKLINE>
    <BLANKLINE>



"""
from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old.user import ApplyThesaurus as ApplyUserThesaurus

PAIRS = [
    ("author_keywords_raw", "author_keywords"),
    ("index_keywords_raw", "index_keywords"),
    ("raw_keywords", "keywords"),
    ("raw_document_title_nouns_and_phrases", "document_title_nouns_and_phrases"),
    ("raw_abstract_nouns_and_phrases", "abstract_nouns_and_phrases"),
    ("raw_nouns_and_phrases", "nouns_and_phrases"),
    ("raw_descriptors", "descriptors"),
]


class ApplyThesaurus(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        for index, (raw_column, column) in enumerate(PAIRS):

            (
                ApplyUserThesaurus(quiet=self.params.quiet)
                .update(**self.params.__dict__)
                .with_thesaurus_file("concepts.the.txt")
                .with_source_field(raw_column)
                .with_other_field(column)
                .where_root_directory(self.params.root_directory)
                .run()
            )
