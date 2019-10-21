import sys
import csv
import aiohttp
import asyncio
from bs4 import BeautifulSoup


def main(filename, links):
    # Ваш код
    raise NotImplementedError


async def statistic(link, result):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                res = {}
                soup = BeautifulSoup(await response.text(), "html.parser")
                users = soup.find_all("a", attrs={"class": ["user-info user-info_inline"]})

                for user in users:
                    login = user["data-user-login"]
                    if login not in res:
                        res[login] = 0
                    res[login] += 1
                result[link] = res
    except:
        return

async def get_all_statistic(link):


if __name__ == '__main__':
    filename = 'top_user_comments.csv'
    links = sys.argv[1:4]

    main(filename, links)
