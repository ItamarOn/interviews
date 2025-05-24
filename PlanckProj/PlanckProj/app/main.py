from fastapi import FastAPI, HTTPException
from app.models import Repo
import json
import os

app = FastAPI()
print('Established')

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/add_repo")
def add_repository(query: Repo):
    """
    add the repo to repos.json if not exsists
    """
    with open(os.path.join(os.path.dirname(__file__), 'repos.json'), 'r') as file:
        json_object = json.load(file)

    if query.url in json_object:
        raise HTTPException(status_code=400, detail="Repository already exists")

    json_object.append(query.url)

    with open(os.path.join(os.path.dirname(__file__), 'repos.json'), 'w') as file:
        json.dump(json_object, file)

    return {"message": "Repository added", "repository": query.url}

@app.post("/remove_repo")
def remove_repository(query: Repo):
    """
    remove the repo from repos.json if not exsists
    """
    with open(os.path.join(os.path.dirname(__file__), 'repos.json'), 'r') as file:
        json_object = json.load(file)

    if query.url not in json_object:
        raise HTTPException(status_code=400, detail="Repository not exists")

    json_object.remove(query.url)

    with open(os.path.join(os.path.dirname(__file__), 'repos.json'), 'w') as file:
        json.dump(json_object, file)

    return {"message": "Repository removed", "repository": query.url}

@app.post("/weekly_update")
def weekly_update_data():
    """
    for every repo in repoes.json, request the url from web and write the results to data dir
    """
    with open(os.path.join(os.path.dirname(__file__), 'repos.json'), 'r') as file:
        json_object = json.load(file)

    for repo in json_object:
        print(f"Fetching data from {repo}")

    return {"message": "Lookup completed", "number of repositories": len(json_object)}


@app.get("/get_info")
def get_info(name: str, address: str):
    """
    return the info of business by name and address in repos.json
    """
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/users.json'), 'r') as file:
        json_object = json.load(file)

    for item in json_object:
        if item.get("name") == name and item.get("address") == address:
            return {"info": item.get("info", "No info found")}

    raise HTTPException(status_code=400, detail="Business not exists")
