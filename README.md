
# ICD-11 Mental Disorder UMAP Visualizer

This project extracts mental and behavioral disorders from the ICD-11 Foundation API, embeds their definitions using a sentence transformer, and visualizes them using UMAP. An interactive version is also provided via Gradio.

## Features
- Fetches hierarchical disorder data from ICD-11
- Embeds disorder definitions using `all-MiniLM-L6-v2`
- Projects to 2D using UMAP
- Interactive search and visualization

## Setup

```bash
git clone https://github.com/yourusername/icd11-umap-visualizer.git
cd icd11-umap-visualizer
pip install -r requirements.txt
