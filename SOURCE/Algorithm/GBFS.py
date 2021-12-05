from Problem import Problem
from Node import Node
from State import State
from Solution import Solution
from queue import PriorityQueue

def Greedy_best_first_Search(problem: Problem) -> Solution:
    '''Graph search: Greedy best-first search algorithm with Manhattan distancs as heuristic'''
    # goal state
    sGoal = State.generateState(problem.goal, problem.N)

    # initial state
    state = State.generateState(problem.initial, problem.N)
    node = Node(state=state)

    # check if initial state is goal state or not
    if problem.isGoal(state):
        return Solution([], problem.path(node))

    # frontier
    frontier = PriorityQueue()
    frontier.put((Manhattan_distance(state, sGoal), node))

    # list of exanded nodes for solution
    expand = []

    while not frontier.empty():
        # frontier pops first element
        node = frontier.get()[1]
        s = node.state.getIndex(problem.N)
        
        # add state to expand
        if s not in expand:
            expand.append(s)

        # generate child nodes of current node
        for child in problem.successor(node):
            state = child.state
            # early check current node is goal or not
            if problem.isGoal(state.getIndex(problem.N)):
                return Solution(expand, problem.path(child))
            # add to frontier
            if (state.getIndex(problem.N) not in expand):
                frontier.put((Manhattan_distance(state, sGoal), child))
        
    return Solution(expand, [])
                


def Manhattan_distance(pos: State, goal: State) -> int:
    '''Manhattan distance: |state.x - goal.x| + |state.y - goal.y|'''
    return abs(pos.row - goal.row) + abs(pos.col - goal.col)
