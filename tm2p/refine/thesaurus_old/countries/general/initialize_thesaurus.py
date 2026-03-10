"""
Initialize Thesaurus
===============================================================================


Smoke tests:
    >>> from tm2p.refine.thesaurus_old.countries import InitializeThesaurus
    >>> (
    ...     InitializeThesaurus()
    ...     .where_root_directory("tests/scopus/")
    ... ).run()


    >>> from tm2p.refine.thesaurus_old.countries import PrintHeader
    >>> (
    ...     PrintHeader()
    ...     .using_colored_output(False)
    ...     .where_root_directory("tests/scopus/")
    ... ).run()
    Australia
      Centre for Law, Markets & Regulation, UNSW Australia, Australia; Charles ...
    Belgium
      Brussels, Belgium
    Brunei Darussalam
      Universiti Brunei Darussalam, School of Business and Economics, Jln Tungk...
    China
      Cheung Kong Graduate School of Business, and Institute of Internet Financ...
    Denmark
      Copenhagen Business School, Department of IT Management, Howitzvej 60, Fr...
    France
      SKEMA Business School, Lille, France; University of Lille Nord de France,...
    Germany
      CESifo, Poschingerstr. 5, Munich, 81679, Germany; Chair of e-Finance, Goe...
    Ghana
      University of the Free State and University of Ghana Business School, Uni...
    <BLANKLINE>


"""

import sys
from importlib.resources import files

from colorama import Fore

from tm2p._intern import ParamsMixin
from tm2p.refine.thesaurus_old._intern import ThesaurusMixin
from tm2p.refine.thesaurus_old._intern.load_thesaurus_as_mapping import (
    internal__load_thesaurus_as_mapping,
)


class InitializeThesaurus(
    ParamsMixin,
    ThesaurusMixin,
):
    """:meta private:"""

    #
    # NOTIFICATIONS:
    # -------------------------------------------------------------------------
    def internal__notify_process_start(self):

        if not self.params.quiet:

            field = self.params.source_field

            file_path = str(self.thesaurus_path)
            if len(file_path) > 72:
                file_path = "..." + file_path[-68:]

            if self.params.colored_stderr:
                filename = str(file_path).rsplit("/", maxsplit=1)[1]
                file_path = file_path.replace(filename, f"{Fore.RESET}{filename}")
                file_path = Fore.LIGHTBLACK_EX + file_path

            sys.stderr.write(f"INFO: Initializing thesaurus from '{field}' field...\n")
            sys.stderr.write(f"  Initializing {file_path}\n")
            sys.stderr.flush()

    # -------------------------------------------------------------------------
    def internal__notify_process_end(self):

        if not self.params.quiet:

            sys.stderr.write(f"  {len(self.data_frame)} keys found\n")
            sys.stderr.write("  Initialization process completed successfully\n")
            sys.stderr.flush()

    #
    # ALGORITHM:
    # -------------------------------------------------------------------------
    def internal__extract_country_from_affiliation(self):

        replacements = [
            ("Bosnia and Herz.", "Bosnia and Herzegovina"),
            ("Brasil", "Brazil"),
            ("Czech Republic", "Czechia"),
            ("Espana", "Spain"),
            ("Macao", "China"),
            ("Macau", "China"),
            ("N. Cyprus", "Cyprus"),
            ("Peoples R China", "China"),
            ("Rusia", "Russia"),
            ("Russian Federation", "Russia"),
            ("Syrian Arab Republic", "Syria"),
            ("United States of America", "United States"),
            ("USA", "United States"),
            ("Türkiye", "Turkey"),
            ("Viet-Nam", "Vietnam"),
            ("Viet Nam", "Vietnam"),
            ("Perú", "Peru"),
        ]

        # extracts the country as the last position of the string
        self.data_frame["key"] = (
            self.data_frame["key"].str.split(",").str[-1].str.strip()
        )

        # normalizes country names
        for pat, repl in replacements:
            self.data_frame["key"] = self.data_frame["key"].str.replace(
                pat, repl, regex=False
            )

        # loads country valid names
        file_path = files("tm2p.package_data.thesaurus.geography").joinpath(
            "country_to_alpha3.the.txt"
        )
        file_path = str(file_path)
        mapping = internal__load_thesaurus_as_mapping(file_path)
        valid_names = list(mapping.keys())

        # checks the data frame
        self.data_frame["key"] = self.data_frame["key"].apply(
            lambda x: x if x in valid_names else "[UNKNWON]"
        )

    # -------------------------------------------------------------------------
    def run(self):
        """:meta private:"""

        #
        # SPECIFIC DATA:
        self.with_thesaurus_file("countries.the.txt")
        self.with_source_field("affiliations")

        self._build_user_thesaurus_path()
        self.internal__notify_process_start()
        self.internal__load_filtered_records()
        self.internal__create_thesaurus_data_frame_from_field()
        self.internal__extract_country_from_affiliation()
        self.internal__reduce_keys()
        self.internal__explode_and_group_values_by_key()
        self._sort_data_frame_by_rows_and_key()
        self._write_thesaurus_data_frame_to_disk()
        self.internal__notify_process_end()
        self.internal__print_thesaurus_header_to_stream(n=8, stream=sys.stderr)


# =============================================================================
