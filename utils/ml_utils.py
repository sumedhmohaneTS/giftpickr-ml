# utils/ml_utils.py

import math
from numpy import hstack
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler

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
    other_interest_subset_metadata = pd.DataFrame()
    is_interest_any = 'any' in user_pref['interests']

    if not is_interest_any:
        other_interest_subset_metadata = subset_metadata

    # if ('interests' in user_pref) and (subset_metadata.empty == False) and (user_pref['interests'] != 'any') and ('any' not in subset_metadata['interests']):
    #     subset_metadata = subset_metadata[subset_metadata['interests'].apply(
    #         lambda x: len(set(x).intersection(set(user_pref['interests']))) > 0)]

    if ('interests' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['interests']):
        subset_metadata = subset_metadata[subset_metadata['interests'].apply(
            lambda x:  any(
                interest in x for interest in user_pref['interests'])
        )]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[other_interest_subset_metadata['interests'].apply(
                lambda x: 'any' in x
            )]

    if ('occasion' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['occasion']):
        subset_metadata = subset_metadata[subset_metadata['occasions'].apply(
            lambda x: 'any' in x or any(
                occasion in x for occasion in user_pref['occasion'])
        )]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[other_interest_subset_metadata['occasions'].apply(
                lambda x: 'any' in x or any(
                    occasion in x for occasion in user_pref['occasion'])
            )]

    if ('relationship' in user_pref) and (subset_metadata.empty == False) and user_pref['relationship'].lower() != 'any':
        subset_metadata = subset_metadata[[user_pref['relationship'].lower() in [r.lower(
        ) for r in relationships] or 'any' in relationships for relationships in subset_metadata['relationships']]]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[[user_pref['relationship'].lower() in [r.lower(
            ) for r in relationships] or 'any' in [r.lower() for r in relationships] for relationships in other_interest_subset_metadata['relationships']]]

    # get the row indices of the products in the subset
    product_indices = subset_metadata.index.tolist()
    other_product_indices = other_interest_subset_metadata.index.tolist()

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


