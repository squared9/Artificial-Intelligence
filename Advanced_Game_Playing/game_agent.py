"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

previous_moves = {}  # map stack with # of player moves


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def score_1(game, player):  # 82.14%
    """
    Heuristics computing score using #player moves - k * #opponent moves
    :param game: game
    :param player: player
    :return: score
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)

    opponent = game.get_opponent(player)
    player_moves = game.get_legal_moves(player)
    opponent_moves = game.get_legal_moves(opponent)

    # return float(len(player_moves) - len(opponent_moves))  # 72.86%
    # return float(len(player_moves) - 2 * len(opponent_moves))  # 79.29%
    # return float(len(player_moves) - 3 * len(opponent_moves))  # 79.29%
    # return float(len(player_moves) - 4 * len(opponent_moves))  # 79.29%
    # return float(len(player_moves) - 5 * len(opponent_moves))  # 80.71%
    # return float(len(player_moves) - 6 * len(opponent_moves))  # 80.71%
    return float(len(player_moves) - 7 * len(opponent_moves))  # 82.14%
    # return float(len(player_moves) - 8 * len(opponent_moves))  # 73.57%
    # return float(len(player_moves) - 9 * len(opponent_moves))  # 79.29%
    # return float(len(player_moves) - 10 * len(opponent_moves))  # 77.86%
    # return float(len(player_moves) - 11 * len(opponent_moves))  # 77.86%


def score_2(game, player):  # 67.14%
    """
    Heuristics computing score as a difference between change of player moves and change of opponent moves
    :param game: game
    :param player: player
    :return: score
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)

    opponent = game.get_opponent(player)

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(opponent))

    previous_player_moves = peek_previous_moves(player)
    previous_opponent_moves = peek_previous_moves(opponent)

    if previous_player_moves is None:
        previous_player_moves = 2 * player_moves

    if previous_opponent_moves is None:
        previous_opponent_moves = 2 * opponent_moves

    return float((previous_player_moves - player_moves) - (previous_opponent_moves - opponent_moves))


def score_3(game, player):  # 57.14%
    """
    Heuristics computing score as a difference between change ratio of the number player and opponent moves
    :param game: game
    :param player: player
    :return: score
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)

    opponent = game.get_opponent(player)

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(opponent))

    previous_player_moves = peek_previous_moves(player)
    previous_opponent_moves = peek_previous_moves(opponent)

    if previous_player_moves is None:
        previous_player_moves = 2 * player_moves

    if previous_opponent_moves is None:
        previous_opponent_moves = 2 * opponent_moves

    if player_moves == 0:
        return float("-inf")
    if opponent_moves == 0:
        return float("inf")

    return float((previous_player_moves / player_moves) - (previous_opponent_moves / opponent_moves))


def score_4(game, player):  # 50.71%
    """
    Heuristics computing score as a ratio of change ratio of the number of player and opponent moves
    :param game: game
    :param player: player
    :return: score
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)

    opponent = game.get_opponent(player)

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(opponent))

    previous_player_moves = peek_previous_moves(player)
    previous_opponent_moves = peek_previous_moves(opponent)

    if previous_player_moves is None:
        previous_player_moves = 2 * player_moves

    if previous_opponent_moves is None:
        previous_opponent_moves = 2 * opponent_moves

    if player_moves == 0:
        return float("-inf")
    if opponent_moves == 0:
        return float("inf")

    return float((previous_player_moves / player_moves) / (previous_opponent_moves / opponent_moves))


