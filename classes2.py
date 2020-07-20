import pygame
pygame.init()


class Square:
    """Square class that represents a square on a Sudoku grid. Holds a number and
    a list of the possible numbers that can go in it
    """
    def __init__(self, group, number):
        self.number = number
        self.group_num = group
        self.can_have = [number == 0] * 9
        self.is_wrong = False

    def reset_can_have(self):
        if self.number == 0:
            self.can_have = [True] * 9

    def set_number(self, number):
        if self.number == 0 and self.can_have[number]:
            self.can_have = [False] * 9
            self.number = number + 1

    def set_wrong(self):
        self.is_wrong = True

    def reset(self):
        self.reset_can_have()
        self.number = 0


class Grid:
    """Grid object: represents a Sudoku grid. Contains the code and logic to solve any grid."""
    # fonts for displaying grid on a surface
    FONT = pygame.font.SysFont("Ariel", 50)             # for numbers
    SMALL_FONT = pygame.font.SysFont("Ariel", 15)       # for possibilities
    # offsets for displaying number possibilities
    OFFSETS = [(0, 0), (15, 0), (30, 0), (0, 15), (15, 15), (30, 15), (0, 30), (15, 30), (30, 30)]

    def __init__(self, grid, show_wrong=True, show_possible=True):
        self.elements = []
        self.groups = []
        self.solvable = True
        self.show_wrong = show_wrong
        self.show_possible = show_possible
        for i in range(9):
            self.elements.append([])
            self.groups.append([])

        for row in range(9):
            for col in range(9):
                group_num = col // 3 + 3 * (row // 3)
                square = Square(group_num, grid[row][col])

                self.elements[row].append(square)
                self.groups[group_num].append(square)

    def solve(self):
        if not self.is_solved():
            i = False
            self.assign_possible()
            if not self.solve_singles() and self.solvable:
                # if there are no singles to be solved and the grid can still be solved, brute force
                i = self.brute_force(2)
                # i is a list of different grid possibilities
            self.assign_possible()
            # return the grids
            return i

    def assign_possible(self):
        # check the grid and assign squares their possible numbers
        for row_num in range(9):
            for col_num in range(9):
                self.elements[row_num][col_num].reset_can_have()

        for num in range(1, 10):
            occurrences = []

            for row_num in range(9):
                for col_num in range(9):
                    if self.elements[row_num][col_num].number == num:
                        occurrences.append([row_num, col_num])

            for occurrence in occurrences:
                row, col = occurrence

                for square in self.elements[row]:
                    square.can_have[num - 1] = False

                for square in self.groups[self.elements[row][col].group_num]:
                    square.can_have[num - 1] = False

                for row in self.elements:
                    row[col].can_have[num - 1] = False

    def solve_singles(self):
        """This function solves the first single it finds and returns True. If it can't find any
            singles or solving a single results in it not being solvable, return False."""
        all_squares = self.groups + self.elements

        for col in range(9):
            all_squares += [[row[col] for row in self.elements]]

        for square_list in all_squares:
            indexes = find_occurrences(square_list)
            for index in range(9):
                current_square = square_list[index]
                # square only has 1 possible number
                if current_square.can_have.count(True) == 1:
                    # find the number and put it in the square
                    current_square.set_number(current_square.can_have.index(True))
                    if not self.check():
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        square_list[index].reset()
                        self.assign_possible()
                        return False
                    return True
                # the only square in the list that can have the number
                elif len(indexes[index]) == 1:
                    square_list[indexes[index][0]].set_number(index)
                    if not self.check():
                        # solve a single and fail check means we know the current grid is
                        # wrong, return False
                        square_list[indexes[index][0]].reset()
                        self.assign_possible()
                        return False
                    return True
        # if it goes through every row, column, and group and cannot find any singles return False
        # so it starts brute forcing
        return False

    def brute_force(self, occurrences):
        """This function finds x number of possible boards and returns them all"""
        grids = []
        for group in self.groups:           # check every group in the grid
            indexes = find_occurrences(group)
            for num in range(9):
                if len(indexes[num]) == occurrences:
                    for index in indexes[num]:
                        # try to solve for each possible square in a group for a number
                        # create a copy of the current board that can be manipulated
                        group[index].set_number(num)
                        self.assign_possible()
                        grid = Grid(self.copy_grid())
                        grid.copy_grid()
                        grids.append(grid)
                        # if no pass test reset the grid to previous and try again
                        group[index].reset()
                        self.assign_possible()
                    return grids
        # if there are no groups with occurrence number of occurrences, recurse increasing the
        # target occurrence by 1
        return self.brute_force(occurrences + 1)

    def check(self):
        """This function checks and returns if the grid is solvable"""
        self.assign_possible()
        for row in self.elements:
            for square in row:
                if square.number == 0 and not any(square.can_have):
                    self.solvable = False
        return self.solvable

    def is_solved(self):
        """This function checks and returns if the grid has been solved"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        all_squares = self.groups + self.elements

        for col in range(9):
            all_squares += [[row[col] for row in self.elements]]

        for square_list in all_squares:
            square_nums = [x.number for x in square_list]
            square_nums.sort()
            if numbers != square_nums:
                return False
        return True

    def copy_grid(self):
        """This function prints and returns the grid as a list of numbers"""
        new_list = []
        for i in range(len(self.elements)):
            new_list.append([])
            for j in range(len(self.elements[i])):
                new_list[i].append(self.elements[i][j].number)
        for row in new_list:
            print([col for col in row])
        return new_list

    def set_square(self, pos, number):
        """This function sets the square at 'pos' to 'number'"""
        self.elements[pos[0]][pos[1]].set_number(number - 1)
        if self.show_possible:
            self.assign_possible()

    def draw(self, screen, is_solve=True):
        """This function draws the Grid onto the passed surface. Draws the possibilities if is_solve is True"""
        for row in range(len(self.elements)):
            for col in range(len(self.elements[row])):
                square = self.elements[row][col]

                if square.number != 0:
                    number = self.FONT.render(str(square.number), True, [(255, 255, 255), (255, 0, 0)]
                                                                        [square.is_wrong])
                    screen.blit(number, (50 * (col + 1) - number.get_width() // 2,
                                         50 * (row + 1) - number.get_height() // 2))
                elif is_solve or self.show_possible:
                    for i in range(len(square.can_have)):
                        if square.can_have[i]:
                            number = self.SMALL_FONT.render(str(i + 1), True, (255, 255, 255))
                            x_offset, y_offset = self.OFFSETS[i]
                            screen.blit(number, (30 + 50 * col + x_offset,
                                                 30 + 50 * row + y_offset))

    def clear(self):
        """This function clears the Grid"""
        self.__init__([[0] * 9] * 9, show_wrong=False, show_possible=False)

    def check_correct(self):
        """This function checks if the Grid is correct or not so far"""
        self.show_wrong = True
        self.solvable = True
        all_squares = self.groups + self.elements

        for col in range(9):
            all_squares += [[row[col] for row in self.elements]]

        for square_list in all_squares:
            numbers = [square.number for square in square_list]
            for i in range(1, 10):
                if numbers.count(i) > 1:
                    self.solvable = False
        return self.solvable


def find_occurrences(squares):
    """This function returns a list of lists of indexes of the possibilities of numbers"""
    # this list tracks the indexes in the group that an occurrence appeared
    indexes = []
    for i in range(9):
        indexes.append([])
    # goes through every square
    for square in squares:
        # checks if the square can have each number from 1-9
        for i in range(9):
            if square.can_have[i]:
                # adds an occurrence to the tracker and marks the index
                indexes[i].append(squares.index(square))
                
    return indexes

