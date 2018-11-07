import http.client
import json
from bisect import bisect
from hashlib import md5
import sys
import re
import csv_parser


class Ring():
    
    def __init__(self, server_list, num_replicas=3):
        nodes = self.generate_nodes(server_list, num_replicas)
        hnodes = [self.hash(node) for node in nodes]
        hnodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hnodes
        self.nodes_map = {self.hash(node): node.split("-")[1] for node in nodes}
    
    @staticmethod
    def hash(val):
        m = md5(val.encode())
        return int(m.hexdigest(), 16)

    @staticmethod
    def generate_nodes(server_list, num_replicas):
        nodes = []
        for i in range(num_replicas):
            for server in server_list:
                nodes.append("{0}-{1}".format(i, server))
        return nodes

    def get_node(self, val):
        pos = bisect(self.hnodes, self.hash(val))
        if pos == len(self.hnodes):
            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]
    


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

def hash(val):
        m = md5(val.encode())
        return int(m.hexdigest(), 16)

def send_requests():
    ring = Ring(servers)
    data_dict = csv_parser.parsetodict(csv_file_name)
    for key, value in data_dict.items():
        connections[ring.get_node(key)].send_entry(dict([(str(hash(value)), value)]))

    for connection in connections.values():
        connection.get_entries()


csv_file_name = 'causes-of-death.csv'
connections = {}        
servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002', 'http://localhost:5003']


if __name__ == "__main__":
    main()