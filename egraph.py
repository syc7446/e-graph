#!/usr/bin/env python 
import networkx as nx
from networkx import DiGraph
import math
import matplotlib.pyplot as plt
from Visualize import plot

class EGraph():
	def __init__(self, G, eG, initial_state, accept_state, eps, eps_h):
		self.G = G
		self.eG = eG # Egraph
		self.initial_state = initial_state
		self.accept_state = accept_state
		self.eps = eps
		self.eps_h = eps_h

		self.ComputePath()

	def ComputePath(self):
		open_set = {}
		closed_set = {}
		g = {}
		f = {}
		visited_state_set = []

		g[self.initial_state] = 0
		f[self.initial_state] = self.eps*nx.dijkstra_path_length(self.G,self.initial_state,self.accept_state,self.MakeWeightFn)
		open_set[self.initial_state] = f[self.initial_state]
		visited_state_set.append(self.initial_state)

		while True:
			min_f = min(f.values())
			cur_state = [state for state in f if f[state] is min_f]
			cur_state = cur_state[0]
			print("cur_state = ", cur_state)
			del open_set[cur_state]
			closed_set[cur_state] = f[cur_state]
			del f[cur_state]

			if cur_state is self.accept_state:
				break

			succ_state_set = self.G.succ[cur_state].keys()

			for succ_state in succ_state_set:
				print("succ_state = ", succ_state)
				# Check if there exists a path from succ_state to accept_state.
				if not nx.has_path(self.G,succ_state,self.accept_state):
					continue

				if not self.IsVisited(succ_state,visited_state_set):
					g[succ_state] = float("inf")
					f[succ_state] = float("inf")

				cost = self.GetCost(cur_state,succ_state)
				if g[succ_state] > g[cur_state]+cost and not self.IsClosed(succ_state,closed_set):
					g[succ_state] = g[cur_state]+cost
					f[succ_state] = g[succ_state]+self.eps*nx.dijkstra_path_length(self.G,succ_state,self.accept_state,self.MakeWeightFn)
					open_set[succ_state] = f[succ_state]
				visited_state_set.append(succ_state)
				print("g[] = ", g[succ_state])
				print("f[] = ", f[succ_state])

		print("closed_set = ", closed_set)

	def MakeWeightFn(self,u, v, d): # This nees to talk to the behavior tree.
		if self.eG.has_edge(u,v):
			# Change this part later so that we request the bahavior tree to compute self.G.edges[u,v]['heuristic'] online.
			return min(self.eps_h*self.G.edges[u,v]['heuristic'], self.eG.edges[u,v]['weight'])
		else:
			return self.eps_h*self.G.edges[u,v]['heuristic']

	def IsVisited(self, succ_state, visited_state_set):
		for i in range(0,len(visited_state_set)):
			if visited_state_set[i] is succ_state:
				return True
		return False

	def GetCost(self, u, v): # This nees to talk to the behavior tree.
		return self.G.edges[u,v]['weight']

	def IsClosed(self, state, closed_set):
		if state in closed_set:
			return True
		else:
			return False

if __name__ == '__main__':
	'''
	Input: G (weights, heuristics), eG
	Output: eG, phi
	'''
	G = DiGraph()
	G.add_node('a')
	G.add_node('b')
	G.add_node('c')
	G.add_node('d')
	G.add_edge('a', 'b', weight=2., heuristic=1.)
	G.add_edge('b', 'c', weight=2., heuristic=1.)
	G.add_edge('c', 'd', weight=2., heuristic=1.)
	G.add_edge('a', 'd', weight=8., heuristic=3.)
	plot(G,"test_graph")
	eG = DiGraph()
	eG.add_node('a')
	eG.add_node('d')
	eG.add_edge('a', 'd', weight=8., heuristic=1.)
	
	EGraph(G, eG, 'a', 'd', 1., 10.)
	
	# Draw the graph.
	# plt.subplot(121)
	# nx.draw(G)
	# plt.subplot(122)
	# nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')
	# plt.show()
