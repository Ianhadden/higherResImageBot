import praw
import commonutils as cu
from bingvisualsearch import get_highest_res_image_for_url
from bingresultscache import get_bing_cache_entry_for_url

targeted_phrases = {'high res', 'higher res'}
reply_phrase = "[Here's the highest resolution version of this image I could find]({})"

bot_replies_enabled = False

def main():

    reddit = get_reddit_instance()
    subreddit = reddit.subreddit("all")

    i = 0

    for submission in subreddit.hot():
        i = i + 1
        if i % 10 == 0:
            print(i)
        if not url_has_potential(submission.url):
            continue
        
        for top_level_comment in submission.comments:
            if comment_meets_criteria(top_level_comment, reddit.user.me()):
                print("TITLE: " + submission.title)
                print("URL: "+ submission.url)
                print("COMMENT: " + top_level_comment.body)
                print("COMMENT AUTHOR: " + top_level_comment.author.name)

                highest_res_url = get_highest_res_image_for_url(submission.url)
                if highest_res_url is not None:
                    reply_to_comment(top_level_comment, highest_res_url)
    print("i capped out at {}".format(i))


def reply_to_comment(comment, highest_res_url):
    reply_text = reply_phrase.format(highest_res_url)
    print("Bot's reply: " + reply_text)
    if bot_replies_enabled:
        print("Commenting")
        try:
            comment.reply(reply_text)
        except Exception as ex:
            print("Encountered error when commenting: ")
            print(ex)

# returns true if the given comment is a 
# good candidate to try to reply to
def comment_meets_criteria(comment, bot_name):
    if not hasattr(comment, 'body'):
        return False
    has_targeted_phrase = False
    for phrase in targeted_phrases:
        if phrase in comment.body.lower():
            has_targeted_phrase = True
            break
    if not has_targeted_phrase:
        return False
    for reply in comment.replies:
        print(reply.author.name)
        # don't recomment
        if reply.author.name == bot_name:
            return False
    return True


def get_reddit_instance():
    keys = cu.get_api_keys()

    return praw.Reddit(
        client_id=keys.get("reddit-client-id"),
        client_secret=keys.get("reddit-client-secret"),
        user_agent=keys.get("reddit-user-agent"),
        username=keys.get("reddit-username"),
        password=keys.get("reddit-password")
    )

# returns true if the url has a common image format and our cache either has
# no entry for the url or has an entry with an identified higher res version
def url_has_potential(url):
    if not (url.endswith("png") or url.endswith("jpg") or url.endswith("jpeg")):
        return False
    cache_entry = get_bing_cache_entry_for_url(url)
    if cache_entry is None:
        return True
    return cache_entry.get(url) is not None

main()