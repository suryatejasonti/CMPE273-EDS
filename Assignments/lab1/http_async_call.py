import asyncio
import concurrent.futures
import requests
import sys

async def async_call():
    number_hits = 3
    with concurrent.futures.ThreadPoolExecutor(max_workers=number_hits) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                requests.get, 
                sys.argv[1]
            )
            for i in range(number_hits)
        ]
        for response in await asyncio.gather(*futures):
                if response.status_code == 200:
                    print(response.headers['Date'])

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_call())