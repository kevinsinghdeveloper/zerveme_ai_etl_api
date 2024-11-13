from typing import List, Tuple, Union

from models.request.RecRequestResourceModel import RecRequestResourceModel
from models.response.SerpResponseModel import SerpResponseModel
from utility.Utility import Utility
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationEngineManager:
    def __init__(self):
        pass

    def find_same_product(self, product_resource: RecRequestResourceModel,
                          related_products: List[SerpResponseModel],
                          related_product_name_field: str,
                          price_difference_range: Tuple[float, float] = None) -> Union[SerpResponseModel | None]:
        # TODO find same product at lower price
        related_products_df = Utility.dataclass_to_dataframe(related_products)

        # TODO fuzzy match to locate

        def tokenize_title(title):

            title = re.sub(r'[^a-zA-Z0-9\s]+', '', title).lower().split()
            return set(title)


        def jaccard_sim(og_product,product):

            intersection = len(og_product.intersection(product))
            union = len(og_product.union(product))
            return intersection / union 

        def get_product_jaccard_sim(product_resource,related_products_df):
            jaccard_sim_list=[]
            for product in related_products_df:

                title = tokenize_title(product['product_title'])
                product_sim = jaccard_sim(title, tokenize_title(product_resource.product_title))
                jaccard_sim_list.append(product_sim)

            related_products_df['jaccard_sim']=jaccard_sim_list
            return related_products_df
        
        def get_product_cosine_sim(product_resource,related_products_df):
            cosine_sim_list=[]
            product_titles = [product_resource.product_title] 

            for product in related_products_df:
                recommendation_name = product['product_title']
                product_titles.append(recommendation_name)

            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(product_titles)
            cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            for i, product in enumerate(related_products_df):
                cosine_sim_list.append(float(cosine_similarities[i]))

            related_products_df['cosine_sim']=cosine_sim_list
            return related_products_df

        # price_difference_range -> .3 to .6 (30 - 60 % diff) -> not required here -> just find at lower price
        return None

    def find_related_product(self, product_resource: RecRequestResourceModel,
                             related_products: List[SerpResponseModel],
                             related_product_name_field: str,
                             price_difference_range: Tuple[float, float]) -> Union[SerpResponseModel | None]:
        # TODO find similar product at lower price
        related_products_df = Utility.dataclass_to_dataframe(related_products)


        # price_difference_range -> .3 to .6 (30 - 60 % diff)
        return None

