import json
import random
import time
import os
from dotenv import load_dotenv
from src.connection_manager import ConnectionManager
from src.helpers import print_h_bar


class ZerePyAgent:
    def __init__(
            self,
            name: str,
            model: str,
            model_provider: str,
            connection_manager: ConnectionManager,
            bio: list[str],
            traits: list[str],
            examples: list[str],
            timeline_read_count: int=10,
            replies_per_tweet: int=5,
            loop_delay: int=30
    ):
        self.name = name
        self.model = model
        self.model_provider = model_provider
        self.connection_manager = connection_manager
        self.bio = bio
        self.traits = traits
        self.examples = examples

        # Behavior Parameters
        self.timeline_read_count = timeline_read_count
        self.replies_per_tweet = replies_per_tweet
        self.loop_delay = loop_delay

        # Load credentials to get user info
        load_dotenv()
        self.username = os.getenv('TWITTER_USERNAME', '').lower()
        
        # Cache for system prompt
        self._system_prompt = None

    def _construct_system_prompt(self) -> str:
        if self._system_prompt is None:
            prompt_parts = []
            prompt_parts.extend(self.bio)
            
            if self.traits:
                prompt_parts.append("\nYour key traits are:")
                prompt_parts.extend(f"- {trait}" for trait in self.traits)
            
            if self.examples:
                prompt_parts.append("\nHere are some examples of your style:")
                prompt_parts.extend(f"- {example}" for example in self.examples)
            
            self._system_prompt = "\n".join(prompt_parts)
        
        return self._system_prompt

    def reset_system_prompt(self):
        self._system_prompt = None

    def prompt_llm(self, prompt: str, custom_sys_prompt: str = None, **kwargs) -> str:
        system_prompt = custom_sys_prompt if custom_sys_prompt else self._construct_system_prompt()
        
        return self.connection_manager.find_and_perform_action(
            action_string="generate-text",
            connection_string=self.model_provider,
            prompt=prompt,
            system_prompt=system_prompt,
            model=self.model,
            **kwargs)

    def loop(self):
        """Main agent loop with hardcoded Twitter interactions"""
        # Configurable behavior weights
        TWEET_INTERVAL = 300  # Post new tweet every 5 minutes
        INTERACTION_WEIGHTS = {
            'nothing': 0.5,  # 50% chance to do nothing
            'like': 0.25,     # 25% chance to like
            'reply': 0.25     # 25% chance to reply
        }
        SELF_REPLY_CHANCE = 0.05  # Very low chance to reply to own tweets
        
        print_h_bar()
        print("\n🤖 Starting agent loop in 5 seconds...")
        print_h_bar()
        
        for i in range(5, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        last_tweet_time = 0

        while True:
            try:
                # Check if it's time to post a new tweet
                current_time = time.time()
                if current_time - last_tweet_time >= TWEET_INTERVAL:
                    print_h_bar()
                    print("\n📝 GENERATING NEW TWEET")
                    print_h_bar()
                    
                    prompt = "Generate an engaging tweet about AI, technology, or programming. Include at most one relevant hashtag, sometimes. Keep it under 280 characters."
                    tweet_text = self.prompt_llm(prompt)
                    
                    if tweet_text:
                        print("\n🚀 Posting tweet:")
                        print(f"'{tweet_text}'")
                        self.connection_manager.find_and_perform_action(
                            action_string="post-tweet",
                            connection_string="twitter",
                            message=tweet_text
                        )
                        last_tweet_time = current_time
                        print("\n✅ Tweet posted successfully!")

                # Read and interact with timeline
                print_h_bar()
                print("\n👀 READING TIMELINE")
                print_h_bar()
                
                timeline_tweets = self.connection_manager.find_and_perform_action(
                    action_string="read-timeline",
                    connection_string="twitter",
                    count=self.timeline_read_count
                )

                if timeline_tweets:
                    print(f"\nFound {len(timeline_tweets)} tweets to process")
                    
                    # Process each tweet
                    for tweet in timeline_tweets:
                        tweet_id = tweet.get('id')
                        if not tweet_id:
                            continue

                        # Check if it's our own tweet
                        is_own_tweet = tweet.get('author_username', '').lower() == self.username

                        # Skip most self-interactions
                        if is_own_tweet and random.random() > SELF_REPLY_CHANCE:
                            continue

                        # Choose interaction based on weights
                        action = random.choices(
                            list(INTERACTION_WEIGHTS.keys()),
                            weights=list(INTERACTION_WEIGHTS.values())
                        )[0]

                        # For own tweets, downgrade replies to likes
                        if is_own_tweet and action == 'reply':
                            action = 'like'
                            
                        # Perform chosen action
                        if action == 'like':
                            print_h_bar()
                            print(f"\n❤️ LIKING TWEET")
                            print(f"Tweet: {tweet.get('text', '')[:50]}...")
                            self.connection_manager.find_and_perform_action(
                                action_string="like-tweet",
                                connection_string="twitter",
                                tweet_id=tweet_id
                            )
                            print("\n✅ Tweet liked successfully!")
                        
                        elif action == 'reply':
                            print_h_bar()
                            print(f"\n💬 GENERATING REPLY")
                            print(f"To tweet: {tweet.get('text', '')[:50]}...")
                            
                            prompt = f"Generate a friendly, engaging reply to this tweet: '{tweet.get('text')}'. Keep it under 280 characters."
                            reply_text = self.prompt_llm(prompt)
                            
                            if reply_text:
                                print(f"\n🚀 Posting reply:")
                                print(f"'{reply_text}'")
                                self.connection_manager.find_and_perform_action(
                                    action_string="reply-to-tweet",
                                    connection_string="twitter",
                                    tweet_id=tweet_id,
                                    message=reply_text
                                )
                                print("\n✅ Reply posted successfully!")

                # Delay between iterations
                print_h_bar()
                print(f"\n⏳ Waiting {self.loop_delay} seconds before next check...")
                print_h_bar()
                time.sleep(self.loop_delay)

            except Exception as e:
                print_h_bar()
                print(f"\n❌ Error in agent loop: {e}")
                print(f"⏳ Waiting {self.loop_delay} seconds before retrying...")
                print_h_bar()
                time.sleep(self.loop_delay)

    def perform_action(self, action_string: str, connection_string: str, **kwargs):
        result = self.connection_manager.find_and_perform_action(action_string, connection_string, **kwargs)
        return result

    def to_dict(self):
        return {
            "name": self.name,
            "model": self.model,
            "model_provider": self.model_provider,
            "bio": self.bio,
            "traits": self.traits,
            "examples": self.examples,
            "timeline_read_count": self.timeline_read_count,
            "replies_per_tweet": self.replies_per_tweet,
            "loop_delay": self.loop_delay
        }

    def set_preferred_model(self, model):
        # Check if model is valid
        result = self.connection_manager.find_and_perform_action(
            action_string="check-model",
            connection_string=self.model_provider,
            model=model)
        if result:
            self.model = model
            print("Model successfully changed.")
        else:
            print("Model not valid for current provider. No changes made.")

    def set_preferred_model_provider(self, model_provider):
        self.model_provider = model_provider
        self.reset_system_prompt()

    def list_available_models(self):
        self.connection_manager.find_and_perform_action(
            action_string="list-models",
            connection_string=self.model_provider)


def load_agent_from_file(agent_path: str, connection_manager: ConnectionManager) -> ZerePyAgent:
    try:
        # Get agent fields from json file
        agent_dict = json.load(open(agent_path, "r"))

        # Create agent object
        agent = ZerePyAgent(
            name=agent_dict["name"],
            model=agent_dict["model"],
            model_provider=agent_dict["model_provider"],
            connection_manager=connection_manager,
            bio=agent_dict["bio"],
            traits=agent_dict["traits"],
            examples=agent_dict["examples"],
            timeline_read_count=agent_dict["timeline_read_count"],
            replies_per_tweet=agent_dict["replies_per_tweet"],
            loop_delay=agent_dict["loop_delay"]
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Agent file not found at path: {agent_path}")
    except KeyError:
        raise KeyError(f"Agent file is missing a required field.")
    except Exception as e:
        raise Exception(f"An error occurred while loading the agent: {e}")
    return agent


def create_agent_file_from_dict(agent_dict: dict):
    try:
        # Create agent file
        with open(f"agents/{agent_dict['name']}.json", "w") as file:
            # Save agent dict to json file
            json.dump(agent_dict, file, indent=4)
    except Exception as e:
        raise Exception(f"An error occurred while creating the agent file: {e}")