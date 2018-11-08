import http.client
import json
import sys
import re
import csv_parser
import get_hash
from hrw_hash import HRW_Hash

class client():
    def __init__(self, host):
        self.host = host
        self.headers = {'Content-type': 'application/json'}
        p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        m = re.search(p,host)
        self.connection = http.client.HTTPConnection(m.group('host'), m.group('port'))

    def send_entry(self, data):
        self.connection.request('POST', '/api/v1/entries', json.dumps(data), self.headers)
        response = self.connection.getresponse()
        return response.code
    
    def get_entries(self):
        self.connection.request('GET', '/api/v1/entries')
        response = self.connection.getresponse()
        
        print(json.dumps(response.read().decode(), sort_keys=True, indent=4))

def main():
    if len(sys.argv) > 1:
        csv_file_name = sys.argv[1]
    
    getconnections()
    send_requests()

def getconnections():
    for server in servers:
        connections[server] = client(server)


def send_requests():
    ring = HRW_Hash(servers)
    data_dict = csv_parser.parsetodict(csv_file_name)
    count = 0
    for key, value in data_dict.items():
        if connections[ring.get_node(key)].send_entry(dict([(str(get_hash.hash(key)), value)])) == 200:
            count += 1
    print('Uploaded all %s entries.' %count)
    print('Verifying the data.')
    for connection in connections.values():
        connection.get_entries()


csv_file_name = 'causes-of-death.csv'
connections = {}        
servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002', 'http://localhost:5003']


if __name__ == "__main__":
    main()