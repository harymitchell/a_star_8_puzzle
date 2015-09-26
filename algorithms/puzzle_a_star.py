import heapq

class Board(object):
    def __init__(self, boardState):
        """
        Initialize new board

        """
        self.boardState = boardState
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        
    def boardStateString(self):
        string = ""
        for b in self.boardState:
            string += str(b)
            string += "\n"
        return string

class AStar(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.boards = []
        self.grid_height = 3
        self.grid_width = 3
        self.bCount = 1

    def init_grid(self):
        # start = [[7,2,4],#   I never waited for this one to finish,
        #          [5,0,6],#   if it is sovlable, my code is very inefficient, 
        #          [8,3,1]]#   defintely interested in some review.
        start  =[[4,2,8],  #
                 [6,1,3],  #  This one takes 17 moves, 20 seconds
                 [5,7,0]]  #
        end   = [[0,1,2],
                 [3,4,5],
                 [6,7,8]]
        self.start = Board(start)
        self.end = Board(end)
        self.boards.append (self.start)
        self.boards.append (self.end)
        self.bCount += 1
        #print "board count = " + str(self.bCount)
        print "start: \n" + self.start.boardStateString()
        print "end:   \n" + self.end.boardStateString()

    def get_heuristic(self, board):
        """
        Compute the heuristic value H for a board:
        Manhattan distance: for all tiles {abs(x_value - x_goal) + abs(y_value - y_goal)}

        @param board
        @returns heuristic value H
        """
        total = 0
        #print "board: \n" + board.boardStateString() 
        for r in range (self.grid_height):
            for c in range (self.grid_width):
                goal_r, goal_c = self.index_of_tile (self.end.boardState, board.boardState[r][c])
                tile_total = abs(r - goal_r) + abs(c - goal_c)
                total += tile_total
                #print "Tile " + str(board.boardState[r][c]) + " has H value of: " + str(tile_total)
        return total

    def is_solvable (self, board):
        """
        Is start a solvable board?
        """
        inversions = 0
        l = []
        for r in board.boardState:
            for c in r:
                if c > 0:
                    l.append (c)
        for i in l:
            for j in l:
                if i > j and l.index(i) < l.index(j):
                    inversions += 1
        print "inversions: " + str(inversions)
        if self.grid_width%2 == 1 and inversions%2 == 1:
            return False
        else:
            return True

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x][y]

    def index_of_free_tile (self, boardState):
        """
        Returns the x,y index of the free tile in board.

        Board example:
                 ((7, 2  ,4),
                 (5,0,6),
                 (8, 3  ,1))


        @param board is a 2D board state
        @returns the x and y index of the free tile in board
        """
        return self.index_of_tile (boardState, 0)

    def index_of_tile (self, boardState, tile):
        """
        Returns the x,y index of the free tile in board.
        
        @param boardState is a 2D board state
        @param tile is the value we are looking for
        @returns the x and y index of the free tile in board
        """
        for r in range(3):
            for c in range(3):
                if boardState[r][c] == tile:
                    return r, c
    
    def boardState_copy (self, boardState):
        """ Return a copy of boardState """
        return list(list(b) for b in boardState)

    def board_for_boardState (self, boardState):
        """
        Returns board or the cached version from self.boards.
        """
        for b in self.boards:
            if b.boardState == boardState:
                # print "found in cache"
                return b
        # New board
        board = Board (boardState)
        self.boards.append (board)
        self.bCount += 1
        #print "board count = " + str(self.bCount)
        return board

    def get_next_boards(self, board):
        """
        Returns all possible board states movable from board.

        @param board get all next board for this board
        @returns boards list 
        """
        boards = []
        free_row, free_column = self.index_of_free_tile (board.boardState)
        #print "board before: \n" + board.boardStateString()
        if free_column < self.grid_width-1:
            copy1 = self.boardState_copy (board.boardState)
            copy1[free_row][free_column] = board.boardState[free_row][free_column + 1]
            copy1[free_row][free_column + 1] = 0
            boards.append(self.board_for_boardState(copy1))
        if free_row > 0:
            copy2 = self.boardState_copy (board.boardState)
            copy2[free_row][free_column] = board.boardState[free_row - 1][free_column]
            copy2[free_row - 1][free_column] = 0
            boards.append(self.board_for_boardState(copy2))
        if free_column > 0:
            copy3 = self.boardState_copy (board.boardState)
            copy3[free_row][free_column] = board.boardState[free_row][free_column - 1]
            copy3[free_row][free_column - 1] = 0
            boards.append(self.board_for_boardState(copy3))
        if free_row < self.grid_height-1:
            copy4 = self.boardState_copy (board.boardState)
            copy4[free_row][free_column] = board.boardState[free_row + 1][free_column]
            copy4[free_row + 1][free_column] = 0
            boards.append(self.board_for_boardState(copy4))
        #print "get_next_boards board count = " + str(len(boards))
        #print "board: \n" + board.boardStateString()
        #for b in boards:
           #print "next: \n" + b.boardStateString()
        return boards

    def display_path(self):
        board = self.end
        count = 0
        print "path end: \n" + board.boardStateString()
        while board.parent and board.parent is not self.start:
            board = board.parent
            print "\n" + board.boardStateString()
            count += 1
        count += 1
        print "path start: \n" + self.start.boardStateString()
        print "total moves: " + str(count)
    
    def update_board(self, nextBoard, board):
        """
        Update nextBoard

        @param nextBoard next board from current board
        @param board current board being processed
        """
        nextBoard.g = board.g + 10
        nextBoard.h = self.get_heuristic(nextBoard)
        nextBoard.parent = board
        nextBoard.f = nextBoard.h + nextBoard.g
        #print "\nnextBoard f =" + str(nextBoard.f)
        #print "Updating board...\nboard: \n" + board.boardStateString() + "\n next_board:\n " + nextBoard.boardStateString()

    def board_in_list (self, board, aList):
        """
        Is board in aList?
        """
        #print "board_in_list"
        #print "board:\n " + board.boardStateString()
        for b in aList:
            #print b.boardStateString()
            if board.boardState == b.boardState:
                return True
        return False

    def is_board_state_end (self, boardState):
        """
        Is boardState the ending state?
        """
        return boardState == self.end.boardState

    def board_in_heapq (self, board, heapq):
        """
        Is board in heapq?
        """
        for f,b in heapq:
            #print "\nf: " + str(f) + "\n board.f: " + str(board.f)
            #print "\nb.boardState: \n" + b.boardStateString()
            #print "\board.boardState: \n" + board.boardStateString()
            if f == board.f and board.boardState == b.boardState:
                #print 'winning!'
                return True
        return False

    def process(self):
        if not self.is_solvable (self.start):
            print "not solvable!"
            return 1
        # add starting board to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop board from heap queue 
            f, board = heapq.heappop(self.opened)
            # add board to closed list so we don't process it twice
            self.closed.add(board)
            #print "board f = " +str(f)
            #print "board = \n" + board.boardStateString()
            #print "closed count = " + str(len(self.closed))
            #print "open count = " + str(len(self.opened))
            # if ending board, display found path
            if self.is_board_state_end (board.boardState): # board.boardState is self.end
                self.display_path()
                break
            # get next boards for board
            next_boards = self.get_next_boards(board)
            # iterate over next_boards
            for next_board in next_boards:
                if not self.board_in_list (next_board, self.closed): # dont process a closed board # next_board not in self.closed: #
                    if (next_board.f, next_board) in self.opened: #  self.board_in_heapq (next_board, self.opened)
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        #print "(next_board.f, next_board) in self.opened"
                        if next_board.g > board.g + 10:
                            self.update_board(next_board, board)
                    else:
                        self.update_board(next_board, board)
                        #print "next_board f =" + str(next_board.f)
                        # add next board to open list
                        heapq.heappush(self.opened, (next_board.f, next_board))

if __name__ == '__main__':
    a = AStar()
    a.init_grid()
    a.process()