def score_5(game, player):  # 78.57%
    """
    Heuristics computing score based on ratio of player and opponents moves and difference of number opponent moves
    :param game: game
    :param player: player
    :return: score
    """
    if game.is_winner(player) or game.is_loser(player):
        return game.utility(player)

    opponent = game.get_opponent(player)

    player_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(opponent))

    previous_player_moves = peek_previous_moves(player)
    previous_opponent_moves = peek_previous_moves(opponent)

    if previous_player_moves is None:
        previous_player_moves = 2 * player_moves

    if previous_opponent_moves is None:
        previous_opponent_moves = 2 * opponent_moves

    if player_moves == 0:
        return float("-inf")
    if opponent_moves == 0:
        return float("inf")

    if player_moves >= opponent_moves:
        return float((player_moves / opponent_moves) + (previous_opponent_moves - opponent_moves))
    else:
        return float(-(opponent_moves / player_moves) + (previous_opponent_moves - opponent_moves))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # return score_1(game, player)
    # return score_2(game, player)
    # return score_3(game, player)
    # return score_4(game, player)
    return score_5(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if len(legal_moves) == 0:
            return -1, -1

        move_number = random.randint(0, len(legal_moves) - 1)
        initial_move = legal_moves[move_number]

        best_move = None
        depth = self.search_depth

        if self.iterative:
            depth = 1

        method_fn = None
        if self.method == 'minimax':
            method_fn = self.minimax
        if self.method == 'alphabeta':
            method_fn = self.alphabeta

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring

            value, move = method_fn(game, depth, True)
            best_value = value
            best_move = move
            while self.iterative:
                depth += 1
                value, move = method_fn(game, depth, True)
                if value > best_value:
                    best_value, best_move = value, move

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        global previous_moves
        previous_moves = {}

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        player = game.active_player
        opponent = game.inactive_player

        def max_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            if game.is_winner(player) or game.is_loser(player) or depth == 0:
                return self.score(game, player), (-1, -1)
            value = float("-inf")
            best_move = (-1, -1)
            moves = game.get_legal_moves()
            push_previous_moves(player, len(moves))
            for move in moves:
                advance_game = game.forecast_move(move)
                game_value, game_move = min_value(advance_game, depth - 1)
                if value < game_value:
                    value, best_move = game_value, move
            pop_previous_moves(player)
            return value, best_move

        def min_value(game, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            if game.is_winner(player) or game.is_loser(player) or depth == 0:
                return self.score(game, player), (-1, -1)
            value = float("inf")
            best_move = (-1, -1)
            moves = game.get_legal_moves()
            # moves = game.get_legal_moves(self)
            push_previous_moves(player, len(moves))
            for move in moves:
                advance_game = game.forecast_move(move)
                game_value, game_move = max_value(advance_game, depth - 1)
                if value > game_value:
                    value, best_move = game_value, move
            pop_previous_moves(player)
            return value, best_move

        best_value, best_move = float("-inf"), (-1, -1)
        moves = game.get_legal_moves()
        for move in moves:
            advance_game = game.forecast_move(move)
            game_value, game_move = min_value(advance_game, depth - 1)
            if best_value < game_value:
                best_value, best_move = game_value, move

        return best_value, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        global previous_moves
        previous_moves = {}

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        player = game.active_player
        opponent = game.inactive_player

        def max_value(game, alpha, beta, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            if game.is_winner(player) or game.is_loser(player) or depth == 0:
                return self.score(game, player), (-1, -1)
            value = float("-inf")
            best_move = (-1, -1)
            moves = game.get_legal_moves()
            push_previous_moves(player, len(moves))
            for move in moves:
                advance_game = game.forecast_move(move)
                game_value, game_move = min_value(advance_game, alpha, beta, depth - 1)
                if value < game_value:
                    value, best_move = game_value, move
                if value >= beta:
                    return value, best_move
                alpha = max(alpha, value)
            pop_previous_moves(player)
            return value, best_move

        def min_value(game, alpha, beta, depth):
            if self.time_left() < self.TIMER_THRESHOLD:
                raise Timeout()

            if game.is_winner(player) or game.is_loser(player) or depth == 0:
                return self.score(game, player), (-1, -1)
            value = float("inf")
            best_move = (-1, -1)
            moves = game.get_legal_moves()
            # moves = game.get_legal_moves(self)
            push_previous_moves(player, len(moves))
            for move in moves:
                advance_game = game.forecast_move(move)
                game_value, game_move = max_value(advance_game, alpha, beta, depth - 1)
                if value > game_value:
                    value, best_move = game_value, move
                if value <= alpha:
                    return value, best_move
                beta = min(beta, value)
            pop_previous_moves(player)
            return value, best_move

        best_value, best_move = float("-inf"), (-1, -1)
        moves = game.get_legal_moves()
        beta = float("inf")
        for move in moves:
            advance_game = game.forecast_move(move)
            game_value, game_move = min_value(advance_game, best_value, beta, depth - 1)
            # print(game_value, game_move)
            if best_value < game_value:
                best_value, best_move = game_value, move

        return best_value, best_move


def pop_previous_moves(player):
    """
    Pop number of previous moves for a player from a stack
    :param player: player
    :return: number of previous moves of a player
    """
    global previous_moves
    if player not in previous_moves:
        return
    moves = previous_moves[player].pop()
    return moves


def peek_previous_moves(player):
    """
    Peeks the top number of previous moves for a player on a stack
    :param player: player
    :return: top number of previous moves of a player
    """
    global previous_moves
    if player not in previous_moves:
        return
    moves = previous_moves[player][-1]
    return moves


def push_previous_moves(player, number_of_moves):
    """
    Pushes number of previous moves for a player to a stack
    :param player: player
    :param number_of_moves: number of moves
    """
    global previous_moves
    if player not in previous_moves:
        previous_moves[player] = []
    previous_moves[player].append(number_of_moves)

