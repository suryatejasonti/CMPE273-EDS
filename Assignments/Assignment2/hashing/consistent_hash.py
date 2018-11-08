from bisect import bisect
import get_hash


class Consistent_Hash():
    
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

    def get_node(self, val):
        pos = bisect(self.hnodes, get_hash.hash(val))
        if pos == len(self.hnodes):
            return self.nodes_map[self.hnodes[0]]
        else:
            return self.nodes_map[self.hnodes[pos]]