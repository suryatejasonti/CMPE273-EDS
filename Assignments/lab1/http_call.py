# importing the requests library
import requests
import sys

# api-endpoint
#URL = "https://webhook.site/49279164-074f-4a1a-a875-1ee55b7c1560"

def sync_call(URL):
    r = requests.get(url = URL)
    if r.status_code == 200:
        print(r.headers['Date'])

if __name__ == "__main__":
    if len(sys.argv) != 0:
        for _ in range(3):
            sync_call(sys.argv[1])