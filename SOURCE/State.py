class State:
    '''
    
    This class the current position of robot in the maze with row-col coordinate
    
    '''
    
    # Constructors
    def __init__(self, col:int = 0, row:int = 0) -> None:
        self.col = col
        self.row = row
        
    def getIndex(self, N:int) -> int:
        '''Return index of coordinate (col, row)'''
        return self.col * N + self.row
        
    def generateState(index:int, size:int):
        '''Return a state by calculate coordinate (col, row) from index and size of maze'''
        col = index // size
        row = index % size
        return State(col=col, row=row)