def get_recommendationsV2(user_pref, metadata_list, num_recommendations=240):

    if len(metadata_list) == 0:
        return []

    metadata_df = pd.DataFrame(metadata_list)
    # create a new DataFrame with only the product metadata columns
    product_metadata = metadata_df[[
        'product_id', 'interests', 'occasions', 'relationships', 'gender', 'min_age', 'max_age', 'no_of_reviews', 'rating', 'price']]

    # generate a score based on rating, reviews, and price
    median_price = np.median(product_metadata['price'])
    mad = np.median(np.abs(product_metadata['price'] - median_price))
    scaling_factor = 1.4826  # scaling factor for MAD to approximate standard deviation
    score = product_metadata['rating'] * np.log10(
        product_metadata['no_of_reviews'] + 1) * (1 / (1 + scaling_factor * abs(product_metadata['price'] - median_price) / mad))

    # normalize the score between 0 and 1
    scaler = MinMaxScaler()
    score_norm = scaler.fit_transform(score.values.reshape(-1, 1))

    # update the product_metadata dataframe with the normalized score
    product_metadata['score'] = score_norm

    product_metadata = product_metadata.drop(
        ['rating', 'no_of_reviews'], axis=1)

    # combine the metadata columns into a single string for each product
    product_metadata['metadata'] = product_metadata.apply(
        lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    # combine the gender, interest, occasion, and relationship columns into a single string for each product
    genders = user_pref['gender'] if 'any' not in user_pref['gender'] else [
        'any']

    interests = user_pref['interests'] if 'any' not in user_pref['interests'] else [
        'any']
    occasion = user_pref['occasion'] if 'any' not in user_pref['occasion'] else [
        'any']
    relationship = [user_pref['relationship']] if 'any' != user_pref['relationship'] else [
        'any']

    genders_col = product_metadata['gender'].apply(
        lambda x:
        'any' if 'any' in genders
        else
        '\', \''.join(sorted(str(val) for val in genders)) + ' a' if 'any' in x
        else '\', \''.join(sorted([str(val) for val in x if str(val) in genders])))

    interests_col = product_metadata['interests'].apply(
        lambda x:
        'any' if 'any' in interests
        else
        '\', \''.join(sorted(str(val) for val in interests)) + ' a' if 'any' in x
        else '\', \''.join(sorted([str(val) for val in x if str(val) in interests])))

    occasions_col = product_metadata['occasions'].apply(
        lambda x:
        'any' if 'any' in occasion
        else
        # '\', \''.join(sorted(str(val) for val in occasion)) + ' a' if 'any' in x
        # else
        '\', \''.join(sorted([str(val) for val in x if str(val) in occasion])))

    relationships_col = product_metadata['relationships'].apply(
        lambda x:
        'any' if 'any' in relationship
        else
        # '\', \''.join(sorted(str(val) for val in relationship)) + ' a' if 'any' in x
        # else
        '\', \''.join(sorted([str(val) for val in x if str(val) in relationship])))

    product_metadata['genderCol'] = genders_col
    product_metadata['interestCol'] = interests_col
    product_metadata['occasionCol'] = occasions_col
    product_metadata['relationshipCol'] = relationships_col
    product_metadata['gior'] = '[\''+product_metadata['genderCol'] + '\'] [\''+product_metadata['interestCol'] + '\'] [\'' + \
        product_metadata['occasionCol'] + '\'] [\'' + \
        product_metadata['relationshipCol'] + '\']'

    # get the subset of product metadata based on user preferences
    subset_metadata = product_metadata.copy()
    other_interest_subset_metadata = pd.DataFrame()
    is_interest_any = 'any' in user_pref['interests']

    if not is_interest_any:
        other_interest_subset_metadata = subset_metadata

    if ('interests' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['interests']):
        subset_metadata = subset_metadata[subset_metadata['interests'].apply(
            lambda x:  any(
                interest in x for interest in user_pref['interests'])
        )]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[other_interest_subset_metadata['interests'].apply(
                lambda x: 'any' in x
            )]

    if ('occasion' in user_pref) & (subset_metadata.empty == False) and ('any' not in user_pref['occasion']):
        subset_metadata = subset_metadata[subset_metadata['occasions'].apply(
            lambda x: 'any' in x or any(
                occasion in x for occasion in user_pref['occasion'])
        )]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[other_interest_subset_metadata['occasions'].apply(
                lambda x: 'any' in x or any(
                    occasion in x for occasion in user_pref['occasion'])
            )]

    if ('relationship' in user_pref) and (subset_metadata.empty == False) and user_pref['relationship'].lower() != 'any':
        subset_metadata = subset_metadata[[user_pref['relationship'].lower() in [r.lower(
        ) for r in relationships] or 'any' in relationships for relationships in subset_metadata['relationships']]]
        if not other_interest_subset_metadata.empty:
            other_interest_subset_metadata = other_interest_subset_metadata[[user_pref['relationship'].lower() in [r.lower(
            ) for r in relationships] or 'any' in [r.lower() for r in relationships] for relationships in other_interest_subset_metadata['relationships']]]

    # get the row indices of the products in the subset
    product_indices = subset_metadata.index.tolist()
    other_product_indices = other_interest_subset_metadata.index.tolist()

    # create a CountVectorizer object to create a sparse matrix of word counts for each product metadata string
    user_pref['interests'].sort()
    user_pref['occasion'].sort()
    user_pref_gior = ''+str(user_pref['gender']) + ' ' + \
        ''+str(user_pref['interests']) + ' ' + \
        str(user_pref['occasion']) + \
        ' [\'' + user_pref['relationship'] + '\']'

    count = CountVectorizer()

    count_matrix = count.fit_transform(product_metadata['gior'])
    user_pref_matrix = count.transform([user_pref_gior])

    # concatenate the count_matrix and ior_matrix into a single sparse matrix

    cosine_sim = cosine_similarity(user_pref_matrix, count_matrix)

    # get the cosine similarity scores for the products in the subset
    allProducts = product_metadata.index.tolist()
    similarity_scores = [(i, cosine_sim[0][i]) for i in allProducts]

    # use the generated score along with similarity to rank the products
    ranked_scores = []

    temp = []
    for i in range(len(product_metadata)):
        final_score = 0
        results = []
        if i in product_indices:
            similarity_weight = 0.7
            product_weight = 0.3
            final_score = similarity_weight * \
                similarity_scores[i][1] + product_weight * \
                product_metadata.loc[i, 'score']
            ranked_scores.append((i, final_score))
        else:
            ranked_scores.append((i, 0))
        # data = {
        #     "index": i,
        #     "final_score": final_score,
        #     "similarity_scores": similarity_scores[i][1],
        #     "score": product_metadata.loc[i, 'score'],
        #     "values": str(product_metadata.iloc[i].to_dict())
        # }
        # results.append(data)
        # temp.append(results)

    ranked_scores = sorted(ranked_scores, key=lambda x: x[1], reverse=True)

    # df = pd.DataFrame(flatten(temp), columns=[
    #     'index', 'final_score', 'similarity_scores', 'score', 'values'])
    # df.to_csv('giftpickr_products.csv', index=False, encoding='utf-8')

    # use the generated score along with similarity to rank the other products
    other_ranked_scores = []
    for i in range(len(product_metadata)):
        final_score = 0
        if i in other_product_indices:
            similarity_weight = 0.5
            product_weight = 0.5
            final_score = similarity_weight * \
                similarity_scores[i][1] + product_weight * \
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


def flatten(l):
    return [item for sublist in l for item in sublist]
