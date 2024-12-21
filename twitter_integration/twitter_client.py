import tweepy
import logging


class TwitterClient:
    """
    Handles Twitter API authentication and basic operations like sending tweets
    and fetching data.
    """

    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        """
        Initialize the Twitter client with API credentials.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.api = self.authenticate()
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def authenticate(self):
        """
        Authenticate with the Twitter API using Tweepy.
        Returns: Tweepy API object.
        """
        try:
            auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            return tweepy.API(auth)
        except Exception as e:
            self.logger.error(f"Failed to authenticate: {e}")
            raise

    def send_tweet(self, text):
        """
        Send a tweet.
        """
        try:
            response = self.api.update_status(status=text)
            self.logger.info(f"Tweet sent: {response.id}")
            return response.id
        except Exception as e:
            self.logger.error(f"Failed to send tweet: {e}")
            raise

    def fetch_mentions(self, since_id=None):
        """
        Fetch mentions from the account's timeline.
        """
        try:
            mentions = self.api.mentions_timeline(since_id=since_id, tweet_mode="extended")
            self.logger.info(f"Fetched {len(mentions)} mentions.")
            return mentions
        except Exception as e:
            self.logger.error(f"Failed to fetch mentions: {e}")
            raise

    def follow_user(self, user_id):
        """
        Follow a user by their ID.
        """
        try:
            self.api.create_friendship(user_id=user_id)
            self.logger.info(f"Followed user {user_id}")
        except Exception as e:
            self.logger.error(f"Failed to follow user {user_id}: {e}")

    def fetch_user_details(self, username):
        """
        Fetch user details by username.
        """
        try:
            user = self.api.get_user(screen_name=username)
            self.logger.info(f"Fetched details for user: {username}")
            return user
        except Exception as e:
            self.logger.error(f"Failed to fetch user details for {username}: {e}")
            raise