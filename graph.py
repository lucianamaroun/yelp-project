""" Friendship graph statistics of the Yelp dataset """

import networkx as nx
import json
import pickle
import os


USER_JSON = 'data/yelp_academic_dataset_user.json'
USER_PKL = 'user_graph.pkl'


def paths_length_two(graph):
  """ Counts the number of paths with length two in the graph.

  Args:
    graph: the networkx.Graph() object.

  Returns:
    An integer representing the number of length two paths.
  """
  count = 0
  for node1 in graph.nodes_iter():
    for node2 in graph[node1]: 
      count += len([node for node in graph[node2] if node > node1]) 
        # the lexicographical order is to avoid repetition
  return count 


def average_degree(graph):
  """ Calculates the average degree of the graph.

  Args:
    graph: the networkx.Graph() object.

  Returns:
    A float representing average degree.
  """
  return sum([graph.degree(node) for node in graph.nodes_iter()]) / \
    float(graph.number_of_nodes())


def load_graph():
  """ Loads the users graph from the users' json file.

  Observations:
    - The users json file is a static parameter of the algorithm, defined in the
      top of this file.
    - The nodes' id are interpreted as strings.

  Args:
    None.

  Returns:
    A networkx.Graph() object.
  """
  user_str = open(USER_JSON, 'r').read()
  users = json.loads(user_str)

  if os.path.exists(USER_PKL):
    pkl_file = open(USER_PKL, 'r')
    graph = pickle.load(pkl_file)
    pkl_file.close()
  else:
    graph = nx.Graph()
    for user in users:
      graph.add_node(user['user_id'])
      for friend in user['friends']:
        graph.add_edge(user['user_id'], friend)
    pkl_file = open(USER_PKL, 'w')
    pickle.dump(graph, pkl_file)
    pkl_file.close()

  return graph


def print_statistics(graph):
  """ Prints in the standard output basic statistics of the graph.

  Args:
    graph: the networkx.Graph() object.

  Returns:
    None.
  """
  n_nodes = graph.number_of_nodes()
  n_edges = graph.number_of_edges()
  total_triangles = sum(nx.triangles(graph).values()) / 3
  components = nx.connected_component_subgraphs(graph)
  lcc = components[0]
  print '# nodes: %d' % n_nodes
  print '# non-isolated nodes: %d' % len([node for node in graph.nodes_iter() if
    graph.degree(node) > 0])
  print '# edges: %d' % n_edges
  print 'clustering coefficient: %.2f' % nx.average_clustering(graph)
  print 'average degree: %.2f' % average_degree(graph)
  print '%% nodes in LCC: %.2f%%' % (lcc.number_of_nodes() / float(n_nodes) * 100)
  print '# components: %d' % len(components)
  print '# triangles: %d' % total_triangles
  print '%% closed triangles: %.2f%%' % (float(total_triangles) / \
    paths_length_two(graph) * 100) 


def main():
  """Main function."""
  graph = load_graph()
  print_statistics(graph)


if __name__ == '__main__':
  main()

