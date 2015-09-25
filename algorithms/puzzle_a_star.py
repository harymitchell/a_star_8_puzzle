import heapq

class Cell(object):
    def __init__(self, x, y, reachable, value):
        """
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        """
        self.reachable = reachable
        self.value = value
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

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
        start = ((7, 2  ,4),
                 (5,None,6),
                 (8, 3  ,1))
        end   = ((None,1,2),
                 (3,   4,5),
                 (6,   7,8))
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in start:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable, start[x][y]))
        self.start = start
        self.end = end
        print ("start", start)
        print ("end"  , end)

    def get_heuristic(self, cell):
        """
        Compute the heuristic value H for a cell: distance between
        this cell and the ending cell multiply by 10.

        @param cell
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """
        Returns a cell from the cells list

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x][y]

    def index_of_free_tile (board):
        """
        Returns the x,y index of the free tile in board.

        Board example:
                 ((7, 2  ,4),
                 (5,None,6),
                 (8, 3  ,1))


        @param board is a 2D board state
        @returns the x and y index of the free tile in board
        """
        for r in board:
            for c in x:
                if c is None:
                    return (r.index (c), c.index (None))


    def get_next_boards(self, board):
        """
        Returns all possible board states movable from board.

        @param board get all next board for this board
        @returns boards list 
        """
        boards = []
        free   = index_of_free_tile (board)
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print 'path: cell: %d,%d' % (cell.x, cell.y)

    def compare(self, cell1, cell2):
        """
        Compare 2 cells F values

        @param cell1 1st cell
        @param cell2 2nd cell
        @returns -1, 0 or 1 if lower, equal or greater
        """
        if cell1.f < cell2.f:
            return -1
        elif cell1.f > cell2.f:
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

    def process(self):
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue 
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, display found path
            if cell is self.end:
                self.display_path()
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

a = AStar()
a.init_grid()
a.process()

