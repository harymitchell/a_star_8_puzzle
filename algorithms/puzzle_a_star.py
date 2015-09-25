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
        self.cells = []
        self.grid_height = 3
        self.grid_width = 3

    def init_grid(self):
        # original
        # walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3), 
        #         (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        # altered
        start = [[7,2,4],
                 [5,0,6],
                 [8,3,1]]
        end   = [[0,1,2],
                 [3,4,5],
                 [6,7,8]]
        self.start = Board(start)
        self.end = end
        print ("start", start)
        print ("end"  , end)

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
                goal_r, goal_c = self.index_of_tile (self.end, board.boardState[r][c])
                tile_total = abs(r - goal_r) + abs(c - goal_c)
                total += tile_total
                #print "Tile " + str(board.boardState[r][c]) + " has H value of: " + str(tile_total)
        return total

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
    
    def board_copy (self,board):
        """ Return a copy of board """
        return Board(list(list(b) for b in board.boardState))

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
            copy1 = self.board_copy (board)
            copy1.boardState[free_row][free_column] = board.boardState[free_row][free_column + 1]
            copy1.boardState[free_row][free_column + 1] = 0
            boards.append(copy1)
        if free_row > 0:
            copy2 = self.board_copy (board)
            copy2.boardState[free_row][free_column] = board.boardState[free_row - 1][free_column]
            copy2.boardState[free_row - 1][free_column] = 0
            boards.append(copy2)
        if free_column > 0:
            copy3 = self.board_copy (board)
            copy3.boardState[free_row][free_column] = board.boardState[free_row][free_column - 1]
            copy3.boardState[free_row][free_column - 1] = 0
            boards.append(copy3)
        if free_row < self.grid_height-1:
            copy4 = self.board_copy (board)
            copy4.boardState[free_row][free_column] = board.boardState[free_row + 1][free_column]
            copy4.boardState[free_row + 1][free_column] = 0
            boards.append(copy4)
        #print "get_next_boards board count = " + str(len(boards))
        #print "board after: \n" + board.boardStateString()
        #for b in boards:
        #    print "next: \n" + b.boardStateString()
        return boards

    def display_path(self):
        board = self.end
        while board.parent is not self.start:
            board = board.parent
            print 'path: board: %d,%d' % board.boardState

    def compare(self, board1, board2):
        """
        Compare 2 board F values

        @param board1 1st board
        @param board2 2nd board
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if board1.f < board2.f:
            return -1
        elif board1.f > board2.f:
            return 1
        return 0
    
    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g
    
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
        #print "Updating board...\nboard: \n" + board.boardStateString() + "\n next_board:\n " + nextBoard.boardStateString()

    def board_in_list (self, board, list):
        print "board_in_list"
        print "board:\n " + board.boardStateString()
        for b in list:
            #print b.boardStateString()
            if board.boardState == b.boardState:
                return True
        return False

    def process(self):
        # add starting board to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop board from heap queue 
            f, board = heapq.heappop(self.opened)
            # add board to closed list so we don't process it twice
            self.closed.add(board)
            # if ending board, display found path
            if board.boardState is self.end:
                self.display_path()
                break
            # get next boards for board
            next_boards = self.get_next_boards(board)
            # iterate over next_boards
            for next_board in next_boards:
                if not self.board_in_list (next_board, self.closed): # dont process a closed board #next_board not in self.closed: #
                    if (next_board.f, next_board) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if next_board.g > board.g + 10:
                            self.update_board(next_board, board)
                    else:
                        self.update_board(next_board, board)
                        # add next board to open list
                        heapq.heappush(self.opened, (next_board.f, next_board))
                else:
                    print ("next board in self.closed")

if __name__ == '__main__':
    a = AStar()
    a.init_grid()
    a.process()

