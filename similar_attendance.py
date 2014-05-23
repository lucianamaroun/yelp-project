""" Friendship graph with overlap of business attendance information. """

import read_json_data as reader
import random
import itertools as itools
import networkx as nx


_THRESHOLD = 0.25


def users_attendance(users, reviews):
  attendance = {}
  for review in reviews:
    user_id = review['user_id']
    if user_id not in attendance:
      attendance[user_id] = set()
    attendance[user_id].add(review['business_id'])
  return attendance


def friends_relative_overlaps(graph, users, attendance):
  relative_overlaps = []
  for user_a in graph:
    for user_b in [u for u in graph[user_a] if u > user_a]:
      intersection = len(attendance[user_a].intersection(attendance[user_b]))
      union = len(attendance[user_a].union(attendance[user_b]))
      relative_overlap = float(intersection) / union
      relative_overlaps.append(relative_overlap)
  return relative_overlaps


def create_random_graph(graph):
  new_graph = nx.Graph()
  new_graph.add_nodes_from(graph.nodes())
  new_graph.add_edges_from(random.sample([(a, b) for (a, b) in
    itools.(graph.nodes(), graph.nodes()) if a != b],
    graph.number_of_edges()))
  return new_graph


def random_relative_overlaps(graph, users, attendance):
  relative_overlaps = []
  for user_a in graph:
    random_edges = len([u for u in graph[user_a] if u > user_a])
    population = graph.nodes()
    population.remove(user_a)
    for user_b in random.sample(population, random_edges):
      intersection = len(attendance[user_a].intersection(attendance[user_b]))
      union = len(attendance[user_a].union(attendance[user_b]))
      relative_overlap = float(intersection) / union
      relative_overlaps.append(relative_overlap)
  return relative_overlaps
      

def label_edges(graph, users, attendance):
  relative_overlaps = []
  count_ones = 0
  for user_a in graph:
    for user_b in [u for u in graph[user_a] if u > user_a]:
      intersection = len(attendance[user_a].intersection(attendance[user_b]))
      union = len(attendance[user_a].union(attendance[user_b]))
      relative_overlap = float(intersection) / union
      relative_overlaps.append(relative_overlap)
      graph[user_a][user_b]['attendance_sim'] = 1 if relative_overlap > \
          _THRESHOLD else 0
      if graph[user_a][user_b]['attendance_sim']:
        count += 1
  return relative_overlaps, count


def main():
  users = reader.read_users()
  reviews = reader.read_reviews()
  graph = reader.read_graph()
  attendance = users_attendance(users, reviews)
  friends_overlaps = friends_relative_overlaps(graph, users, attendance)
  random_graph = create_random_graph(graph)
  random_overlaps = random_relative_overlaps(random_graph, users, attendance)
  friends_out = open('friends_overlaps.txt', 'w')
  for overlap in friends_overlaps:
    print >> friends_out, _overlap
  out_overlaps.close()
  random_out = open('random_overlaps.txt', 'w')
  for overlap in random_overlaps:
    print >> random_out, overlap
  random_out.close()


if __name__ == '__main__':
  main()
