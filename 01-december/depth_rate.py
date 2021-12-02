from pathlib import Path
import sys
from typing import List

def count_num_depth_increases(data: List[int]) -> int:
    curr_depth = data[0]
    num_increases = 0
    for i in range(1, len(data)):
        if data[i] > curr_depth:
            num_increases += 1
        curr_depth = data[i]
    return num_increases

def count_num_depth_window_increases(data: List[int], window_size: int = 3) -> int:
    curr_window_sum = sum(data[:window_size])
    num_increases = 0
    for i in range(1, len(data) - window_size + 1):
        next_window_sum = sum(data[i:i + window_size])
        if next_window_sum > curr_window_sum:
            num_increases += 1
        curr_window_sum = next_window_sum
    return num_increases

def load_sonar_data(path: str) -> List[int]:
    data = []
    with Path(path).open() as f:
        for line in f:
            data.append(int(line.strip()))
    return data

def main():
    path = sys.argv[1]
    data = load_sonar_data(path)
    print(count_num_depth_window_increases(data))

if __name__ == "__main__":
    main()