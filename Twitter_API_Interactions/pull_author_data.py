import requests
import os
import json
import time

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url(id: any):
    user_fields = "user.fields=created_at,description,entities,id,location,name,public_metrics,username"
    url = "https://api.twitter.com/2/users?ids={}&{}".format(id, user_fields)
    print('create_url', url)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    authors = open("author_chunks.txt", "r")
    data = authors.read()
    data_into_list = data.split('\n')

    for i, user_id in enumerate(data_into_list):
        url = create_url(user_id)

        json_response = connect_to_endpoint(url)
        json_object = json.dumps(json_response, indent=4, sort_keys=True)

        filename = f"response_user{i}.json"
        with open(filename, "w") as outfile:
            outfile.write(json_object)

        print(f'{i}/{len(data_into_list)}')
        time.sleep(3)

    authors.close()


if __name__ == "__main__":
    main()
