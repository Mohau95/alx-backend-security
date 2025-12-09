from datetime import datetime

from django.core.cache import cache


class RateLimiter:
    def __init__(self, limit=100, window=60):
        """
        limit = number of allowed requests
        window = seconds (60s = 1 minute)
        """
        self.limit = limit
        self.window = window

    def is_allowed(self, ip):
        key = f"rate_limit_{ip}"
        data = cache.get(key)

        if not data:
            # First request
            cache.set(key, {"count": 1, "timestamp": datetime.now()}, self.window)
            return True

        count = data["count"]
        timestamp = data["timestamp"]

        # Reset window
        if (datetime.now() - timestamp).seconds > self.window:
            cache.set(key, {"count": 1, "timestamp": datetime.now()}, self.window)
            return True

        # Check limit
        if count >= self.limit:
            return False

        # Increase count
        data["count"] += 1
        cache.set(key, data, self.window)
        return True
