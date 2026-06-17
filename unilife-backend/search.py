import re
import pandas as pd

def load_reddit_posts(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    # split reddit posts into blocks
    blocks = re.split(r"--- POST \d+ ---", raw)
    
    reddit_docs = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        
        # Extract each field using regex
        title_match = re.search(r"title:\s*(.+)", block)
        text_match = re.search(r"text:\s*(.+?)\n\nfull_content:", block, re.DOTALL)
        content_match = re.search(r"full_content:\s*(.+)", block, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else "Reddit Post"
        full_content = content_match.group(1).strip() if content_match else ""
        
        reddit_docs.append({
            "title": title,
            "text": full_content,
            "url": "",  # no urls are in this file
            "source": "reddit"
        })
    
    return reddit_docs

#load csv files and put on same path
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
programmes = pd.read_csv(os.path.join(base_dir, "uva_english_programme_titles.csv"))
posts = pd.read_csv(os.path.join(base_dir, "uva_facebook_posts.csv"))

documents = []
#combining both sources
for _, row in programmes.iterrows():
    documents.append({
        "title": row["Official Programme Name"],
        "text": row["Official Programme Name"],
        "url": row["Source URL"],
        "source": "programme"
    })

for _, row in posts.iterrows():
    documents.append({
        "title": row["text"][:45], # first 45 characters are the title
        "text": row["text"],
        "url": row["url"],
        "source": "post"
    })

documents.extend(load_reddit_posts(os.path.join(base_dir, "reddit_posts.txt")))

from rank_bm25 import BM25Okapi

tokenized_docs = [doc["text"].lower().split() for doc in documents]
bm25 = BM25Okapi(tokenized_docs)

def search(query, top_n=5):
    tokens = query.lower().split()
    scores = bm25.get_scores(tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    
    results = []
    for i in top_indices:
        if scores[i] > 0:  # please return actual matches only
            results.append({
                "title": documents[i]["title"],
                "url": documents[i]["url"],
                "source": documents[i]["source"],
                "score": round(scores[i], 3)
            })
    return results

if __name__ == "__main__":
    query = "media"
    results = search(query)
    for r in results:
        print(r)