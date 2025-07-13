import tweepy
import os

def twitter_auth():
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    )
    return client

def publish_tweet(text):
    client = twitter_auth()
    response = client.create_tweet(text=text)
    print(f"Tweet publié: {response.data['id']}")

if __name__ == "__main__":
    publish_tweet("Lancement de mon nouveau produit digital 🚀 #business #digital")
