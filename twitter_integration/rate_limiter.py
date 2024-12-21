import time
import logging


class RateLimiter:
    """
    A utility to manage API rate limits.
    """

    def __init__(self, max_requests, time_window):
        """
        Initialize with maximum requests and the time window (in seconds).
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.request_timestamps = []
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def can_proceed(self):
        """
        Check if a new request can proceed based on rate limits.
        """
        current_time = time.time()
        self.request_timestamps = [
            ts for ts in self.request_timestamps if ts > current_time - self.time_window
        ]
        if len(self.request_timestamps) < self.max_requests:
            return True
        return False

    def record_request(self):
        """
        Record a new request.
        """
        if self.can_proceed():
            self.request_timestamps.append(time.time())
            self.logger.info("Request recorded.")
            return True
        else:
            self.logger.warning("Rate limit reached. Delaying request.")
            return False

    def wait_until_available(self):
        """
        Wait until the next request can be made.
        """
        while not self.can_proceed():
            time_to_wait = self.time_window - (time.time() - self.request_timestamps[0])
            self.logger.info(f"Waiting {time_to_wait:.2f} seconds.")
            time.sleep(max(0.1, time_to_wait))
