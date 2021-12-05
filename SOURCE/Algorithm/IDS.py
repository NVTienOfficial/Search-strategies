import typing
import os
from Problem import Problem
from Node import Node
from State import State
from Solution import Solution
from queue import Queue

def Iterative_deeping_Search(problem: Problem) -> Solution:
    '''Iterative deepening search algorithm with depth is from 0 to N*N'''
    for depth in range(0, problem.N*problem.N):
        result, node, expand = Depth_limited_Search(problem, depth)
        if result != -1:    # valid solution is found if result != cutoff
            return Solution(expand, problem.path(node))

    return None

def Depth_limited_Search(problem: Problem, max_depth: int) -> typing.Tuple[int, Node, list]:
    '''Depth limited search algorithm'''
    # initial state
    node = Node(state=State.generateState(problem.initial, problem.N))

    # frontier
    frontier = Queue()
    frontier.put(node)

    # list of expanded state for solution
    expand = []

    while not frontier.empty():
        # frontier pops the first element
        node = frontier.get()
        s = node.state.getIndex(problem.N)
        
        # add to expand nodes
        if s not in expand:
            expand.append(s)
        
        # check if current state is goal state or not
        if problem.isGoal(s):
            return 1, node, expand

        # if node's depth is bigger than max_depth, return cutoff
        if problem.depth(node) > max_depth:
            return -1, None, expand
        elif not problem.isCycle(node):
            # no cycle then generate child nodes of current node
            for child in problem.successor(node):
                frontier.put(child)

    return 0, None, expand