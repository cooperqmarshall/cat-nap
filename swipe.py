from praw.models.listing.generator import ListingGenerator
from praw.models.reddit.submission import Submission
from os import environ, path
from urllib.parse import urlparse
import redis
import requests


def get_post(posts: ListingGenerator, is_duplicate: bool = True, has_image: bool = False) -> Submission:
    '''
    Loops through the praw posts generator and returns a praw post: Submission
    that meets the criteria defined in `should_get_post()`. If no post is
    found, an Exception is raised.

    :params
        posts: a generator function that yeilds a praw Submission
        is_duplicate: if the returned post can be returned again in an
            additional function call. Defaults to true. If set to false, this
            flag triggers the post.url to be saved in a Redis database. This
            requires the REDIS_URL environemt variable to be set 
        has_image: if the post should have an image. Defaults to false

    :returns
        post: a praw Submission object i.e. a reddit post
    '''
    post = next(posts)
    if not is_duplicate:
        conn = get_redis_connection()
    else:
        conn = None
    while post:
        if should_get_post(post, conn, has_image):
            if conn:
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


def should_get_post(post: Submission, conn: redis.Redis | None = None, has_image: bool = False) -> bool:
    file_path = urlparse(post.url).path
    file_type = path.splitext(file_path)[1]
    return (has_image or file_type in ['.jpg', '.png']) \
        and not post.over_18 \
        and (conn is None or not is_duplicate_url(conn, post.url)) \
        and post.link_flair_text == 'Cat Picture'


def get_image(url: str) -> bytes:
    req = requests.get(url)
    return req.content
