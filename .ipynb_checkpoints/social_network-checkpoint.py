import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

def load_graph():

    D = nx.read_weighted_edgelist('data/higgs-social_network.edgelist.gz', create_using=nx.DiGraph)
    print("loaded graph")
    degrees = [n.degree for n in D.nodes]
    plt.hist(degrees,log=True)


if __name__ == "__main__":

    load_graph()
