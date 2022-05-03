import json
from datetime import datetime
import requests
import uuid
from instascrape import Reel,Post,IGTV

login_response={}
json_data={}

def genrate_random_file_name():
    return str(uuid.uuid4())


def authontication(username, password):
    global login_response, json_data

    count=0

    while (not json_data.get("authenticated")) and count<10:

        link = 'https://www.instagram.com/accounts/login/'
        login_url = 'https://www.instagram.com/accounts/login/ajax/'

        time = int(datetime.now().timestamp())
        response = requests.get(link)
        csrf = response.cookies['csrftoken']

        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                    	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
                    	Safari/537.36 Edg/79.0.309.43",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = requests.post(login_url, data=payload, headers=login_header)
        json_data = json.loads(login_response.text)

        count+=1

    return login_response, json_data


def Download_reel(url, login_response, json_data):

    try:
        if json_data.get("authenticated") != None:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            session_id = cookie_jar['sessionid']


            # Header with session id
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            	AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
            	Safari/537.36 Edg/79.0.309.43",
                "cookie": f"sessionid={str(session_id)});"
            }

            # Passing Instagram reel link as argument in Reel Module
            insta_reel = Reel(url)

            # Using scrape function and passing the headers
            insta_reel.scrape(headers=headers)

            # video_name = genrate_random_file_name()+"_video"

            video_name = "rishabh"+"_video"

            # Giving path where we want to download reel to the
            # download function
            insta_reel.download(fp=f"{video_name}.mp4")

            return video_name

    except Exception as e:
        return "None"

def Download_Post(url, login_response, json_data):

    try:
        if json_data.get("authenticated") != None:
            cookies = login_response.cookies
            cookie_jar = cookies.get_dict()
            session_id = cookie_jar['sessionid']


            # Header with session id
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
                Safari/537.36 Edg/79.0.309.43",
                "cookie": f"sessionid={str(session_id)});"
            }

            # Passing Instagram reel link as argument in Reel Module
            insta_post = Post(str(url))

            # Using scrape function and passing the headers
            insta_post.scrape(headers=headers)

            # post_name = genrate_random_file_name()+"_post"

            post_name = "rishabh"+"_post"

            # Giving path where we want to download reel to the
            # download function
            insta_post.download(fp=f"{post_name}.jpg")

            return post_name

    except Exception as e:
        return "None"