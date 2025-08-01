import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.request.RecRequestResourceModel import RecRequestResourceModel
from sentence_transformers import SentenceTransformer, util


class MachineLearningToolkit:
    def __init__(self, config: dict = None):
        self.__config = config

        self.__target_model = self.__config['default_model']

        self.__model = SentenceTransformer(self.__target_model)

    @staticmethod
    def tokenize_title(title: str) -> set:
        title = re.sub(r'[^a-zA-Z0-9\s]+', '', title).lower().split()
        return set(title)

    @staticmethod
    def jaccard_sim(og_product: set, product: set) -> float:
        intersection = len(og_product.intersection(product))
        union = len(og_product.union(product))
        return intersection / union

    @staticmethod
    def get_product_jaccard_sim(
            product_resource: RecRequestResourceModel,
            related_product_name_field: str,
            related_products_df: pd.DataFrame
    ) -> pd.DataFrame:
        related_products_df = related_products_df.copy()
        # Tokenize the original product title
        og_product_tokens = MachineLearningToolkit.tokenize_title(
            product_resource.product_title
        )

        # Apply Jaccard similarity for each row in the DataFrame
        related_products_df['similarity'] = related_products_df[
            related_product_name_field
        ].apply(
            lambda x: MachineLearningToolkit.jaccard_sim(
                og_product_tokens, MachineLearningToolkit.tokenize_title(x)
            )
        )

        return related_products_df

    @staticmethod
    def get_product_cosine_sim(
            product_resource: RecRequestResourceModel,
            related_product_name_field: str,
            related_products_df: pd.DataFrame
    ) -> pd.DataFrame:
        related_products_df = related_products_df.copy()
        # Combine the product titles (original product + related products)
        product_titles = (
            [product_resource.product_title] +
            related_products_df[related_product_name_field].tolist()
        )

        # Compute TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(product_titles)

        # Calculate cosine similarities between the original product and
        # related products
        cosine_similarities = cosine_similarity(
            tfidf_matrix[0:1], tfidf_matrix[1:]
        ).flatten()

        # Assign the cosine similarity scores to the DataFrame
        related_products_df['similarity'] = cosine_similarities

        return related_products_df

    def get_product_sbert_sim(
            self,
            product_resource: RecRequestResourceModel,
            related_product_name_field: str,
            related_products_df: pd.DataFrame
    ) -> pd.DataFrame:
        # Get the embedding of the original product title
        product_title = product_resource.product_title
        product_embedding = self.__model.encode(product_title,
                                                convert_to_tensor=True)

        # Get embeddings for all related product titles
        related_titles = related_products_df[
            related_product_name_field
        ].tolist()
        related_embeddings = self.__model.encode(
            related_titles, convert_to_tensor=True
        )

        # Compute cosine similarity using SBERT embeddings
        sbert_similarities = util.cos_sim(
            product_embedding, related_embeddings
        ).flatten().tolist()

        # Add the SBERT similarity scores to the DataFrame
        related_products_df['similarity'] = sbert_similarities
        return related_products_df
