import redis
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime, timedelta

app = FastAPI()
# be sure redis is up: `docker run -p 6379:6379 redis`
r = redis.Redis(host="localhost", port=6379, db=0)

MAX_REQUESTS = 5
WINDOW_SECONDS = 60

@app.get("/")
def get_click_count(request: Request):
    client_ip = request.client.host
    key = f"sliding:{client_ip}"
    now = datetime.utcnow().timestamp()

    # remove old entries
    r.ltrim(key, 0, MAX_REQUESTS - 1)
    timestamps = r.lrange(key, 0, -1)
    timestamps = [float(ts.decode()) for ts in timestamps if float(ts.decode()) > now - WINDOW_SECONDS]

    if len(timestamps) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    r.lpush(key, now)
    r.expire(key, WINDOW_SECONDS)  # auto-clean if inactive

    return {"msg": f"Allowed: {len(timestamps) + 1} requests in current window"}


if __name__ == "__main__":
    uvicorn.run("zesty-redis-try:app", host="0.0.0.0", port=8000)