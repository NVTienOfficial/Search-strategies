from typing import Dict, List
from Node import Node
from State import State
from Solution import Solution

class Problem:
    '''

    Problem find a path from a state to goal in a maze NxN
    
    '''

    # Constructors
    def __init__(self, N:int = 0, adjacency = [], initial:int = 0, goal:int = 0) -> None:
        self.N = (int)(N)
        self.transition_model = self.createTransModel(adjacency)
        self.initial = initial
        self.goal = goal

    # Valid functions
    def isGoal(self, state: int) -> bool:
        '''Check if the current state is goal state or not'''
        if state == self.goal:
            return True;
        return False;

    def validAction(action:str) -> bool:
        '''Check if action is up(u), down(d), left(l), or right(r)'''
        action = action.lower()
        if action == 'u' or action == 'd' or action == 'l' or action == 'r':
            return True;
        return False;

    # Functions
    def result(self, node:Node, action:str) -> Node:
        '''Current node receives an action to generate a next node'''
        model = self.transition_model[node.state.getIndex()]         # transition model for current node (a dictionary)

        # Execute action
        new_index = model[action]

        # Check action valid or not
        if new_index ==  None:
            return None     # node do not receive action

        state = State.generateState(new_index, self.N)              
        return Node(state=state, parent=node, action=action, path_cost=1)

    def successor(self, parent: Node) -> List[Node]:
        '''Returns all successor node of parent node passed'''
        key = parent.state.getIndex(self.N)
        model = self.transition_model.get(key)         # transition model of parent node

        childs = []
        for index, action in model.items():
            state = State.generateState(index, self.N)
            node = Node(state=state, parent=parent, action=action, path_cost=1+parent.path_cost)
            childs.append(node)

        childs.sort()

        return childs

    def action(self, state:State) -> List[str]:
        '''Returns possible actions for the input state'''
        return self.transition_model[state.getIndex()].values()

    def path(self, node:Node) -> List[int]:
        '''Funtion return path from a node to initial node'''
        if node == None:
            return []
        route = [node.state.getIndex(self.N)]
        tmp = node
        while tmp.parent != None:
            tmp = tmp.parent
            route.append(tmp.state.getIndex(self.N))
        route.reverse()
        return route

    def depth(self, node: Node) -> int:
        '''Return depth of current node from root node'''
        d = 0
        while node.parent != None:
            d += 1
            node = node.parent
        return d

    def isCycle(self, node: Node) -> bool:
        '''Check if path from root node to current node contains cycle or not'''
        tmp = node
        s = node.state.getIndex(self.N)
        while tmp.parent != None:
            tmp = tmp.parent
            if tmp.state.getIndex(self.N) == s:
                return True
        return False

    # Initialization model
    def createTransModel(self, adjacency:List) -> dict[int, dict[int, str]]:
        '''Returns transition model as a dictionary with:
            + Key: index of state
            + Value: a dictionary with: - Key:   state that key state receive action to generate
                                        - Value: action
        '''
        models = {}         # Transition model for problem

        index = 0
        for adj in adjacency:               # Loop all state
            model = {}                      # transition model for each state
            for i in adj:                   # loop all next state
                action = self.getAction(index, i)
                model[i] = action
            models[index] = model
            index += 1

        return models

    # Another functions
    def getAction(self, parent:int, child:int) -> str:
        '''Returns action(u, d, l, r) from 2 index'''

        p_col = parent // self.N
        p_row = parent % self.N
        c_col = child // self.N
        c_row = child % self.N

        d_col = c_col - p_col
        d_row = c_row - p_row

        if d_col == 0 and d_row == -1:
            return "u"
        elif d_col == 0 and d_row == 1:
            return "d"
        elif d_col == -1 and d_row == 0:
            return "l"
        elif d_col == 1 and d_row == 0:
            return "r"

        return None