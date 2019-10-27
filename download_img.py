import asyncio
import os
import random
import async_timeout
import aiohttp
import aiofiles

folder = "images"


async def download_img(session, url):
    try:
        async with session.get(url, ssl=True) as response:
            if response.status == 200:
                alphabet = '123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
                img_name = ''.join([random.choice(list(alphabet)) for x in range(6)])
                file_name = "{}.jpg".format(img_name)
                file_path = os.path.join(folder, file_name)
                #print(img_name, url)

                f = await aiofiles.open(file_path, mode='wb')
                await f.write(await response.read())
                await f.close()
    except:
        print("TimeoutError", url)


async def main(loop, urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        tasks = [download_img(session, url) for url in urls]
        await asyncio.gather(*tasks)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def fetch_imgs(urls):
    loop.run_until_complete(main(loop, urls))
