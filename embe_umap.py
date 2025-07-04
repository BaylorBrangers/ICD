import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt

with open("data/mental_disorders.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data).dropna(subset=["definition"]).reset_index(drop=True)
texts = df["definition"].tolist()
titles = df["title"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

reducer = umap.UMAP(n_neighbors=10, min_dist=0.3, metric="cosine")
proj = reducer.fit_transform(embeddings)

plt.figure(figsize=(12, 9))
plt.scatter(proj[:, 0], proj[:, 1], s=10, alpha=0.7)
for i, title in enumerate(titles):
    plt.annotate(title, proj[i], fontsize=6, alpha=0.5)
plt.title("ICD-11 Mental Disorders - UMAP")
plt.tight_layout()
plt.show()
