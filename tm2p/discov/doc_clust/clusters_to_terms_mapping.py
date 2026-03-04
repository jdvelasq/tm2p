"""
Clusters to Terms Mapping
===============================================================================


Smoke tests:
    >>> from sklearn.cluster import KMeans
    >>> kmeans = KMeans(
    ...     n_clusters=4,
    ...     init="k-means++",
    ...     n_init=10,
    ...     max_iter=300,
    ...     tol=0.0001,
    ...     algorithm="lloyd",
    ...     random_state=0,
    ... )
    >>> from tm2p.packages.document_clustering import ClustersToTermsMapping
    >>> mapping = (
    ...     ClustersToTermsMapping()
    ...     #
    ...     # FIELD:
    ...     .with_field("raw_keywords")
    ...     .having_items_in_top(50)
    ...     .having_items_ordered_by("OCC")
    ...     .having_item_occurrences_between(None, None)
    ...     .having_item_citations_between(None, None)
    ...     .having_items_in(None)
    ...     #
    ...     # COUNTERS:
    ...     .using_counters(True)
    ...     #
    ...     # TFIDF:
    ...     .using_binary_item_frequencies(False)
    ...     .using_row_normalization(None)
    ...     .using_idf_reweighting(False)
    ...     .using_idf_weights_smoothing(False)
    ...     .using_sublinear_tf_scaling(False)
    ...     #
    ...     # CLUSTERING:
    ...     .using_clustering_algorithm_or_dict(kmeans)
    ...     #
    ...     # DATABASE:
    ...     .where_root_directory("tests/fintech/")
    ...     .where_database("main")
    ...     .where_record_years_range(None, None)
    ...     .where_record_citations_range(None, None)
    ...     .where_records_match(None)
    ...     #
    ...     .run()
    ... )
    >>> import pprint
    >>> pprint.pprint(mapping)
    {0: ['FINANCIAL_SERVICES 05:0746',
         'BUSINESS_MODELS 03:1335',
         'FINANCIAL_INSTITUTION 03:0488',
         'FINANCIAL_TECHNOLOGY 03:0461',
         'BANKING 03:0370',
         'TECHNOLOGY 02:0310',
         'REGTECH 02:0266',
         'CHINA 02:0150'],
     1: ['SUSTAINABILITY 03:0227',
         'SUSTAINABLE_DEVELOPMENT 03:0227',
         'LITERATURE_REVIEW 02:0560',
         'FINANCIAL_SYSTEM 02:0385',
         'DIGITIZATION 02:0319'],
     2: ['FINANCE 11:1950',
         'INNOVATION 08:0990',
         'FINANCIAL_SERVICE 04:1036',
         'COMMERCE 03:0846',
         'SURVEYS 03:0484',
         'FINANCIAL_SERVICES_INDUSTRIES 02:0696',
         'DIGITAL_TECHNOLOGIES 02:0494',
         'PERCEIVED_USEFULNESS 02:0346',
         'CYBER_SECURITY 02:0342',
         'CASE_STUDY 02:0340',
         'DESIGN_METHODOLOGY_APPROACH 02:0329',
         'SALES 02:0329',
         'ARTIFICIAL_INTELLIGENCE 02:0327',
         'FINANCIAL_INDUSTRY 02:0323',
         'SECURITY_AND_PRIVACY 02:0323',
         'ROBOTS 02:0289',
         'TECHNOLOGY_ACCEPTANCE_MODEL 02:0280',
         'DEVELOPING_COUNTRIES 02:0248',
         'INFORMATION_SYSTEMS 02:0235',
         'THEORETICAL_FRAMEWORK 02:0206',
         'MOBILE_TELECOMMUNICATION_SYSTEMS 02:0186',
         'GLOBAL_SYSTEM_FOR_MOBILE_COMMUNICATIONS 02:0184',
         'MOBILE_PAYMENT 02:0184',
         'CONTENT_ANALYSIS 02:0181',
         'DIGITALIZATION 02:0181',
         'POPULAR_PRESS 02:0181',
         'CUSTOMER_EXPERIENCE 01:0576'],
     3: ['FINTECH 32:5393',
         'BLOCKCHAIN 03:0881',
         'FINANCIAL_INCLUSION 03:0590',
         'CROWDFUNDING 03:0335',
         'MARKETPLACE_LENDING 03:0317',
         'ELECTRONIC_MONEY 03:0305',
         'LENDINGCLUB 02:0253',
         'PEER_TO_PEER_LENDING 02:0253',
         'SHADOW_BANKING 02:0253',
         'P2P_LENDING 02:0161']}



"""

from tm2p._intern import ParamsMixin
from tm2p.discov.doc_clust.term_occurrence_by_cluster import TermOccurrenceByCluster


class ClustersToTermsMapping(
    ParamsMixin,
):
    """:meta private:"""

    def run(self):

        contingency_table = (
            TermOccurrenceByCluster().update(**self.params.__dict__).run()
        )

        themes = contingency_table.idxmax(axis=1)

        mapping = {}
        for word, theme in zip(themes.index, themes):
            if theme not in mapping:
                mapping[theme] = []
            mapping[theme].append(word)

        return mapping
