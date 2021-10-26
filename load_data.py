import networkx as nx
import gzip
import json
import matplotlib.pyplot as plt

# out = nx.read_edgelist('data/higgs-retweet_network.edgelist.gz')
# print(type(out))

with gzip.open('data/higgs-retweet_network.edgelist.gz','rt') as f:

    edges = []
    for line in f.readlines():
        edges.append([int(i) for i in line.strip().split()])


D = nx.DiGraph()
D.add_weighted_edges_from(edges)

print(len(D))
components = list(nx.strongly_connected_components(D))
components = [c for c in components if len(c) >1 ]
subgraphs = [D.subgraph(c) for c in components]
sizes = [len(c) for c in components]
tree_status = [nx.is_tree(c) for c in subgraphs]

# for s in subgraphs[:10]:
#     nx.draw(s)
#     plt.show()

print(tree_status)
sizes = [s for s in sizes if s<100]
plt.hist(sizes,bins = 100,log=True)

plt.show()

