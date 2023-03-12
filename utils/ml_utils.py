# utils/ml_utils.py

import math
from numpy import hstack
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# TODO Handle any values and score !!!!!!!!!!!!!!!!!!!!!!!!!!


def get_recommendations(user_pref, metadata_list, num_recommendations=12):

    if len(metadata_list) == 0:
        return []

    metadata_df = pd.DataFrame(metadata_list)
    # create a new DataFrame with only the product metadata columns
    product_metadata = metadata_df[[
        'product_id', 'interests', 'occasions', 'relationships', 'gender', 'min_age', 'max_age', 'no_of_reviews', 'rating', 'price']]

    # generate a score based on rating, reviews, and price
    product_metadata['score'] = product_metadata['rating'] * np.log10(
        product_metadata['no_of_reviews'] + 1) / np.log10(product_metadata['price'] + 1)

    product_metadata = product_metadata.drop(
        ['rating', 'no_of_reviews'], axis=1)

    # combine the metadata columns into a single string for each product
    product_metadata['metadata'] = product_metadata.apply(
        lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    # create a CountVectorizer object to create a sparse matrix of word counts for each product metadata string
    count = CountVectorizer()
    count_matrix = count.fit_transform(product_metadata['metadata'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # get the subset of product metadata based on user preferences
    subset_metadata = product_metadata.copy()
    other_subset_metadata = subset_metadata

    # if ('interests' in user_pref) and (subset_metadata.empty == False) and (user_pref['interests'] != 'any') and ('any' not in subset_metadata['interests']):
    #     subset_metadata = subset_metadata[subset_metadata['interests'].apply(
    #         lambda x: len(set(x).intersection(set(user_pref['interests']))) > 0)]

    if ('interests' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['interests']):
        subset_metadata = subset_metadata[subset_metadata['interests'].apply(
            lambda x:  any(
                interest in x for interest in user_pref['interests'])
        )]
        other_subset_metadata = other_subset_metadata[other_subset_metadata['interests'].apply(
            lambda x: 'any' in x
        )]

    if ('occasion' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['occasion']):
        subset_metadata = subset_metadata[subset_metadata['occasions'].apply(
            lambda x: 'any' in x or any(
                occasion in x for occasion in user_pref['occasion'])
        )]
        other_subset_metadata = other_subset_metadata[other_subset_metadata['occasions'].apply(
            lambda x: 'any' in x or any(
                occasion in x for occasion in user_pref['occasion'])
        )]

    if ('relationship' in user_pref) and (subset_metadata.empty == False) and user_pref['relationship'].lower() != 'any':
        subset_metadata = subset_metadata[[user_pref['relationship'].lower() in [r.lower(
        ) for r in relationships] or 'any' in relationships for relationships in subset_metadata['relationships']]]
        other_subset_metadata = other_subset_metadata[[user_pref['relationship'].lower() in [r.lower(
        ) for r in relationships] or 'any' in [r.lower() for r in relationships] for relationships in other_subset_metadata['relationships']]]

    # get the row indices of the products in the subset
    product_indices = subset_metadata.index.tolist()
    other_product_indices = other_subset_metadata.index.tolist()

    # get the cosine similarity scores for the products in the subset
    similarity_scores = [(i, cosine_sim[i][product_indices].mean())
                         for i in range(cosine_sim.shape[0])]
    other_similarity_scores = [(i, cosine_sim[i][other_product_indices].mean())
                               for i in range(cosine_sim.shape[0])]

    # sort the similarity scores in descending order
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)

    other_similarity_scores = sorted(
        other_similarity_scores, key=lambda x: x[1], reverse=True)

    # use the generated score along with similarity to rank the products
    ranked_scores = []
    for i in range(len(product_metadata)):
        final_score = 0
        if i in product_indices:
            similarity_weight = 0.8
            product_weight = 0.2
            final_score = similarity_weight * \
                similarity_scores[i][1] + product_weight * \
                product_metadata.loc[i, 'score']
            ranked_scores.append((i, final_score))
        else:
            ranked_scores.append((i, 0))

    ranked_scores = sorted(ranked_scores, key=lambda x: x[1], reverse=True)

    # use the generated score along with similarity to rank the products
    other_ranked_scores = []
    for i in range(len(product_metadata)):
        final_score = 0
        if i in other_product_indices:
            similarity_weight = 0.8
            product_weight = 0.2
            final_score = similarity_weight * \
                other_similarity_scores[i][1] + product_weight * \
                product_metadata.loc[i, 'score']
            other_ranked_scores.append((i, final_score))
        else:
            other_ranked_scores.append((i, 0))

    other_ranked_scores = sorted(
        other_ranked_scores, key=lambda x: x[1], reverse=True)

    # get the indices of the top n most similar products
    num_recommendations = min(num_recommendations, len(product_indices))
    top_indices = [
        i[0] for i in ranked_scores[:num_recommendations] if not math.isnan(i[1])]

    # get the indices of the top n most other similar products
    other_num_recommendations = min(
        num_recommendations, len(other_product_indices))
    other_top_indices = [
        i[0] for i in other_ranked_scores[:other_num_recommendations] if not math.isnan(i[1])]

    # get the product IDs of the top n most similar products
    productIds = list(product_metadata.iloc[top_indices]['product_id'])
    otherproductIds = list(
        product_metadata.iloc[other_top_indices]['product_id'])

    # get the product metadata of the top n most similar products
    top_products_metadata = product_metadata.iloc[top_indices]
    # get the product metadata of the top n most similar products
    other_top_products_metadata = product_metadata.iloc[other_top_indices]

    # create a dictionary with the product IDs as keys and the product metadata as values
    top_products_dict = {}
    for i in range(len(top_products_metadata)):
        product_id = int(top_products_metadata.iloc[i]['product_id'])
        product_data = top_products_metadata.iloc[i].to_dict()
        data = {
            'interests': product_data.get('interests', []),
            'gender': product_data.get('gender', []),
            'relationships': product_data.get('relationships', []),
            'occasions': product_data.get('occasions', []),
        }
        top_products_dict[product_id] = data

    # create a dictionary with the product IDs as keys and the product metadata as values
    other_top_products_dict = {}
    for i in range(len(other_top_products_metadata)):
        product_id = int(other_top_products_metadata.iloc[i]['product_id'])
        product_data = other_top_products_metadata.iloc[i].to_dict()
        data = {
            'interests': product_data.get('interests', []),
            'gender': product_data.get('gender', []),
            'relationships': product_data.get('relationships', []),
            'occasions': product_data.get('occasions', []),
        }
        other_top_products_dict[product_id] = data

    result_dict = {"productIds": productIds, "products": top_products_dict,
                   "otherProductIds": otherproductIds, "otherProducts": other_top_products_dict}

    return result_dict
