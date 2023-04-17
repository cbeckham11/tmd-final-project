import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(next_token: str, iteration: int):
    tweet_fields = "tweet.fields=author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,reply_settings,source,text&user.fields=created_at,description,entities,id,location,name,public_metrics,username"
    start_time = 'start_time=2020-11-04T00:00:00.000Z'
    end_time = 'end_time=2020-11-14T00:00:00.000Z'
    if iteration == 0:
        url = "https://api.twitter.com/2/tweets/search/all?query=%22shade%22&{}&{}&{}&max_results=100".format(start_time, end_time, tweet_fields)
    else:
        url = "https://api.twitter.com/2/tweets/search/all?query=%22shade%22&{}&{}&{}&max_results=100&next_token={}".format(start_time, end_time, tweet_fields, next_token)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # create first call
    count = 0
    url = create_url(None, count)

    json_response = connect_to_endpoint(url)
    json_object = json.dumps(json_response, indent=4, sort_keys=True)

    filename = "response1.json"
    with open(filename, "w") as outfile:
        outfile.write(json_object)

    next_token = json_response['meta']['next_token']
    res_count = 0
    time.sleep(3)
    
    while next_token is not None:
        count += 1
        url = create_url(next_token, count)

        json_response = connect_to_endpoint(url)
        json_object = json.dumps(json_response, indent=4, sort_keys=True)

        next_token = json_response['meta']['next_token']

        filename = f"response{count}.json"
        with open(filename, "w") as outfile:
            outfile.write(json_object)

        res_count += json_response['meta']['result_count']
        print(res_count)
        time.sleep(2.5)

if __name__ == "__main__":
    main()
