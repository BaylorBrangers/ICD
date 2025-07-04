import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import umap
import gradio as gr

with open("data/mental_disorders.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data).dropna(subset=["definition"]).reset_index(drop=True)
titles = df["title"].tolist()
definitions = df["definition"].tolist()

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(definitions)
proj = umap.UMAP(n_neighbors=10, min_dist=0.3, metric="cosine").fit_transform(embeddings)

df["x"] = proj[:, 0]
df["y"] = proj[:, 1]

def plot(query):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.scatter(df["x"], df["y"], alpha=0.5)
    if query:
        matches = df[df["title"].str.contains(query, case=False)]
        ax.scatter(matches["x"], matches["y"], color="red", label="Matches")
        for _, row in matches.iterrows():
            ax.annotate(row["title"], (row["x"], row["y"]), fontsize=7)
    return fig

gr.Interface(
    fn=plot,
    inputs=gr.Textbox(label="Search Disorder Title"),
    outputs=gr.Plot(label="UMAP Plot"),
    title="ICD-11 Mental Disorder UMAP Explorer"
).launch()
