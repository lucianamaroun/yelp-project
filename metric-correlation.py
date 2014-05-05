""" Calculates the correlation between a metric and the usefulness of a
    reviewer.
"""

import networkx
import scipy

import graph
import read


def calculate_usefulness(reviews):
  useful = {}
  for review in reviews:
    if review['user_id'] not in useful:
      useful[review['user_id']] = 0
    useful[review['user_id']] += reviews['votes']['useful']
  return useful


def calculate_metric(graph):
  metric = {}
  for node in graph:
    metric[node] = networkx.closeness_centrality(graph, node)
  return metric


def get_vectors(useful, metric):
  useful_vec = []
  metric_vec = []
  mapping = []
  for node in graph:
    mapping.append(node)
    useful_vec.append(useful[node])
    metric_vec.append(metric[node])
  return mapping, useful_vec, metric_vec    


def calculate_correlation():
  reviews = read.get_reviews()
  useful = calculate_usefulness(reviews)
  graph = graph.load_graph()
  metric = calculate_metric(graph)
  mapping, u_vec, m_vec = get_vectors(useful, metric)
  return scipy.stats.stats.pearsonr(u_vec, m_vec)


if __name__ == '__main__':
  print calculate_correlation()
