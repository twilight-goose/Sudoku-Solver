import pygame
import random
import classes2 as classes
import ui
pygame.init()

'''
Author: James Wang
Date:
Version:
Description: Basic Sudoku interface with solving algorithm. User can input their own grid
            and the program can show the possible numbers by toggling a button, and the program
            can solve it for you if it is solvable.
'''


# constant array for the "hardest" sudoku grid
# can only be solved with brute force
# for testing and visualization purposes only
HARDEST_GRID = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 0, 0],
                [0, 7, 0, 0, 9, 0, 2, 0, 0],
                [0, 5, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 5, 7, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 3, 0],
                [0, 0, 1, 0, 0, 0, 0, 6, 8],
                [0, 0, 8, 5, 0, 0, 0, 1, 0],
                [0, 9, 0, 0, 0, 0, 4, 0, 0]]

# global screen constant for everything to be displayed on
SCREEN = pygame.display.set_mode((675, 500))
pygame.display.set_caption("Small Brain Sudoku Go Brrrrrrrrrrrr")

# Black background for the screen
BACKGROUND = pygame.Surface((675, 500))
BACKGROUND.fill((0, 0, 0))

# Blit background onto the screen
SCREEN.blit(BACKGROUND, (0, 0))

# Global constant object for cycle ticking
CLOCK = pygame.time.Clock()

# Global bool constant for whether the user wants the program to run
RUN = True

EVERY_CORD = []
for x in range(9):
    for y in range(9):
        EVERY_CORD.append((x, y))


def solve(grid):
    """
    Takes a Grid object as a parameter and if it's solvable returns the solved
    Grid object. If it's not solvable, it returns False.
    """
    # determine if the given grid is solvable or not
    if not grid.check_correct() or not grid.check:
        return False        # return False if the grid cannot be solved

    # if the grid can be solved, initialize variables needed to begin solving
    global RUN
    grids = [grid]
    solved = False
    solved_grid = None

    # run the function until either the user wants to exit or the grid is solved
    while not solved and RUN:
        # refresh at 120 cycles per second so solving speed is not limited by frame rate
        # CLOCK.tick(120)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUN = False

        if len(grids) == 0:
            return False
        # solving algorithm
        current_grid = grids[-1]            # choose the last grid in the list of grids
        result = current_grid.solve()       # do a single step in the solving process

        if not current_grid.solvable:       # if the grid is no longer solvable, delete it
            grids.pop(-1)
        elif current_grid.is_solved():      # if the grid has been solved
            solved = True                           # exit the loop
            solved_grid = current_grid              # and return the solution
        elif result:                        # if the return value is a grid (brute force returns grid)
            grids.remove(current_grid)          # remove the current grid from the list
            grids.extend(result)                # replace it with the different possibilities

        # refresh the screen and board
        draw_board(SCREEN, None, [-1, -1])
        current_grid.draw(SCREEN, is_solve=True)
        pygame.display.flip()
    # return the solved grid if it is solved
    return solved_grid


