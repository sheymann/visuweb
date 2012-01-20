# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Construit le graphe égocentré d'un noeud.

Requires Python 2.7
"""
#    Copyright (C) 2011 by
#    Sébastien Heymann <sebastien.heymann@lip6.fr>
#    All rights reserved.
#    BSD license.

import tornado.escape
import gevent
from gevent import monkey ; monkey.patch_all()
import json
import random
import re
from time import sleep
#from networkx.readwrite import json_graph
import networkx as nx

from logger import Logger
from lookup import Lookup
from config import CONFIG


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]


class GraphBuilder:
    def __init__(self):
        self.__logger__ = Logger(self.__class__.__name__)
    
    def __getCanonicalNode__(self, neighbors_tmp, node):
        #print neighbors_tmp
        cname = re.sub('^https?://','',node.lower())
        name = "http://" + cname
        if neighbors_tmp["canonical_mapping"].has_key(name):
            return neighbors_tmp["canonical_mapping"][name]
        else:
            return neighbors_tmp["canonical_mapping"][cname]

    def __getNeighbors__(self, node):
        json = "{}"
        try:
            json = Lookup().fetchNode(tornado.escape.url_escape(node))
        except Exception, e:
            self.__logger__.error(str(e))
        return tornado.escape.json_decode(json)
    
    def build(self, node):
        G = nx.DiGraph()
        G.add_node(node)
        node = node.lower()
        neighbors_tmp = self.__getNeighbors__(node)
        if not neighbors_tmp.has_key("canonical_mapping"):
            return G
        
        cnode = self.__getCanonicalNode__(neighbors_tmp, node)
        neighbors = neighbors_tmp["nodes"][cnode]["nodes_referenced_by"].keys()
        #neighbors.extend(neighbors_tmp["nodes"][cnode]["nodes_referenced"].keys())
        #print neighbors
        G.add_nodes_from(neighbors)
        
        chunkedNeighbors = list(chunks(neighbors, CONFIG.parallel_jobs))
        for c in chunkedNeighbors:
            jobs = [gevent.spawn(self.__getNeighbors__, node) for node in c]
            gevent.joinall(jobs, timeout=120)  # 2min timeout
            for job in jobs:
                if job:
                    if job.value:
                        if job.value.has_key("nodes"):
                            for n in job.value["nodes"].keys():
                                [G.add_edge(source, n) for source in job.value["nodes"][n]["nodes_referenced_by"].keys() if G.has_node(source)]
            sleep(0.5)
        return G


class GraphUtils:
    def write_gexf(self, graph, filename):
        nx.write_gexf(graph, filename)
    
#    def write_json(self, graph, filename): TODO upgrade networkx to 1.6rc1
#        with open(filename, "wb") as f:
#            data = json_graph.node_link_data(graph)
#            s = json.dumps(data)
#            f.write(s)

#    def compute_metrics(self, graph):
#        


if __name__ == "__main__":
    builder = GraphBuilder()
    graph = builder.build("twitter.com/jacomyal")
    GraphUtils().write_gexf(graph, "twitter_com_jacomyal.gexf")

