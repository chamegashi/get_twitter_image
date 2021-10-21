import json, config
# from typing import 
from requests_oauthlib import OAuth1Session

from TwitterImageFormat import TwitterImage

AK = config.API_KEY
AS = config.API_SECRET_KEY
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(AK, AS, AT, ATS) #認証処理

# ---- フォロー取得
def get_follow():

    url = "https://api.twitter.com/1.1/friends/list.json"
    follow_list = []

    res = twitter.get(url)

    if res.status_code == 200:
        users = json.loads(res.text)['users']
        for user in users:
            follow_list.append(user['id'])

    else:
        print("Failed: %d" % res.status_code)

    return follow_list

# ---- user 情報取得
def get_user_from_user_name(user_name):
    url = "https://api.twitter.com/1.1/users/lookup.json?screen_name=" + user_name
    res = twitter.get(url)
    data = json.loads(res.text)[0]
    return {
        "id": data["id_str"],
        "name": data["name"],
        "screen_name": data["screen_name"],
        "profile_image_url": data["profile_image_url"]
    }

# ---- image 取得
def get_images(users):
    nnx = 30
    url_base = "https://api.twitter.com/1.1/statuses/user_timeline.json?user_id="
    ret_image_urls = []

    for user in users:
        url = url_base + user['id'] + "&count=" + str(nnx)
        res = twitter.get(url)
        check_image = []

        if res.status_code == 200:
            data = json.loads(res.text)
            for tweet in data:
                text = tweet['text']

                # RT 判定
                if(text[0:2] == "RT"):
                    if not ('extended_entities' in tweet):
                        continue

                    media_list = tweet['extended_entities']['media']

                    for media in media_list:
                        image_url = media['media_url']

                        if image_url in check_image:
                            continue

                        tweet_url = tweet['entities']['media'][0]['expanded_url'][0:-8]
                        check_image.append(
                            TwitterImage(
                                image_url,
                                tweet_url,
                                tweet["text"],
                                tweet["created_at"],
                                user['name']
                            )
                        )

                    continue

                if("https://t.co" in text):
                    if not ('extended_entities' in tweet):
                        continue

                    media_list = tweet['extended_entities']['media']

                    for media in media_list:
                        image_url = media['media_url']

                        if image_url in check_image:
                            continue

                        tweet_url = tweet['entities']['media'][0]['expanded_url'][0:-8]
                        check_image.append(
                            TwitterImage(
                                image_url,
                                tweet_url,
                                tweet["text"],
                                tweet["created_at"],
                                user['name']
                            )
                        )
            
            ret_image_urls.append(check_image)

        else:
            print("Failed: %d" % res.status_code)
    
    return ret_image_urls


if __name__ == '__main__':
    user = get_user_from_user_name("papaiaMK2")
    res = get_images([user])
    print(res)

