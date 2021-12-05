from Problem import Problem
from State import State
from Solution import Solution
from Node import Node
from queue import PriorityQueue

def Uniform_cost_Search(problem:Problem) -> Solution:
    '''Uniform-cost search algorithm''' 

    # initial state
    state = State.generateState(problem.initial, problem.N)
    node = Node(state=state)

    # check if initial state is goal state or not
    if problem.isGoal(state.getIndex(problem.N)):
        return Solution([node], [node])

    # create frontier
    frontier = PriorityQueue()
    frontier.put((0, node))

    reached = {}    # list of explored node for algorithm  {state: node}
    expand = []     # list of state for solution

    while not frontier.empty():
        # frontier pop first element
        node = frontier.get()[1]
        state = node.state
        s = state.getIndex(problem.N)

        # add state to expand if not exists
        if s not in expand:
            expand.append(s)

        # check current state is goal state or not
        if problem.isGoal(state.getIndex(problem.N)):
            return Solution(expand, problem.path(node))

        # generate child nodes of current node
        for child in problem.successor(node):
            state = child.state
            s = state.getIndex(problem.N)
            if (s not in reached) or (child.path_cost < reached[s].path_cost):
                reached[s] = child
                frontier.put((child.path_cost, child))
        
    return Solution(expand, [])