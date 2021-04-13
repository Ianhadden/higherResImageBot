import requests, json, os
import commonutils as cu

bing_calls_enabled = False

# Given a url of an image, returns the url of the highest resolution version
# of that image found with bing visual search. If no larger version is found,
# returns None
def get_highest_res_image_for_url(url):
    print("Running!")

    visual_search_results = get_bing_visual_search_results(url)

    default_insights = get_default_insights(visual_search_results)

    highest_res_image = find_highest_res_image(default_insights)
    original_image = find_requested_image(default_insights)

    if highest_res_image is None:
        print("no other pages had the image")
        return None

    if highest_res_image.get("height") > original_image.get("height"):
        print("found a bigger image")
        return highest_res_image.get("contentUrl")
    else:
        print("did not find a bigger image")
        return None


# returns the default insights tag object from a bing visual search result
def get_default_insights(visual_search_results):
    # https://docs.microsoft.com/en-us/azure/cognitive-services/bing-visual-search/default-insights-tag
    response_tags = visual_search_results.get("tags")
    for insight_tag in response_tags:
        # default insight tag has empty string as displayName
        if insight_tag.get("displayName") == "":
            return insight_tag


# returns the image object of the highest res version of the image in the visual search results.
# returns None if no other page other than the one inputted into the visual search contains the image.
# takes the default insights object from the visual search results as a parameter
def find_highest_res_image(default_insights):

    for action in default_insights.get("actions"):
        if action.get("actionType") == "PagesIncluding":
            pages_including = action
            break

    largest_height = 0
    largest_image = None
    for image in pages_including.get("data").get("value"):
        if image.get("height") > largest_height:
            largest_height = image.get("height")
            largest_image = image

    return largest_image


# returns the image object associated with the image/url that was the input to the visual search
# takes the default insights object from the visual search results as a parameter
def find_requested_image(default_insights):
    # imageById holds image associated with request input
    for action in default_insights.get("actions"):
        if action.get("actionType") == "ImageById":
            return action.get("image")


def get_bing_visual_search_results(url):
    if bing_calls_enabled:
        return do_bing_visual_search(url)
    else:
        return do_mock_bing_visual_search()


# returns json from file
def do_mock_bing_visual_search():
    print("reading bing output from file")
    file = cu.open_file_from_repo_root("/bing visual search samples/output from wonky request.json")
    return json.load(file)


# Returns json from the bing visual search
def do_bing_visual_search(url):
    print("getting bing output from visual search")
    keys = cu.get_api_keys()
    bing_key = keys.get("bing-resource-key")

    imageInfo = {"imageInfo" : {"url" : url}}

    BASE_URI = 'https://api.bing.microsoft.com/v7.0/images/visualsearch'
    REQUEST_FILES = {'knowledgeRequest': (None, json.dumps(imageInfo))}
    HEADERS = {'Ocp-Apim-Subscription-Key': bing_key}
    
    try:
        response = requests.post(BASE_URI, headers=HEADERS, files=REQUEST_FILES)
        response.raise_for_status()
        #print_json(response.json())
        return response.json()
        
    except Exception as ex:
        raise ex


def print_json(obj):
    """Print the object as json"""
    print(json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': ')))