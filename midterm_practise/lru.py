from functools import lru_cache
from urllib.request import urlopen
from urllib.error import HTTPError

@lru_cache(maxsize=32)
def get_pep(num):
    'Retrieve text of a Python Enhancement Proposal'
    resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
    try:
        with urlopen(resource) as s:
            return s.read()
    except HTTPError:
        return 'Not Found'

if __name__ == '__main__':
    for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991, 8:
        pep = get_pep(n)
        print(n, len(pep))
    print(get_pep.cache_info())