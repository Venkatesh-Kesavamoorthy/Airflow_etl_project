import tweepy
import pandas as pd
from datetime import datetime


def run_x_etl():
    # ✅ Explicit bearer token (decoded, not URL-encoded)
    bearer_token = "AAAAAAAAAAAAAAAAAAAAANh44AEAAAAAGGaxhqicgYo1iya%2BJxrajcYpDMc%3DAEPQtV6OdUpdcb7R3KvAdtRxffRtwBPelBuEg6Luvx43Sji90n"

    # Create Tweepy client (disable auto sleep so Airflow handles retries)
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=False)

    try:
        # ✅ Use hardcoded Elon Musk user_id (avoids extra API call)
        ELON_ID = "44196397"

        # Fetch recent tweets (excluding retweets & replies)
        tweets = client.get_users_tweets(
            id=ELON_ID,
            max_results=10,
            tweet_fields=["created_at", "public_metrics", "text"],
            exclude=["retweets", "replies"]
        )

        tweet_list = []
        if tweets.data:
            for tweet in tweets.data:
                refined_tweet = {
                    "user": "elonmusk",
                    "date": tweet.created_at,
                    "text": tweet.text,
                    "retweet_count": tweet.public_metrics["retweet_count"],
                    "like_count": tweet.public_metrics["like_count"],
                    "reply_count": tweet.public_metrics["reply_count"],
                    "quote_count": tweet.public_metrics["quote_count"],
                }
                tweet_list.append(refined_tweet)

        # ✅ Save directly to S3 (Airflow connection/S3 hook handles auth)
        df = pd.DataFrame(tweet_list)
        df.to_csv("s3://airflow-s3-x-bucket/elon_musk_tweets.csv", index=False)

        print(f"✅ Saved {len(df)} tweets to S3")

    except tweepy.errors.TooManyRequests as e:
        # ❌ No time.sleep here
        # ✅ Raise so Airflow retries after retry_delay
        print("⚠️ Rate limit hit — letting Airflow retry...")
        raise

    except tweepy.TweepyException as e:
        print(f"❌ Tweepy error: {e}")
        raise
