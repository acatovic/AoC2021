from pathlib import Path
import sys
from typing import List, Tuple

import numpy as np  # type: ignore


def calc_winning_score(board: np.ndarray, last_draw: float) -> float:
    board = update_board_is_bingo(board)
    return last_draw * sum(board.flatten())

def is_bingo(board: np.ndarray) -> bool:
    for i in range(5):
        if np.all(board[:, i] == np.inf) or np.all(board[i, :] == np.inf):
            return True
    return False

def load_data(path: str) -> Tuple[List[float], np.ndarray]:
    """Return tuple (draws, boards). """
    boards = []
    with Path(path).open() as f:
        draws = list(map(float, next(f).strip().split(',')))
        for line in f:
            line = line.strip()
            if not line:
                board = np.zeros((5, 5))
                for i in range(5):
                    board[i] = np.array(list(map(float, next(f).split())))
                boards.append(board)

    return draws, boards

def play_bingo(draws: List[float], boards: List[np.ndarray]) -> Tuple[float, np.ndarray]:
    """Return tuple (last_draw, winning_board)."""
    for draw in draws:
        for i in range(len(boards)):
            boards[i] = update_board(boards[i], draw)
            if is_bingo(boards[i]):
                return draw, boards[i]

def play_bingo_last_board_wins(draws: List[float], boards: List[np.ndarray]) -> Tuple[float, np.ndarray]:
    """Return tuple (last_draw, winning_board)."""
    winning_boards = []
    winning_draws = []
    for draw in draws:
        for i in range(len(boards)):
            if i in winning_boards:
                continue
            boards[i] = update_board(boards[i], draw)
            if is_bingo(boards[i]):
                winning_boards.append(i)
                winning_draws.append(draw)
    
    return winning_draws[-1], boards[winning_boards[-1]]

def update_board(board: np.ndarray, draw: float) -> np.ndarray:
    return np.where(board == draw, np.inf, board)

def update_board_is_bingo(board: np.ndarray) -> np.ndarray:
    return np.where(board == np.inf, 0, board)

def main():
    draws, boards = load_data(sys.argv[1])
    
    # lets play bingo!
    last_draw, winning_board = play_bingo_last_board_wins(draws, boards)
    winning_score = calc_winning_score(winning_board, last_draw)
    print(winning_score)


if __name__ == '__main__':
    main()