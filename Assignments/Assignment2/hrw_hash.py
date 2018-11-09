import math
import sys
from Helpers.get_hash import hashit
from Helpers.csv_parser import csv_line_dict
from Client.client import Client

class HRW_Hash():
    
    def __init__(self , num_replicas=3):
        nodes = self.generate_nodes(num_replicas)
        hnodes = [hashit(node) for node in nodes]
        hnodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hnodes
        self.nodes_map = {hashit(node): node.split("-")[1] for node in nodes}

    @staticmethod
    def generate_nodes(num_replicas):
        nodes = []
        for i in range(num_replicas):
            for server in servers:
                nodes.append("{0}-{1}".format(i, server))
        return nodes

    @staticmethod
    def merge_hashes(key_hash, node_info):
        return ((key_hash | 1) * (node_info | 1)) % 2**64

    def get_node(self, val):
        key_hash = hashit(val)
        annotated = [(self.merge_hashes(key_hash, hnode), self.nodes_map[hnode]) for hnode in self.hnodes]
        ordered = sorted(annotated)
        return [host for _, host in ordered[:1]][0]
    

def send_requests():
    for server in servers:
        connections[server] = Client(server)
    ring = HRW_Hash()
    data = csv_line_dict(csv_file_name)
    count = 0
    for key, value in data:
        if connections[ring.get_node(key)].send_entry(dict([(str(hashit(key)), value)])) == 200:
            count += 1
    print('Uploaded all %s entries.' %count)
    
    print('Verifying the data.')
    for connection in connections.values():
        connection.get_entries()

csv_file_name = 'causes-of-death.csv'
connections = {}
servers = ['http://localhost:5000','http://localhost:5001','http://localhost:5002', 'http://localhost:5003']

def main():
    if len(sys.argv) > 1:
        csv_file_name = sys.argv[1]
    send_requests()

if __name__ == "__main__":
    main()