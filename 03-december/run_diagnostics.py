from pathlib import Path
import sys
from typing import Tuple

import numpy as np  # type: ignore

def calc_epsilon(gamma_bin: str) -> Tuple[str, int]:
    """Using XOR operation to invert gamma and return binary and decimal form."""
    gamma_dec = int(gamma_bin, base=2)

    # apply XOR operator
    inverse_gamma = gamma_dec ^ (2 ** (len(gamma_bin) + 1) - 1)
    eps_bin = bin(inverse_gamma)[3:]  # slice off '0b1' indicator
    eps_dec = int(eps_bin, base=2)

    return eps_bin, eps_dec

def calc_gamma(data: np.ndarray) -> Tuple[str, int]:
    """Return a tuple consisting of binary form/string and decimal of gamma value."""
    n = np.array([len(data)] * len(data[0]), dtype=int)
    ones = np.count_nonzero(data, axis=0)
    zeros = n - ones
    gamma_bin = ''.join(map(str, (ones > zeros).astype(int)))
    return gamma_bin, int(gamma_bin, base=2)

def calc_co2_scrubber_rating(data: np.ndarray) -> Tuple[str, int]:
    for i in range(data.shape[1]):
        bits = data[:, i]
        ones = bits == 1
        zeros = bits == 0
        if sum(zeros) <= sum(ones):
            data = data[np.where(zeros)[0]]
        else:
            data = data[np.where(ones)[0]]
        bits = data[:, i]
        i += 1
        if len(data) == 1:
            break
    
    data = ''.join(map(str, data.flatten()))
    return data, int(data, base=2)

def calc_oxygen_generator_rating(data: np.ndarray) -> Tuple[str, int]:
    for i in range(data.shape[1]):
        bits = data[:, i]
        ones = bits == 1
        zeros = bits == 0
        if sum(ones) >= sum(zeros):
            data = data[np.where(ones)[0]]
        else:
            data = data[np.where(zeros)[0]]
        bits = data[:, i]
        i += 1
        if len(data) == 1:
            break
    
    data = ''.join(map(str, data.flatten()))
    return data, int(data, base=2)

def load_diagnostics_data(path: str) -> np.ndarray:
    data = []
    with Path(path).open() as f:
        for line in f:
            bits = list(map(int, line.strip()))
            data.append(bits)
    return np.array(data, dtype=int)

def main():
    path = sys.argv[1]
    data = load_diagnostics_data(path)
    #gamma = calc_gamma(data)
    #eps = calc_epsilon(gamma[0])
    #print(f"gamma: {gamma}")
    #print(f"epsilon: {eps}")
    #print(f"power_consumption: {gamma[1] * eps[1]}")
    oxy = calc_oxygen_generator_rating(data)
    co2 = calc_co2_scrubber_rating(data)
    print(oxy)
    print(co2)
    life_support = oxy[1] * co2[1]
    print(life_support)

if __name__ == '__main__':
    main()