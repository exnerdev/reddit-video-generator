from json import JSONDecodeError
from typing import Final
from requests import get
from internet import UserAgents
from random import choice

Subreddits: Final = [
    "AmItheAsshole",
    "AITAH",
    "TwoHotTakes",
    "EntitledPeople",
    "AmIOverreacting",
    "TrueOffMyChest",
    "TalesFromTheFrontDesk",
]

# Todo - Add Return Type
def GetRedditPost():
    response = get(f"https://www.reddit.com/r/{choice(Subreddits)}.json", headers={ 
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": choice(UserAgents),
    })
    if not response.ok:
        raise Exception(f"Failed to fetch Reddit post: {response.status_code} {response.reason}")
    else:
        try:
            data = response.json()
        except JSONDecodeError as e:
            raise Exception("Failed to decode JSON response. Error: " + str(e))
        
        list = data["data"]["children"]
        if (len(list) > 1):
            return choice(list)["data"]