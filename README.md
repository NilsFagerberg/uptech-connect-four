* Win conditions are checked after each successful drop
* Player turn is passed after each successful drop
* The main loop (in `play()`) handles I/O
* The unit test suite can be expanded upon, it's mainly there to ensure that the game is still correctly evaulated after any potential refactorings.
* The test suite can be run with `python3 -m unittest test_connect_four -v` and currently verifies:
    - Input validation
    - "Horizontal" win condition for both players (with offsets, e.g. X X X X . . . up to . . . X X X X)
    - "Vertical" win conditions for both players
    - Both diagonal win conditions for both players with offsets ("norhtwest" to "southeast" and "southwest" to "northeast")
    - Some validation of the initial game state
* If you have failing tests after a refactor, you can uncomment the "debugprint" calls in the failing test to see the board state after each game turn for the test. 
