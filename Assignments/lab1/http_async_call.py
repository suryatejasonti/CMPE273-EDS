# importing the requests library
import requests
import asyncio
import sys

# api-endpoint
#URL = "https://webhook.site/49279164-074f-4a1a-a875-1ee55b7c1560"
async def async_call(URL):    
    r = requests.get(url = URL)
    if r.status_code == 200:
        print(r.headers['Date'])

async def main(URL):
    await asyncio.gather(
        async_call(URL),
        async_call(URL),
        async_call(URL),
    )  

if __name__ ==  '__main__':
    if len(sys.argv) > 0:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(sys.argv[1]))