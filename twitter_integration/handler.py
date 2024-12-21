from .twitter_client import TwitterClient
from .rate_limiter import RateLimiter
import random


class TweetHandler:
    """
    Handles automated tweeting and replies.
    """

    def __init__(self, twitter_client, rate_limiter):
        """
        Initialize with TwitterClient and RateLimiter instances.
        """
        self.twitter_client = twitter_client
        self.rate_limiter = rate_limiter
        self.default_replies = [
            "Thank you for reaching out.",
            "I appreciate your thoughts.",
            "Your message means a lot.",
        ]

    def post_tweet(self, content):
        """
        Post a tweet if within rate limits.
        """
        if self.rate_limiter.record_request():
            return self.twitter_client.send_tweet(content)
        else:
            self.rate_limiter.wait_until_available()
            return self.post_tweet(content)

    def reply_to_mention(self, mention):
        """
        Reply to a specific mention.
        """
        user = mention.user.screen_name
        reply = random.choice(self.default_replies)
        response = f"@{user} {reply}"
        self.post_tweet(response)

    def handle_mentions(self, since_id=None):
        """
        Fetch and handle mentions since the given ID.
        """
        mentions = self.twitter_client.fetch_mentions(since_id)
        for mention in mentions:
            self.reply_to_mention(mention)
        if mentions:
            return mentions[0].id
        return since_id