from collections import defaultdict

from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timedelta

app = FastAPI()

user_requests = defaultdict(list)
"""
ip : [time1 ,time2]
"""

def check_if_user_is_ok(host, ts):
    all_enters = user_requests.get(host)
    last_min = ts - timedelta(minutes=1)
    if all_enters:
        counter = 0
        for enter in all_enters:
            if enter > last_min:
                counter +=1
        if counter >= 5:
            return False

    user_requests[host].append(ts)
    return True


@app.get("/")
def get_click_count(request: Request):
    now = datetime.now()
    check_res = check_if_user_is_ok(request.client.host, now)
    if not check_res:
        raise HTTPException(status_code=429)
    return {"msg": f"hello world {request.client.host}"}

