import math
import get_hash

class HRW_Hash():
    
    def __init__(self, server_list, num_replicas=3):
        nodes = self.generate_nodes(server_list, num_replicas)
        hnodes = [get_hash.hash(node) for node in nodes]
        hnodes.sort()

        self.num_replicas = num_replicas
        self.nodes = nodes
        self.hnodes = hnodes
        self.nodes_map = {get_hash.hash(node): node.split("-")[1] for node in nodes}

    @staticmethod
    def generate_nodes(server_list, num_replicas):
        nodes = []
        for i in range(num_replicas):
            for server in server_list:
                nodes.append("{0}-{1}".format(i, server))
        return nodes

    @staticmethod
    def merge_hashes(key_hash, node_hash):
        return ((key_hash | 1) * (node_hash | 1)) % 2**64

    def get_node(self, val):
        key_hash = get_hash.hash(val)
        annotated = [(self.merge_hashes(key_hash, hnode), self.nodes_map[hnode]) for hnode in self.hnodes]
        ordered = sorted(annotated)
        print([host for _, host in ordered[:1]][0])
        return [host for _, host in ordered[:1]][0]
    