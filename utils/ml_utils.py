# utils/ml_utils.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def get_recommendations(user_pref, metadata_list, num_recommendations=5):

    metadata_df = pd.DataFrame(metadata_list)
    # create a new DataFrame with only the product metadata columns
    product_metadata = metadata_df[[
        'product_id', 'interests', 'occasions', 'relationships', 'gender', 'min_age', 'max_age']]

    # combine the metadata columns into a single string for each product
    product_metadata['metadata'] = product_metadata.apply(
        lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    # create a CountVectorizer object to create a sparse matrix of word counts for each product metadata string
    count = CountVectorizer()
    count_matrix = count.fit_transform(product_metadata['metadata'])

    # calculate the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # get the subset of product metadata based on user preferences
    subset_metadata = product_metadata.copy()

    if ('interests' in user_pref) & (subset_metadata.empty == False):
        subset_metadata = subset_metadata[subset_metadata['interests'].apply(
            lambda x: len(set(x).intersection(set(user_pref['interests']))) > 0)]

    if ('occasion' in user_pref) & (subset_metadata.empty == False):
        if isinstance(user_pref['occasion'], str):
            subset_metadata = subset_metadata[[user_pref['occasion'].lower() in [o.lower(
            ) for o in occasions] for occasions in subset_metadata['occasions']]]
        elif isinstance(user_pref['occasion'], list):
            subset_metadata = subset_metadata[[any(o.lower() in [occ.lower(
            ) for occ in occasions] for o in user_pref['occasion']) for occasions in subset_metadata['occasions']]]

    if ('relationship' in user_pref) & (subset_metadata.empty == False):
        if isinstance(user_pref['relationship'], str):
            subset_metadata = subset_metadata[[user_pref['relationship'].lower() in [o.lower(
            ) for o in relationships] for relationships in subset_metadata['relationships']]]
        elif isinstance(user_pref['relationship'], list):
            subset_metadata = subset_metadata[[any(o.lower() in [occ.lower(
            ) for occ in relationships] for o in user_pref['relationship']) for relationships in subset_metadata['relationships']]]

    # get the row indices of the products in the subset
    product_indices = subset_metadata.index.tolist()

    # get the cosine similarity scores for the products in the subset
    similarity_scores = [(i, cosine_sim[i][product_indices].mean())
                         for i in range(cosine_sim.shape[0])]

    # sort the similarity scores in descending order
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)

    # get the indices of the top n most similar products
    top_indices = [i[0] for i in similarity_scores[1:num_recommendations+1]]

    # get the product IDs of the top n most similar products
    top_products = list(product_metadata.iloc[top_indices]['product_id'])

    result_dict = {"productIds": top_products}
    return result_dict
