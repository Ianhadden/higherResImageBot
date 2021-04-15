import json, time
import commonutils as cu

CACHE_DIRECTORY_PATH = "/cache/"
CACHE_PATH = "/cache/bing_visual_search_cache.json"
URL_ENTRIES = "url_entries"
LAST_SWEEP_TIME = "last_sweep_time"
HIGH_RES_URL = "high_res_url"
TIME_STAMP = "time_stamp"
SECONDS_IN_DAY = 86400
SECONDS_IN_FIVE_DAYS = 432000

# Checks the cache to see if we have an entry for this url.
# If we don't, returns None. If we do, returns a dict in form {passed_url : high_res_url}
def get_bing_cache_entry_for_url(url):
    if not cu.does_file_exist_from_repo_root(CACHE_PATH):
        return None

    cache_read_file = cu.open_file_from_repo_root(CACHE_PATH)
    cache_data = json.load(cache_read_file)
    cache_read_file.close()
    sweep_if_needed(cache_data)

    if not URL_ENTRIES in cache_data or not url in cache_data.get(URL_ENTRIES):
        return None
    cache_value = cache_data.get(URL_ENTRIES).get(url).get(HIGH_RES_URL)
    return {url : cache_value}

# Add a cache entry to the cache
def add_bing_cache_entry(og_url, new_url):
    if cu.does_file_exist_from_repo_root(CACHE_PATH):
        cache_read_file = cu.open_file_from_repo_root(CACHE_PATH)
        cache_data = json.load(cache_read_file)
        cache_read_file.close()
    else:
        cache_data = {LAST_SWEEP_TIME : time.time(), URL_ENTRIES: {}}

    url_entries_data = cache_data.get(URL_ENTRIES)
    cache_entry = {og_url : {HIGH_RES_URL : new_url, TIME_STAMP : time.time()}}
    url_entries_data.update(cache_entry)

    if not cu.does_file_exist_from_repo_root(CACHE_DIRECTORY_PATH):
        cu.create_directory_from_repo_root(CACHE_DIRECTORY_PATH)

    cache_write_file = cu.open_file_from_repo_root(CACHE_PATH, "w+")
    json.dump(cache_data, cache_write_file)
    cache_write_file.close()

# Checks if it's been over a day since we last deleted anything from the cache.
# If it has been, goes through all the entries and deletes any that are older
# than five days. The reasoning is that after 5 days that submission should 
# not be on the hot lists anymore so we probably don't need to keep around 
# a cache entry for it. And we need to delete old entries to prevent the 
# cache file from growing indefinitely.
def sweep_if_needed(cache_data):
    current_time = time.time()
    if current_time - cache_data.get(LAST_SWEEP_TIME) > SECONDS_IN_DAY:
        cache_url_entries = cache_data.get(URL_ENTRIES)
        for key, value in list(cache_url_entries.items()):
            if current_time - value.get(TIME_STAMP) > SECONDS_IN_FIVE_DAYS:
                del cache_url_entries[key]
        cache_data[LAST_SWEEP_TIME] = current_time
        cache_write_file = cu.open_file_from_repo_root(CACHE_PATH, "w")
        json.dump(cache_data, cache_write_file)
        cache_write_file.close()