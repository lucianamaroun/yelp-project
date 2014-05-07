""" Calculates the correlation between a metric and the usefulness of a
    reviewer.
"""

import networkx
import scipy.stats
import pickle
import os

import graph
import read


def calculate_usefulness(users):
  useful = {}
  for user in users:
    useful[user['user_id']] = user['votes']['useful']
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
  vecfile = open('pairs.csv', 'w')
  for node in useful:
    mapping.append(node)
    useful_vec.append(useful[node])
    metric_vec.append(metric[node])
    print >> vecfile, str(useful[node]) + ',' + str(metric[node])
  return mapping, useful_vec, metric_vec 


def calculate_correlation():
  print 'Reading users'
  users = read.get_users()
  print 'Calculating usefulness'
  useful = calculate_usefulness(users)
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
