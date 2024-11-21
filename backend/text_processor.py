import math
import pandas as pd
from spacy.lang.vi import Vietnamese
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from core.embeddings.models import EmbeddingModel

class TextProcessor:
    def __init__(self, threshold: float = 0.2):
        self.threshold = threshold
        self.nlp = Vietnamese()
        self.nlp.add_pipe('sentencizer')
        self.embedding_model = EmbeddingModel()

    def semantic_splitting(self, text: str) -> list:
        """Splits text into coherent chunks based on semantic similarity."""
        doc = self.nlp(text)
        sentences = [sent.text for sent in doc.sents]

        vectorizer = TfidfVectorizer().fit_transform(sentences)
        vectors = vectorizer.toarray()

        similarities = cosine_similarity(vectors)
        chunks = [[sentences[0]]]

        for i in range(1, len(sentences)):
            sim_score = similarities[i - 1, i]
            if sim_score >= self.threshold:
                chunks[-1].append(sentences[i])
            else:
                chunks.append([sentences[i]])

        return [' '.join(chunk) for chunk in chunks]

    def get_embedding(self, text: str) -> list:
        """Returns the embedding of the input text."""
        return self.embedding_model.get_embedding(text)

    def process_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """Splits content into semantic chunks and returns a DataFrame."""
        processed_df = pd.DataFrame()
        for _, row in df.iterrows():
            content = row['content']
            if content:
                chunks = self.semantic_splitting(content)
                for idx, chunk in enumerate(chunks):
                    new_row = {
                        "url": row['url'],
                        "price": row['price'],
                        "title": row['title'],
                        "image_urls": row['image_urls'],
                        "content": chunk
                    }
                    processed_df = pd.concat([processed_df, pd.DataFrame([new_row])], ignore_index=True)

        processed_df['content'] = processed_df['content'].replace('', math.nan)
        processed_df.dropna(subset=['content'], inplace=True)
        return processed_df
