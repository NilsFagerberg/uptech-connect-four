class ConnectFour:
    """A Connect Four game with a 7x6 board."""
    
    def __init__(self):
        """Initialize the game board with dimensions 7 columns x 6 rows."""
        self.columns = 7
        self.rows = 6
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.column_heights = [0] * self.columns  # Track the next available row for each column
        self.current_player = 1  # Player 1 starts
        self.winner = 0
    
    def get_game_state(self):
        """Return the current game state as a matrix (7x6)."""
        return [row[:] for row in self.board]
    
    def print_game_state(self):
        """Print the current game state to stdout."""
        print("\n")
        # Print column numbers
        print("  " + " ".join(str(i) for i in range(self.columns)))
        print(" " + "-" * (self.columns * 2 + 1))
        
        # Print board with row separators (reversed to show top row visually at top)
        for row_index, row in enumerate(reversed(self.board)):
            display_row = self.rows - 1 - row_index
            print("| " + " ".join(self._get_symbol(cell) for cell in row) + f" | {display_row}")
        
        print(" " + "-" * (self.columns * 2 + 1))
        print()
    
    def _get_symbol(self, cell):
        """Get the symbol to display for a cell."""
        if cell == 0:
            return "."
        elif cell == 1:
            return "X"
        else:  # cell == 2
            return "O"
    
    def is_valid_move(self, column):
        """Check if a move is valid for the given column."""
        if column < 0 or column >= self.columns:
            return False
        return self.column_heights[column] < self.rows
    
    def drop_piece(self, column):
        """
        Drop a piece in the specified column.
        
        Returns True if the move was successful, False otherwise.
        """
        if not self.is_valid_move(column):
            return False
        
        row = self.column_heights[column]
        self.board[row][column] = self.current_player
        self.column_heights[column] += 1

        # sets winner, if any
        self.set_winner(self.check_winner())
        self.switch_player()

        return True
    
    def check_winner(self):
        """
        Check if there's a winner.
        
        Returns the player number (1 or 2) if there's a winner, 0 otherwise.
        """
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.columns - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row][col + 1] ==
                    self.board[row][col + 2] == self.board[row][col + 3]):
                    return self.board[row][col]
        
        # Check vertical
        for col in range(self.columns):
            if self.column_heights[col] < 4:
                continue  # Not enough pieces in this column to have a winner
            for row in range(self.rows - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row + 1][col] ==
                    self.board[row + 2][col] == self.board[row + 3][col]):
                    return self.board[row][col]
        
        # Check diagonal (bottom-left to top-right)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row - 1][col + 1] ==
                    self.board[row - 2][col + 2] == self.board[row - 3][col + 3]):
                    return self.board[row][col]
        
        # Check diagonal (top-left to bottom-right)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row + 1][col + 1] ==
                    self.board[row + 2][col + 2] == self.board[row + 3][col + 3]):
                    return self.board[row][col]
        
        return 0
    
    def is_board_full(self):
        """Check if the board is full."""
        return all(height == self.rows for height in self.column_heights)
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 3 - self.current_player  # Toggles between 1 and 2
    
    def set_winner(self, player):
        """Set the winner of the game. This can only be done once."""
        if self.winner == 0:
            self.winner = player

    def play(self):
        """Main game loop for playing Connect Four."""
        print("Welcome to Connect Four!")
        print("Players take turns dropping pieces into columns (0-6).")
        print("Player 1 is X, Player 2 is O")
        print("First to get 4 in a row wins!\n")
        
        self.print_game_state()
        
        while True:
            # Get player input
            player_symbol = "X" if self.current_player == 1 else "O"
            while True:
                try:
                    column = int(input(f"Player {self.current_player} ({player_symbol}), enter column (0-{self.columns - 1}): "))
                    if self.drop_piece(column):
                        break
                    else:
                        print(f"Invalid move! Column {column} is full or out of range. Try again.")
                except ValueError:
                    print("Invalid input! Please enter a number.")
            
            self.print_game_state()
            
            # Check for winner
            if self.winner:
                print(f"Player {self.winner} wins! Congratulations!")
                break
            
            # Check for draw
            if self.is_board_full():
                print("It's a draw!")
                break


def main():
    """Run the Connect Four game."""
    game = ConnectFour()
    game.play()


if __name__ == "__main__":
    main()
