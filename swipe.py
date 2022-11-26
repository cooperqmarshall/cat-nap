from praw.models.listing.generator import ListingGenerator
from praw.models.reddit.submission import Submission
from os import environ, path
from urllib.parse import urlparse
import redis
import requests


def get_original_image_url(posts: ListingGenerator) -> Submission:
    post = next(posts)
    conn = get_redis_connection()
    while post:
        if should_get_post(conn, post):
            conn.set(post.url, 'used')
            return post

        post = next(posts)

    raise Exception('could not find non-duplicate image url')


def get_redis_connection() -> redis.Redis:
    return redis.from_url(environ['REDIS_URL'])


def is_duplicate_url(conn: redis.Redis, url: str) -> bool:
    '''
    Checks if a redis database contains the passed url strings as a key.

    :params
        conn: redis instance
        url: string representing a url of a reddit post

    :returns
        True if the `url` param exists as a key in the redis database
    '''
    return conn.get(url) is not None


def should_get_post(conn: redis.Redis, post: Submission) -> bool:
    file_path = urlparse(post.url).path
    file_type = path.splitext(file_path)[1]
    return file_type in ['.jpg', '.png'] \
        and not post.over_18 \
        and not is_duplicate_url(conn, post.url) \
        and post.link_flair_text == 'Cat Picture'


def get_image(url: str) -> bytes:
    req = requests.get(url)
    return req.content