def main():
    """The main function of the program."""
    # initialize a Grid object that the user can interact with
    grid = classes.Grid([[0] * 9] * 9, show_conflicts=False, show_possible=False)

    # surface object that indicates the square that the user has selected
    selected_square = pygame.Surface((50, 50))
    selected_square.fill((120, 120, 120))
    selected_cord = [-1, -1]

    # key constants for number input
    number_key = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5,
                  pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}

    number_key.update({pygame.K_KP1: 1, pygame.K_KP2: 2, pygame.K_KP3: 3, pygame.K_KP4: 4, pygame.K_KP5: 5,
                       pygame.K_KP6: 6, pygame.K_KP7: 7, pygame.K_KP8: 8, pygame.K_KP9: 9})

    # 4 GUI buttons that the user can interact with
    solve_button = ui.Button("Solve", (502, 25))
    check_button = ui.Button("Check", (502, 100))
    show_button = ui.Button("Show Possible", (502, 175))
    clear_button = ui.Button("Clear", (502, 250))
    load_random = ui.Button("Generate Grid", (502, 325))
    hardest_button = ui.Button("Load Hardest", (502, 400))
    # list of buttons
    buttons = [solve_button, check_button, clear_button, show_button, load_random, hardest_button]

    global RUN

    while RUN:
        # refresh standard 60 times per second
        CLOCK.tick(60)
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            elif event.type == pygame.KEYDOWN:
                # keyboard input - inserting and deleting numbers on the board
                if event.key == pygame.K_ESCAPE:
                    selected_cord = [-1, -1]                    # deselect the square
                elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                    grid.set_square(selected_cord, 0)           # clear the selected square
                elif event.key in number_key.keys():
                    number = number_key[event.key]
                    grid.set_square(selected_cord, number, override_can_have=True)      # place a number in a square
                elif event.key == pygame.K_UP:
                    if selected_cord[0] != 0:
                        selected_cord[0] -= 1
                elif event.key == pygame.K_DOWN:
                    if selected_cord[0] != 8:
                        selected_cord[0] += 1
                elif event.key == pygame.K_LEFT:
                    if selected_cord[1] != 0:
                        selected_cord[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    if selected_cord[1] != 8:
                        selected_cord[1] += 1
                elif event.key == pygame.K_t:
                    timer = classes.Timer()
                    grid.assign_possible()
                    timer.stop()
                  
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Mouse input - selecting a square on the grid and buttons
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x in range(25, 475) and y in range(25, 475):
                    selected_cord = [(y - 25) // 50, (x - 25) // 50]
                elif x in range(500, 650):
                    if y in range(25, 75):
                        solved_grid = solve(grid)
                        if solved_grid:
                            solve_button.reset()
                            grid = solved_grid
                        elif solved_grid is not None:
                            solve_button.cannot_solve()
                    elif y in range(100, 150):
                        grid.check()
                        grid.show_conflicts = not grid.check_correct()
                    elif y in range(175, 225):
                        grid.assign_possible()
                        grid.show_possible = not grid.show_possible
                    elif y in range(250, 300):
                        grid.clear()
                    elif y in range(325, 375):
                        grid = generate_grid()
                    elif y in range(400, 450):
                        grid = classes.Grid(HARDEST_GRID, show_possible=False)

        # refresh the screen, board, and buttons
        draw_board(SCREEN, selected_square, selected_cord)
        grid.draw(SCREEN, is_solve=False)
        for button in buttons:
            button.draw(SCREEN)

        pygame.display.flip()


def generate_grid():
    """This function generates a random grid of a random difficulty and returns
        it as a Grid object. It creates an empty grid, fills a random square,
        the solves it. Then it randomly removes"""
    grid = classes.Grid([[0] * 9] * 9)
    x, y = random.randrange(9), random.randrange(9)
    grid.set_square((x, y), random.randrange(1, 10))
    cords = EVERY_CORD.copy()

    grid = solve(grid)
    grid.show_possible = False

    squares_to_clear = []

    for i in range(50 + random.randrange(0, 19)):
        cord_index = random.randrange(len(cords))
        cord = cords[cord_index]
        cords.pop(cord_index)
        squares_to_clear.append(cord)

    for cord in squares_to_clear:
        grid.set_square(cord, 0)
    grid.set_board()

    return grid


def draw_board(screen, selected_square, cord):
    """This function draws a 9 x 9 grid and the selected square indicator
        onto the passed surface"""
    screen.fill((0, 0, 0))
    if cord != [-1, -1]:
        screen.blit(selected_square, (cord[1] * 50 + 25, cord[0] * 50 + 25))

    for i in range(10):
        pos = 25 + 50 * i
        pygame.draw.line(screen, (255, 255, 255), (25, pos), (475, pos))
        pygame.draw.line(screen, (255, 255, 255), (pos, 25), (pos, 475))

    pygame.draw.line(screen, (255, 255, 255), (25, 175), (475, 175), 5)
    pygame.draw.line(screen, (255, 255, 255), (25, 325), (475, 325), 5)
    pygame.draw.line(screen, (255, 255, 255), (175, 25), (175, 475), 5)
    pygame.draw.line(screen, (255, 255, 255), (325, 25), (325, 475), 5)

    pygame.draw.line(screen, (255, 255, 255), (25, 25), (475, 25), 5)
    pygame.draw.line(screen, (255, 255, 255), (25, 475), (475, 475), 5)
    pygame.draw.line(screen, (255, 255, 255), (25, 25), (25, 475), 5)
    pygame.draw.line(screen, (255, 255, 255), (475, 25), (475, 475), 5)


main()
pygame.quit()

