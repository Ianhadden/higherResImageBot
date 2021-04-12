import requests, json, os

def main():
    print("Running!")

    visual_search_results = get_bing_visual_search_results()

    default_insights = get_default_insights(visual_search_results)

    highest_res_image = find_highest_res_image(default_insights)
    original_image = find_requested_image(default_insights)

    if highest_res_image.get("height") > original_image.get("height"):
        print("found a bigger image!")
    else:
        print("did not find a bigger image!")

    #print(highest_res_image.get("contentUrl"))


# returns the default insights tag object from a bing visual search result
def get_default_insights(visual_search_results):
    # https://docs.microsoft.com/en-us/azure/cognitive-services/bing-visual-search/default-insights-tag
    response_tags = visual_search_results.get("tags")
    for insight_tag in response_tags:
        # default insight tag has empty string as displayName
        if insight_tag.get("displayName") == "":
            return insight_tag


# returns the image object of the highest res version of the image searched for using visual search
# takes the default insights object from the visual search results as a parameter
def find_highest_res_image(default_insights):

    for action in default_insights.get("actions"):
        if action.get("actionType") == "PagesIncluding":
            pages_including = action
            break

    largest_height = 0
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


def get_bing_visual_search_results():
    print("entered da function")
    if bing_calls_enabled:
        return do_bing_visual_search()
    else:
        return do_mock_bing_visual_search()


# returns json from file
def do_mock_bing_visual_search():
    print("reading bing output from file")
    file = open_file_from_repo_root("/bing visual search samples/output from url.json")
    return json.load(file)


# Returns json from the bing visual search
def do_bing_visual_search():
    print("getting bing output from visual search")
    keys = json.load(open_file_from_repo_root('/keys/api-keys.json'))
    bing_key = keys.get("bing-resource-key")

    imageInfo = {"imageInfo" : {"url" : "http://tehnostiri.ro/wp-content/uploads/2020/09/broaste.jpg"}}

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


# open a file in the repository using relative path from the root of the repository
def open_file_from_repo_root(relative_path):
    parent_directory = os.path.dirname(os.path.dirname(__file__))
    return open(parent_directory + relative_path)


def print_json(obj):
    """Print the object as json"""
    print(json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': ')))


bing_calls_enabled = False
main()
