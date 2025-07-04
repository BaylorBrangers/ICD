import requests
import json
import os
import time

API_KEY = os.getenv("WHO_API_KEY")
if not API_KEY:
    raise ValueError("Set WHO_API_KEY in your environment.")

BASE_URL = "https://id.who.int/icd/entity/"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

ROOT_ENTITY = "1218675610"  # Mental, behavioural or neurodevelopmental disorders

def get_children(entity_id):
    url = BASE_URL + entity_id + "/children"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["destinationEntities"]

def get_details(entity_id):
    url = BASE_URL + entity_id
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def recurse(entity_id, results):
    for child in get_children(entity_id):
        detail = get_details(child["id"])
        title = detail.get("title", {}).get("@value", "")
        definition = detail.get("definition", {}).get("@value", "")
        results.append({"id": child["id"], "title": title, "definition": definition})
        time.sleep(0.1)
        recurse(child["id"], results)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    collected = []
    recurse(ROOT_ENTITY, collected)
    with open("data/mental_disorders.json", "w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=2)
