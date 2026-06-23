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


# ---- METRIC 1: Known-Item Search (Mean Reciprocal Rank) --------------------
# 5 target pages + the keywords 

eval_dataset_dict = {
    "psychology":                          "https://www.uva.nl/en/programmes/bachelors/psychology/psychology.html",
    "communication science":               "https://www.uva.nl/en/programmes/bachelors/communication-science/communication-science.html",
    "day in the life music student":       "https://www.facebook.com/reel/2370505260088549/",
    "master's information session choose": "https://www.facebook.com/reel/767129205881787/",
    "exam week studying library":          "https://www.facebook.com/UniversityofAmsterdam/posts/pfbid0CUS9ZFvhtNF9fbtS1eaK6GcnAhL4HtVPK129FdwbK9bTviz9BJqL4gnuZToq1e8hl",
}

def reciprocal_rank(results, target_url, k=10):
    # rank is the 1-based position, so RR = 1/rank (a #1 hit = 1.0)
    for rank, res in enumerate(results[:k], start=1):
        if target_url and target_url in res["url"]:
            return 1.0 / rank
    return 0.0

print("\n=== METRIC 1: Known-Item Search (Reciprocal Rank) ===")
rr_scores = []
for query, target in eval_dataset_dict.items():
    results = search(query, top_n=10)
    rr = reciprocal_rank(results, target)
    rr_scores.append(rr)
    rank = next((i for i, r in enumerate(results[:10], start=1) if target in r["url"]), None)
    print(f"  RR={rr:.3f}  (rank {rank})  query='{query}'")
print(f"  --> Mean Reciprocal Rank (MRR) = {sum(rr_scores)/len(rr_scores):.3f}")

# ---- METRIC 2: Informational Search (Precision@k) --------------------------
# # Precision@k: fraction of the top-k results that are actually on-topic.
# Relevance = result contains a related topic word from the rubric.

K = 5
informational_queries = {
    "international student": {"international","exchange","visa","abroad","foreign","immigration","master","llm","admission","semester"},
    "exchange semester":     {"exchange","semester","abroad","incoming","registration","deregister"},
    "law degree":            {"law","legal","llm","justice","competition","rights","tax"},
    "study tips":            {"tip","tips","advice","prepare","preparation","resources","resource","resit","help"},
    "free ticket event":     {"ticket","opera","concert","event","events","invitation","festival","show"},
}

def precision_at_k(query, rubric_terms, k=K):
    scores = bm25.get_scores(query.lower().split())
    idx = [i for i in sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
           if scores[i] > 0][:k]
    if not idx:
        return 0.0, 0
    relevant = sum(1 for i in idx
                   if set(documents[i]["text"].lower().split()) & rubric_terms)
    return relevant / len(idx), len(idx)

print(f"\n=== METRIC 2: Informational Search (Precision@{K}) ===")
p_scores = []
for query, rubric in informational_queries.items():
    p, n = precision_at_k(query, rubric)
    p_scores.append(p)
    print(f"  P@{n}={p:.2f}  query='{query}'")
print(f"  --> Mean Precision = {sum(p_scores)/len(p_scores):.3f}")