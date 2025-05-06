import uvicorn
from fastapi import FastAPI, Request, HTTPException
from collections import defaultdict
from datetime import datetime, timedelta

app = FastAPI()
user_requests = defaultdict(list)


def check_if_user_is_ok(host, ts):
    all_enters = user_requests.get(host)
    last_min = ts - timedelta(minutes=1)
    if all_enters:
        print(f'last_min: {last_min} || {[str(i) for i in all_enters]}')
        if len([1 for enter in all_enters if enter > last_min]) >= 5:
            return False

    user_requests[host].append(ts)
    return True


@app.get("/")
def get_click_count(request: Request):
    now = datetime.now()
    check_res = check_if_user_is_ok(request.client.host, now)
    if not check_res:
        print(f"User {request.client.host} is blocked")
        raise HTTPException(status_code=429)
    return {"msg": f"hello world {request.client.host}"}


if __name__ == "__main__":
    uvicorn.run("zesty-tries:app", host="0.0.0.0", port=8000)