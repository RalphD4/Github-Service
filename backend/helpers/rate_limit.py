# rate limiter written by Vishnu 

import time 

def rl_response(status, headers):
    if status == 429: 
        retry_after =  headers.get("Retry-After", "60")

    if status == 403 and headers.get("X-RateLimit-Remaining") == "0":
        rl_reset = headers.get("X-RateLimit-Reset")
        retry_after = "60"
        reset_time = int(rl_reset) - int(time.time())
        if rl_reset and reset_time > 0:
            retry_after = str(reset_time)

    else:
        return None 

    body = {
        "error" : "rate_limited",
        "message" : "GitHub API rate limits exceeded"
    }

    return body, 429, {"Retry After" : retry_after}

