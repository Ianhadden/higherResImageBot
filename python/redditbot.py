import praw
import commonutils as cu
from bingvisualsearch import get_highest_res_image_for_url

def main():

    keys = cu.get_api_keys()

    reddit = praw.Reddit(
        client_id=keys.get("reddit-client-id"),
        client_secret=keys.get("reddit-client-secret"),
        user_agent=keys.get("reddit-user-agent"),
        username=keys.get("reddit-username"),
        password=keys.get("reddit-password")
    )

    #print(reddit.user.me())

    subreddit = reddit.subreddit("pics")

    for submission in subreddit.hot(limit=3):
        print("")
        print(submission.title)
        print(submission.url)
        if has_common_image_format(submission.url):
            print("has common image format")
            highest_res_url = get_highest_res_image_for_url(submission.url)
            if highest_res_url is None:
                print("no bigger image found")
            else:
                print("og url: " + submission.url)
                print("new url: " + highest_res_url)


def has_common_image_format(url):
    return url.endswith("png") or url.endswith("jpg") or url.endswith("jpeg")

main()