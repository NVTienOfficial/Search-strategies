from State import State

class Node:
    '''
    
    This class represents a node (case) in maze
    
    '''

    # Constructors    
    def __init__(self, state:State = State(0,0), parent = None, action:str = "", path_cost:int = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        if self.state.col < other.state.col:
            return True
        elif self.state.col == other.state.col:
            if self.state.row < other.state.row:
                return True
            else:
                return self.path_cost < other.path_cost
        else:
            return False