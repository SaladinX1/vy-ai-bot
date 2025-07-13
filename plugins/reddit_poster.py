
# plugins/reddit_poster.py

import praw

# Configuration à personnaliser ou charger depuis un fichier .env / config
REDDIT_CLIENT_ID = "your_client_id"
REDDIT_CLIENT_SECRET = "your_client_secret"
REDDIT_USER_AGENT = "AutoPosterBot v1.0"
REDDIT_USERNAME = "your_username"
REDDIT_PASSWORD = "your_password"

# Initialisation de l'API Reddit
def get_reddit_instance():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD
    )

def post_to_subreddit(args):
    reddit = get_reddit_instance()
    subreddit_name = args["subreddit"]
    title = args["title"]
    content = args.get("content", "")

    try:
        submission = reddit.subreddit(subreddit_name).submit(title, selftext=content)
        print(f"[REDDIT] Posté sur r/{subreddit_name}: {submission.url}")
        return {"status": "posted", "url": submission.url}
    except Exception as e:
        print(f"[REDDIT ERROR] {e}")
        return {"status": "error", "message": str(e)}

def handle_action(action, args):
    if action == "post_to_subreddit":
        return post_to_subreddit(args)
    raise ValueError(f"Action inconnue: {action}")
