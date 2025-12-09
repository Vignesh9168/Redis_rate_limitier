#Django Redis Rate Limiter 

A Django middleware- based  rate limiter using Redis counter for fixed-window thorttling.

## Features 
- IP-based throttling (per-window)
- Retry-After header
- Simple, production-ready middleware
- Works with reverse proxies (uses X-Forwarded-For if present)

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   pip install -r requirements.txt
3. Ensure Redis is running and reachable at REDIS_URL in settings.py.
4. Run Django migrations (if needed) and start the server:
   python manage.py runserver

## Notes
- This implementation uses a fixed window counter. For stronger guarantees under distributed traffic, consider a Lua script or Redis token-bucket implementation.
- Adjust RATE_LIMIT and WINDOW in settings.py as per your traffic requirements.

