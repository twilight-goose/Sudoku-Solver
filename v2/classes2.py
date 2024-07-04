import pygame
pygame.init()

from datetime import datetime
from datetime import timedelta
from datetime import date


class Square:
    """Represents a square on a Sudoku grid. Holds a number and
    a list of candidate numbers.
    
    Properties:
    
    variable       |type           |description
    ------------------------------------------------------------
    num             int
    
    candidate       list of int
    
    locked          bool
    
    """
    def __init__(self, pos, number, locked=False):
    
        self.number = number
        self.candidates = [number == 0] * 9
        self.locked = locked
        
        self.pos = pos
        self.has_conflict = False

    def reset_candidates(self):
        if self.number == 0:
            self.candidates = [True] * 9

    def set_number(self, number):
        if not self.locked and self.candidates[number - 1]:
            self.candidates = [False] * 9
            self.number = number
            self.has_conflict = False

    def set_conflict(self):
        self.has_conflict = True

    def reset(self):
        if not self.locked:
            self.number = 0
            self.reset_candidates()


class Grid:
    """Grid object: represents a Sudoku grid.
    
    Grid Quadrants and order of squares within quadrant:
    
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
    
    """

    # fonts for displaying grid on a surface
    FONT = pygame.font.SysFont("Ariel", 50)             # for numbers
    SMALL_FONT = pygame.font.SysFont("Ariel", 15)       # for candidates
    # offsets for displaying candidates
    OFFSETS = [(0, 0), (15, 0), (30, 0), (0, 15), (15, 15), (30, 15), (0, 30), (15, 30), (30, 30)]

    def __init__(self, grid, show_conflicts=True, show_candidates=True):
        def __fill_lists(self):
            for i in range(9):
                self.rows.append([])
                self.cols.append([])
                self.quadrants.append([])
        """
        grid is of form
        
            list of lists of int with dimensions 9x9
        """
        self.rows = []
        self.cols = []
        self.quadrants = []
        
        self.solvable = True
        self.show_conflicts = show_conflicts
        self.show_candidates = show_candidates
    
        __fill_lists(self)
    
        for i in range(81):
            row = i // 9
            col = i % 9 
            quad_num = col // 3 + 3 * (row // 3)
        
            square = Square([row, col], number=grid[row][col])

            self.rows[row].append(square)
            self.cols[col].append(square)
            self.quadrants[quad_num].append(square)
    
    def assign_candidates(self):
        # check the grid and assign squares their candidates numbers
        def assign_set(set_list):
            for _set in set_list:
            
                nums = [sq.number - 1 for sq in _set if sq.number != 0]
                
                for square in _set:
                    
                    # potentially replace with list mapping
                    # list comprehension
                    # numpy
                    for num in nums:
                        square.candidates[num] = False 
                    
                    if square.number == 0 and square.candidates.count(True) == 0:
                        self.solvable = False
       
        self.reset_candidates()
        assign_set(self.rows)
        assign_set(self.cols)
        assign_set(self.quadrants)
    
    def reset_candidates(self):
        for row in self.rows:
            for square in row:
                square.reset_candidates()
    
    def check(self):
        """This function checks and returns if the grid is solvable"""
        return self.assign_candidates()

    def is_solved(self):
        def sum_squares(squares):
            return sum(square.number for square in squares)
    
        """This function checks and returns if the grid has been solved"""
        
        for i in range(9):
            if sum_squares(self.rows[i]) != 45 or \
                    sum_squares(self.quadrants[i]) != 45 or \
                    sum_squares(self.cols[i]) != 45:\

                return False
        return True

    def copy_grid(self):
        """This function prints and returns the grid as a list of numbers"""
        new_list = []
        for i in range(9):
            new_list.append([])
            for j in range(9):
                new_list[i].append(self.rows[i][j].number)

        return new_list

    def set_square(self, pos, number, override_candidates=True):
        """This function sets the square at pos to number"""
        square = self.rows[pos[0]][pos[1]]
        
        if number == 0:
            square.reset()
        else:
            if override_candidates:
                square.reset()
            square.set_number(number)
        
        self.assign_candidates()

    def set_board(self):
        """This method sets all the current squares on the board and makes
            them unlocked"""
        for i in self.rows:
            for j in i:
                if j.number != 0:
                    j.locked = True

    def draw(self, screen, is_solve=True):
        """This function draws the Grid onto the passed surface. Draws the possibilities if is_solve is True"""
        for row in range(len(self.rows)):
            for col in range(len(self.rows[row])):
                square = self.rows[row][col]

                if square.number != 0:
                    number = self.FONT.render(str(square.number), True, [[(255, 255, 0), (255, 255, 255)][not square.locked],
                                                                         (255, 0, 0)][square.has_conflict])
                    screen.blit(number, (50 * (col + 1) - number.get_width() // 2,
                                         50 * (row + 1) - number.get_height() // 2))

                elif is_solve or self.show_candidates:
                    
                    for i in range(len(square.candidates)):
                        if square.candidates[i]:
                            number = self.SMALL_FONT.render(str(i + 1), True, (255, 255, 255))
                            x_offset, y_offset = self.OFFSETS[i]
                            screen.blit(number, (30 + 50 * col + x_offset,
                                                 30 + 50 * row + y_offset))

    def clear(self):
        """This function clears the Grid"""
        self.__init__([[0] * 9] * 9, show_conflicts=False, show_candidates=False)

    def check_correct(self):
        """This function checks if the Grid is correct or not so far,
            and finds any conflicts"""
        all_squares = self.quadrants + self.rows + self.cols
        for square_list in all_squares:
            for square in square_list:
                square.has_conflict = False

        for square_list in all_squares:
        
            numbers = [square.number for square in square_list]
            seen_numbers = []
            
            for square in square_list:
            
                num = square.number
                
                if num != 0:
                    if num in seen_numbers:
                    
                        square.has_conflict = True
                        square_list[seen_numbers.index(num)].has_conflict = True
                        self.solvable = False
                        
                seen_numbers.append(square.number)
                
        return self.solvable
    
    def solve(self):                    
        if not self.is_solved():
            i = False

            if not self.solve_singles() and self.solvable:      # no singles to solve, still solvable
                if not self.naked_doubles():                   # if no paired doubles
                    # if there are no singles to be solved and the grid can still be solved, brute force
                    if not self.naked_triples():
                        return self.brute_force(2)
                    # i is a list of different grid possibilities
            else:
                # if a single was solved
                self.assign_candidates()
            return i

    def solve_singles(self):
        """Solve naked singles"""
        ret_val = False
        
        for row in self.rows:
            indexes = find_occurrences(row)
            
            for i in range(9):
                current_square = row[i]
                
                if current_square.candidates.count(True) == 1:
                    
                    current_square.set_number(current_square.candidates.index(True) + 1)
                    self.assign_candidates()
                    
                    if not self.solvable:
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        row[i].reset()
                        self.assign_candidates()
                        return False
                    else:
                        ret_val = True
                    
                if len(indexes[i]) == 1:
                    row[indexes[i][0]].set_number(i + 1)
                    self.assign_candidates()
                    
                    if not self.solvable:
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        row[indexes[i][0]].reset()
                        self.assign_candidates()
                        return False
                    else:
                        ret_val = True
        
        remaining_sq = self.cols + self.quadrants
        
        for square_list in remaining_sq:
            indexes = find_occurrences(square_list)

            for i in range(9):
                current_square = square_list[i]
                
                # the only square in the list that can have the number
                if len(indexes[i]) == 1:
                    square_list[indexes[i][0]].set_number(i + 1)
                    self.assign_candidates()
                    
                    if not self.solvable:
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        square_list[indexes[i][0]].reset()
                        self.assign_candidates()
                        return False
                    else:
                        ret_val = True
        # if it goes through every row, column, and group and cannot find any singles return False
        # so it starts brute forcing
        return ret_val
    
    def naked_doubles(self):
        ret_val = False
        
        for _set_ in self.rows + self.cols + self.quadrants:
            """solve paired doubles"""
            # for each set of 9 squares
            # list of all candidates for squares in the set
            cands = [sq.candidates for sq in _set_]
            
            # for each square in the set
            for i in range(8):
                # if the square has only 2 candidates and 
                # another square only has the same two candidates
                if cands[i].count(True) == 2 and \
                        cands.count(cands[i]) == 2:
                    # retrieve the candidate values
                    can1 = cands[i].index(True)
                    can2 = cands[i].index(True, can1 + 1)
                    
                    # remove those candidates from the other squares
                    # in the set becuase those two values must be
                    # in those two squares
                    for sq in [sq for sq in _set_ if sq.candidates != cands[i]]:
                        
                        if sq.candidates[can1] or sq.candidates[can2]:
                            ret_val = True

                            sq.candidates[can1] = False
                            sq.candidates[can2] = False

        return ret_val
    
    def naked_triples(self):
        ret_val = False
        
        for _set_ in self.rows + self.cols + self.quadrants:
            # for each set of 9 squares
            # list of all candidates for squares in the set
            cands = [sq.candidates for sq in _set_]
            
            # for each square in the set
            for i in range(7):
                # if the square has only 2 candidates and 
                # another square only has the same two candidates
                if cands[i].count(True) == 3 and \
                        cands.count(cands[i]) == 3:
                    # retrieve the candidate values
                    can1 = cands[i].index(True)
                    can2 = cands[i].index(True, can1 + 1)
                    can3 = cands[i].index(True, can2 + 1)
                    
                    # remove those candidates from the other squares
                    # in the set becuase those two values must be
                    # in those two squares
                    for sq in [sq for sq in _set_ if sq.candidates != cands[i]]:
                        if sq.candidates[can1] or sq.candidates[can2] or sq.candidates[can3]:
                            ret_val = True
                            sq.candidates[can1] = False
                            sq.candidates[can2] = False
                            sq.candidates[can3] = False

        return ret_val
    
    def brute_force(self, target):
        """This function finds x number of possible boards and returns them all"""
        grids = []
        
        self.assign_candidates()
        
        for quadrant in self.quadrants:           # check every group in the grid
            
            indexes = find_occurrences(quadrant)
            
            for i in range(9):
                if len(indexes[i]) == target:
                    for index in indexes[i]:
                        
                        new_grid = Grid(self.copy_grid())
                        new_grid.set_square(quadrant[index].pos, i + 1)
                        new_grid.assign_candidates()
                        grids.append(new_grid)
                            
                    return grids
        return self.brute_force(target + 1)
        
    def __str__(self):
        ret_val = ""
        for row in self.rows:
            ret_val += str([col.number for col in row]) + "\n"
        return ret_val
        

def find_occurrences(squares):
    """returns
    list of 9
        lists of square
            where square has candidate i = 1-9
    """
    # this list tracks the indexes in the group that an occurrence appeared
    indexes = [[] for x in range(9)]
    # goes through every square
    for square in squares:
        # checks if the square can have each number from 1-9
        for i in range(9):
            
            if square.candidates[i]:
                # adds an occurrence to the tracker and marks the index
                indexes[i].append(squares.index(square))
                
    return indexes

#######################################################################################
#######################################################################################


class Timer:
    """
    Just for timing operations to compare temporal efficiency.
    """
    def __init__(self):
        self.s_time = datetime.now()

    def start(self):
        self.s_time = datetime.now()

    def stop(self):
        d = datetime.now() - self.s_time
        print("That took {0} seconds and {1} microseconds\n".format(d.seconds, d.microseconds))

