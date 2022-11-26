from os import environ

from praw import Reddit

from swipe import get_image, get_original_image_url
from send import format_message, send_message


def main():
    reddit = Reddit(
        client_id=environ['CLIENT_ID'],
        client_secret=environ['CLIENT_SECRET'],
        user_agent=environ['CAT_NAP_USER_AGENT'])

    posts = reddit.subreddit(environ['SUBREDDIT']).hot()

    post = get_original_image_url(posts)
    image = get_image(post.url)
    msg = format_message(image, post.url)
    send_message(msg, host='smtp.gmail.com', port=587)


if __name__ == '__main__':
    main()
