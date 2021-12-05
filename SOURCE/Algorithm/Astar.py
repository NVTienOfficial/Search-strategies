from queue import PriorityQueue
from Problem import Problem
from Node import Node
from State import State
from Solution import Solution
from Algorithm.GBFS import Manhattan_distance

def A_star_Search(problem: Problem) -> Solution:
    '''Graph search: A* search algorithm with Manhattan distance as heuristic'''
    # goal state
    sGoal = State.generateState(problem.goal, problem.N)

    # initial state
    state = State.generateState(problem.initial, problem.N)
    node = Node(state=state)
    s = state.getIndex(problem.N)

    # check if initial state if goal state or not
    if problem.isGoal(s):
        return Solution([node], [node])
    
    # frontier
    frontier = PriorityQueue()
    frontier.put((Manhattan_distance(state, sGoal), node))

    reached = {}        # list of explored nodes for algorithm  {state: node}
    expand = []         # list of expanded nodes for solution

    while not frontier.empty():
        # frontier pops first element
        node = frontier.get()[1]
        state = node.state
        s = state.getIndex(problem.N)

        # add to expand
        if s not in expand:
            expand.append(s)

        # check if current state is goal state or not
        if problem.isGoal(s):
            return Solution(expand, problem.path(node))

        # generate child nodes of current node
        for child in problem.successor(node):
            state = child.state
            s = state.getIndex(problem.N)
            fChild = evaluation(child, sGoal)

            # add to frontier
            if (s not in reached) or (fChild < evaluation(reached[s], sGoal)):
                reached[s] = child
                frontier.put((fChild, child))
    
    return Solution(expand, [])

def evaluation(node: Node, goal: State) -> int:
    '''f(n) = g(n) + h(n) = path_cost + Manhattan distance'''
    return Manhattan_distance(node.state, goal) + node.path_cost