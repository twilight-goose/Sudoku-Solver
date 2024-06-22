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
    def __init__(self, quad_num, number, locked=False):
    
        self.number = number
        self.candidates = [number == 0] * 9
        self.locked = locked
        
        self.quad_num = quad_num
        self.has_conflict = False

    def reset_candidates(self):
        if self.number == 0:
            self.candidates = [True] * 9

    def set_number(self, number):
        if not self.locked and self.candidates[number]:
            self.candidates = [False] * 9
            self.number = number + 1

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
        self.show_candidates =   show_candidates
    
        __fill_lists(self)
    
        for i in range(81):
            row = i // 9
            col = i % 9 
            quad_num = col // 3 + 3 * (row // 3)
        
            square = Square(quad_num, number=grid[row][col])

            self.rows[row].append(square)
            self.cols[col].append(square)
            self.quadrants[quad_num].append(square)

    def solve(self):
        if not self.is_solved():
            i = False
            self.assign_candidates()

            if not self.solve_singles() and self.solvable:
                # if there are no singles to be solved and the grid can still be solved, brute force
                i = self.brute_force(2)
                # i is a list of different grid possibilities
            self.assign_candidates()
            # return the grids
            return i

    def assign_candidates(self):
        # check the grid and assign squares their candidates numbers
        for row in range(9):
            for col in range(9):
                self.rows[row][col].reset_candidates()

        for num in range(1, 10):
            occurrences = []

            for row_num in range(9):
                for col_num in range(9):
                    if self.rows[row_num][col_num].number == num:
                        occurrences.append([row_num, col_num])

            for occurrence in occurrences:
                row, col = occurrence

                for square in self.rows[row]:
                    square.candidates[num - 1] = False

                for square in self.quadrants[self.rows[row][col].quad_num]:
                    square.candidates[num - 1] = False

                for row in self.rows:
                    row[col].candidates[num - 1] = False

    def solve_singles(self):
        """This function solves the first single it finds and returns True. If it can't find any
            singles or solving a single results in it not being solvable, return False."""
        all_squares = self.quadrants + self.rows

        for col in range(9):
            all_squares += [[row[col] for row in self.rows]]

        for square_list in all_squares:
            indexes = find_occurrences(square_list)
            for index in range(9):
                current_square = square_list[index]
                # square only has 1 candidates number
                if current_square.candidates.count(True) == 1:
                    # find the number and put it in the square
                    current_square.set_number(current_square.candidates.index(True))
                    if not self.check():
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        square_list[index].reset()
                        self.assign_candidates()
                        return False
                    return True
                # the only square in the list that can have the number
                elif len(indexes[index]) == 1:
                    square_list[indexes[index][0]].set_number(index)
                    if not self.check():
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        square_list[indexes[index][0]].reset()
                        self.assign_candidates()
                        return False
                    return True
        # if it goes through every row, column, and quadrant and cannot find any singles return False
        # so it starts brute forcing
        return False

    def brute_force(self, occurrences):
        """This function finds x number of candidates boards and returns them all"""
        grids = []
        for quadrant in self.quadrants:           # check every quadrant in the grid
            indexes = find_occurrences(quadrant)
            for num in range(9):
                if len(indexes[num]) == occurrences:
                    for index in indexes[num]:
                        # try to solve for each candidates square in a quadrant for a number
                        # create a copy of the current board that can be manipulated
                        quadrant[index].set_number(num)
                        self.assign_candidates()
                        grid = Grid(self.copy_grid())
                        grid.copy_grid()
                        grids.append(grid)
                        # if no pass test reset the grid to previous and try again
                        quadrant[index].reset()
                        self.assign_candidates()
                    return grids
        # if there are no quadrants with occurrence number of occurrences, recurse increasing the
        # target occurrence by 1
        return self.brute_force(occurrences + 1)

    def check(self):
        """This function checks and returns if the grid is solvable"""
        self.assign_candidates()
        for row in self.rows:
            for square in row:
                if square.number == 0 and not any(square.candidates):
                    self.solvable = False
        return self.solvable

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
        for i in range(len(self.rows)):
            new_list.append([])
            for j in range(len(self.rows[i])):
                new_list[i].append(self.rows[i][j].number)
        for row in new_list:
            print([col for col in row])
        return new_list

    def set_square(self, pos, number, override_candidates=False):
        """This function sets the square at 'pos' to 'number'"""
        square = self.rows[pos[0]][pos[1]]
        if number == 0:
            square.reset()
        else:
            if override_candidates:
                square.reset()
            square.set_number(number - 1)

        if self.show_candidates:
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
        self.solvable = True

        for quadrant in self.quadrants:
            for square in quadrant:
                square.has_conflict = False

        all_squares = self.quadrants + self.rows

        for col in range(9):
            all_squares += [[row[col] for row in self.rows]]

        for square_list in all_squares:
            numbers = [square.number for square in square_list]
            for i in range(1, 10):
                if numbers.count(i) > 1:
                    self.solvable = False
                    for square in square_list:
                        if square.number == i:
                            square.has_conflict = True
        return self.solvable


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

#-------------------------------------------------------------------------------

def find_occurrences(squares):
    """This function returns a list of lists of indexes of the possibilities of numbers"""
    # this list tracks the indexes in the quadrant that an occurrence appeared
    indexes = []
    for i in range(9):
        indexes.append([])
    # goes through every square
    for square in squares:
        # checks if the square can have each number from 1-9
        for i in range(9):
            if square.candidates[i]:
                # adds an occurrence to the tracker and marks the index
                indexes[i].append(squares.index(square))
                
    return indexes

