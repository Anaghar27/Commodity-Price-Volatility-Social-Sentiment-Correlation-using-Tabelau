import os, pandas as pd
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)
analyzer = SentimentIntensityAnalyzer()

engine = create_engine(
    f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"
    f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DB')}"
)

# map each commodity symbol to its subreddit
sub_map = {"CL=F": "wallstreetbets", "GC=F": "Gold", "SI=F": "Silver"}

def fetch_and_store():
    rows = []
    for symbol, sub in sub_map.items():
        for post in reddit.subreddit(sub).new(limit=200):
    text = post.title or post.selftext or ""
    compound = analyzer.polarity_scores(text)["compound"]  # between -1 and +1
    data.append({
      "topic": sub,
      "created_utc": post.created_utc,
      "score": compound
    })
    pd.DataFrame(rows).to_sql("staging_reddit", engine, if_exists="replace", index=False)

if __name__ == "__main__":
    fetch_and_store()