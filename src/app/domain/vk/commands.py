import httpx
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
VERSION = float(os.getenv("VERSION", 5.199))
GROUP_ID = os.getenv("GROUP_ID")


async def get_vk_followers_count() -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get('https://api.vk.com/method/groups.getMembers', params={
            "group_id": GROUP_ID,
            "access_token": TOKEN,
            "v": VERSION
        })
        data = response.json()

        if 'response' in data and 'count' in data['response']:
            return data['response']['count']
        else:
            return 0
