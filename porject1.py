# -*- coding: utf-8 -*-
"""
This is porject 1
"""

EX_GRAPH0 = {0:set([1,2]),1:set([]),2:set({})}
EX_GRAPH1 = {0:set([1,4,5]),1:set([2,6]),2:set([3]),3:set([0]),4:set([1]),5:set([2]),6:set([])}
EX_GRAPH2 = {0:set([1,4,5]),1:set([2,6]),2:set([3,7]),3:set([7]),4:set([1]),5:set([2]),6:set([]),7:set([3]),8:set([1,2]),9:set([0,3,4,5,6,7])}


def make_cimplete_graph(num_nodes):
    """
    This function takes a number and returns a complete graph with that number of nodes
    """
    result = dict([(currentNode,[linkedNode for linkedNode in range(num_nodes) if linkedNode != currentNode]) for currentNode in range(num_nodes)])

    return result


def compute_in_degrees(digraph):
    """
    This function takes a digraph and returns a dictionary with the nodes and each of their own in degrees
    """
    result = dict([(key, sum(key in digraph[nodes] for nodes in digraph)) for key in digraph])

    return result 



def in_degree_distribution(digraph):
    """
    This function takesa digraph and returns the distribution of in degrees of the digraph
    """

    result,in_degrees = {},[]
    degrees = compute_in_degrees(digraph)

    for key in degrees:
        in_degrees.append(degrees[key])
    for num in in_degrees:
        result[num] = in_degrees.count(num)

    return result 

