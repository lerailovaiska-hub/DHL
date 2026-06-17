import re
import pandas as pd

programmes = pd.read_csv("uva_english_programme_titles.csv")
posts = pd.read_csv("uva_facebook_posts.csv")

documents = []

for _, row in programmes.iterrows():
    documents.append({
        "title": row["Official Programme Name"],
        "text": row["Official Programme Name"],  # or full_content if using the richer CSV
        "url": row["Source URL"],
        "source": "programme"
    })

from rank_bm25 import BM25Okapi

tokenized_docs = [doc["text"].lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)