""" Calculates the correlation between a metric and the usefulness of a
    reviewer.
"""

import networkx
import scipy.stats
import pickle
import os

import graph
import read


def calculate_usefulness(reviews):
  useful = {}
  for review in reviews:
    if review['user_id'] not in useful:
      useful[review['user_id']] = 0
    useful[review['user_id']] += review['votes']['useful']
  return useful


def calculate_metric(graph):
  metric = {}
  if os.path.exists('closeness.pkl'):
    dump = open('closeness.pkl', 'r')
    return pickle.load(dump)
  for node in graph:
    metric[node] = networkx.closeness_centrality(graph, node)
  dump = open('closeness.pkl', 'w')
  pickle.dump(metric, dump)
  return metric


def get_vectors(useful, metric):
  useful_vec = []
  metric_vec = []
  mapping = []
  for node in useful:
    mapping.append(node)
    useful_vec.append(useful[node])
    metric_vec.append(metric[node])
  return mapping, useful_vec, metric_vec 


def calculate_correlation():
  print 'Reading reviews'
  reviews = read.get_reviews()
  print 'Calculating usefulness'
  useful = calculate_usefulness(reviews)
  print 'Reading graph'
  reviewers_graph = graph.load_graph()
  print 'Calculating centrality'
  metric = calculate_metric(reviewers_graph)
  print 'Getting vectors'
  mapping, u_vec, m_vec = get_vectors(useful, metric)
  print 'Calculating correlation'
  return scipy.stats.pearsonr(u_vec, m_vec)


if __name__ == '__main__':
  print calculate_correlation()
