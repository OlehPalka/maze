"""
Implemention of the Maze ADT using a 2-D array.
git repo - https://github.com/OlehPalka/maze
"""
import copy
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert 0 <= row < self.num_rows() and \
            0 <= col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert 0 <= row < self.num_rows() and \
            0 <= col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert 0 <= row < self.num_rows() and \
            0 <= col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        stack = Stack()
        stack.push((self._start_cell.row, self._start_cell.col))
        (row, col) = stack.peek()
        while len(stack) != 0:

            prev_row = row
            prev_col = col
            (row, col) = stack.peek()
            if prev_row == row and prev_col == col:
                (row, col) = stack.pop()

            counter = False
            if self._exit_found(row, col):
                self._mark_path(row, col)
                return True

            if self._valid_move(row, col - 1):
                stack.push((row, col - 1))
                counter = True

            if self._valid_move(row + 1, col):
                stack.push((row + 1, col))
                counter = True

            if self._valid_move(row, col + 1):
                stack.push((row, col + 1))
                counter = True

            if self._valid_move(row - 1, col):
                stack.push((row - 1, col))
                counter = True

            if counter:
                self._mark_path(row, col)
            else:
                self._mark_tried(row, col)

        for rows in range(self.num_rows()):
            for cols in range(self.num_cols()):
                part = self._maze_cells[rows, cols]
                if part == "x":
                    self._maze_cells[rows, cols] = "o"
        return False

    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for rows in range(self.num_rows()):
            for cols in range(self.num_cols()):
                part = self._maze_cells[rows, cols]
                if part in ("x", "o"):
                    self._maze_cells[rows, cols] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        result = ""
        for rows in range(self.num_rows()):
            for cols in range(self.num_cols()):
                part = self._maze_cells[rows, cols]
                if part is None:
                    part = "_"
                else:
                    part = str(part)
                result += part + " "
            result += "\n"
        return result[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return 0 <= row < self.num_rows() \
            and 0 <= col < self.num_cols() \
            and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col
