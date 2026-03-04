def _terms_to_cluster_mapping(
    terms_by_dimmension,
    clustering_estimator_or_dict,
):

    if isinstance(clustering_estimator_or_dict, dict):
        #
        # User provide a dictionary with the mapping
        return terms_by_dimmension.copy()

    #
    # Selects first n_cluster components for clustering
    embedding = terms_by_dimmension.iloc[:, : clustering_estimator_or_dict.n_clusters]
    clustering_estimator_or_dict.fit(embedding)

    #
    # Rename the clusters from the most frequent to the less frequent
    communities = {}
    for i in range(clustering_estimator_or_dict.n_clusters):
        communities[i] = []

    for i, label in enumerate(clustering_estimator_or_dict.labels_):
        communities[label].append(i)

    lengths = [(key, len(communities[key])) for key in communities]
    lengths = sorted(lengths, key=lambda x: x[1], reverse=True)
    sorted_labels = [index for index, _ in lengths]

    old_2_new = {old: new for new, old in enumerate(sorted_labels)}
    labels = [old_2_new[label] for label in clustering_estimator_or_dict.labels_]

    mmapping = dict(zip(terms_by_dimmension.index, labels))

    return mmapping
