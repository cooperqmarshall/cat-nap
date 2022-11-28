from os import environ
from praw import Reddit
from praw.models.reddit.submission import Submission
from swipe import get_post


def test_get_post():
    reddit = Reddit(
        client_id=environ['CLIENT_ID'],
        client_secret=environ['CLIENT_SECRET'],
        user_agent=environ['CAT_NAP_USER_AGENT'])
    posts = reddit.subreddit('cats').hot()
    post = get_post(posts, is_duplicate=True, has_image=True)

    assert type(post) == Submission
