# utils/ml_utils.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def get_recommendations(product_id, metadata_df, num_recommendations=5):
    """
    Given a product ID and metadata dataframe, returns a list of recommended products based on cosine similarity.

    Args:
        product_id (str): ID of the product to get recommendations for
        metadata_df (pandas.DataFrame): dataframe containing product metadata, including interest, occasion and relationship
        num_recommendations (int, optional): number of recommendations to return. Defaults to 5.

    Returns:
        list: list of recommended products based on cosine similarity
    """

    # create a new DataFrame with only the product metadata columns
    product_metadata = metadata_df[['product_id', 'interest', 'occasion', 'relationship']]
    
    # combine the metadata columns into a single string for each product
    product_metadata['metadata'] = product_metadata.apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    
    # create a CountVectorizer object to create a sparse matrix of word counts for each product metadata string
    count = CountVectorizer()
    count_matrix = count.fit_transform(product_metadata['metadata'])
    
    # calculate the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    # get the row index of the product we want to get recommendations for
    product_index = product_metadata[product_metadata['product_id'] == product_id].index[0]
    
    # get the cosine similarity scores for the product we want to get recommendations for
    similarity_scores = list(enumerate(cosine_sim[product_index]))
    
    # sort the similarity scores in descending order
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # get the indices of the top n most similar products
    top_indices = [i[0] for i in similarity_scores[1:num_recommendations+1]]
    
    # get the product IDs of the top n most similar products
    top_products = list(product_metadata.iloc[top_indices]['product_id'])
    
    return top_products
