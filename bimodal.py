""" Module with bimodal analysis of the network. In this analysis, the nodes are
    considered demanding or not according to the average rating they give.
"""

import json
import networkx as nx
import graphutil as gu


def label_graph_nodes(graph):
  """ Add labels to graph nodes, which represent users, according to the rating
      characteristic.

  Observations:
    - If the user has average degree less than 2.5, than it is considered
      demanding and receive -1 label. Otherwise, they are easygoing and receive
      a 1 label.
    - The method does not retrieve anything, modifying the graph in place.

  Args:
    graph: the graph whose nodes are to be labeled.

  Returns:
    None.
  """
  user_str = open(gu.USER_JSON, 'r').read()
  users = json.loads(user_str)
  for user in users:
    graph.node[user['user_id']]['class'] = 1 if user['average_stars'] >= 2.5 \
      else -1


if __name__ == '__main__':
  print 'Loading graph...'
  graph = gu.load_graph()
  print 'Labeling graph...'
  label_graph_nodes(graph)
  print 'Calculating assortativity...'
  print nx.attribute_assortativity_coefficient(graph, 'class')
