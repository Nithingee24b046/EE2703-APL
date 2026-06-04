#!/usr/bin/env python3
"""
Keyboard Layout Optimization via Simulated Annealing

Notes:
- Cost is total Euclidean distance between consecutive characters.
- Coordinates are fixed (QWERTY-staggered grid). Optimization swaps assignments.

This base code uses Python "types" - these are optional, but very helpful
for debugging and to help with editing.

"""

import argparse
import json
import math
import os
import random
import string
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt  # type: ignore


Point = Tuple[float, float]
Layout = Dict[str, Point]


def qwerty_coordinates(chars: str) -> Layout:
    """Return QWERTY grid coordinates for the provided character set.

    The grid is a simple staggered layout (units are arbitrary):
    - Row 0: qwertyuiop at y=0, x in [0..9]
    - Row 1: asdfghjkl at y=1, x in [0.5..8.5]
    - Row 2: zxcvbnm at y=2, x in [1..6]
    - Space at (4.5, 3)
    Characters not present in the grid default to the space position.
    """
    row0 = "qwertyuiop"
    row1 = "asdfghjkl"
    row2 = "zxcvbnm"

    coords: Layout = {}
    for i, c in enumerate(row0):
        coords[c] = (float(i), 0.0)
    for i, c in enumerate(row1):
        coords[c] = (0.5 + float(i), 1.0)
    for i, c in enumerate(row2):
        coords[c] = (1.0 + float(i), 2.0)
    coords[" "] = (4.5, 3.0)

    # Backfill for requested chars; unknowns get space position.
    space_xy = coords[" "]
    for ch in chars:
        if ch not in coords:
            coords[ch] = space_xy
    return coords


def initial_layout() -> Layout:
    """Create an initial layout mapping chars to some arbitrary positions of letters."""

    # Start with identity for letters and space; others mapped to space.
    base_keys = "abcdefghijklmnopqrstuvwxyz "

    # Get coords - or use coords of space as default
    layout = qwerty_coordinates(base_keys)
    return layout


def preprocess_text(text: str, chars: str) -> str:
    """Lowercase and filter to the allowed character set; map others to space."""
    
    preprocessed_content=''
    for ch in text.lower():
        if ch not in chars:
            preprocessed_content += ' '
        else:
            preprocessed_content += ch

    return preprocessed_content


def path_length_cost(text: str, layout: Layout) -> float:
    """Sum Euclidean distances across consecutive characters in text."""
    path_cost = 0
    text_length = len(text)

    for i in range(text_length - 1):
        path_cost += math.dist(layout[text[i]],layout[text[i+1]])
    
    return path_cost



######
# Define any other useful functions, such as to create new layout etc.
######


# Dataclass is like a C struct - you can use it just to store data if you wish
# It provides some convenience functions for assignments, printing etc.
@dataclass
class SAParams:
    iters: int = 50000
    t0: float = 1.0  # Initial temperature setting
    alpha: float = 0.999  # geometric decay per iteration
    epoch: int = 1  # iterations per temperature step (1 = per-iter decay)


def simulated_annealing(
    text: str,
    layout: Layout,
    params: SAParams,
    rng: random.Random,
) -> Tuple[Layout, float, List[float], List[float]]:
    """Simulated annealing to minimize path-length cost over character swaps.

    Returns best layout, best cost, and two lists:
    - best cost up to now (monotonically decreasing)
    - cost of current solution (may occasionally go up)
    These will be used for plotting
    """
    #Getting the parameters from the class
    number_iterations=params.iters
    t0=params.t0
    alpha=params.alpha

    prev_layout=layout.copy()
    current_layout={}
    optimized_layout = {}

    keys_layout=list(layout.keys())

    min_cost_list=[]
    actual_cost_list=[]

    min_cost=prev_cost=path_length_cost(text,prev_layout) # Initialize the initial cost
    
    for i in range(number_iterations):
        #Updating the temperature after every iteration
        T=t0*(alpha**i)

        current_layout=prev_layout.copy()

        #Swap 2 random keys
        key1,key2=rng.sample(keys_layout,2) 
        current_layout[key1],current_layout[key2]=current_layout[key2],current_layout[key1]

        current_cost=path_length_cost(text,current_layout)
        
        min_cost=min(min_cost,current_cost) #Updating the minimum cost
        if min_cost == current_cost:
            optimized_layout = current_layout

        
        delta=current_cost-prev_cost #Defining delta parameter

        #Simulated annealing algorithm
        if delta<0:
            prev_layout=current_layout
            prev_cost=current_cost
        else:
            probability=math.exp(-delta/T)
            if rng.random()<probability:
                prev_layout=current_layout
                prev_cost=current_cost
        
        #Updating the lists to be shown in plots
        min_cost_list.append(min_cost)
        actual_cost_list.append(prev_cost)

    return (optimized_layout,min_cost,min_cost_list,actual_cost_list)

def plot_costs(
    layout: Layout, best_trace: List[float], current_trace: List[float]
) -> None:

    # Plot cost trace
    out_dir = "."
    plt.figure(figsize=(6, 3))
    plt.plot(best_trace, lw=1.5)
    plt.plot(current_trace, lw=1.5)
    plt.xlabel("Iteration")
    plt.ylabel("Best Cost")
    plt.title("Best Cost vs Iteration")
    plt.tight_layout()
    path = os.path.join(out_dir, f"cost_trace.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")

    # Plot layout scatter
    xs, ys, labels = [], [], []
    for ch, (x, y) in layout.items():
        xs.append(x)
        ys.append(y)
        labels.append(ch)

    plt.figure(figsize=(6, 3))
    plt.scatter(xs, ys, s=250, c="#1f77b4")
    for x, y, ch in zip(xs, ys, labels):
        plt.text(
            x,
            y,
            ch,
            ha="center",
            va="center",
            color="white",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.15", fc="#1f77b4", ec="none", alpha=0.9),
        )
    plt.gca().invert_yaxis()
    plt.title("Optimized Layout")
    plt.axis("equal")
    plt.tight_layout()
    path = os.path.join(out_dir, f"layout.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def load_text(filename) -> str:
    if filename is not None:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback demo text
    return (
        "the quick brown fox jumps over the lazy dog\n"
        "APL is the best course ever\n"
    )


def main(filename: str | None = None) -> None:
    rng = random.Random(0)
    chars = "abcdefghijklmnopqrstuvqxyz "

    iters = 100 #Created by me

    # Initial assignment - QWERTY
    layout0 = initial_layout()

    # Prepare text and evaluate baseline
    raw_text = load_text(filename)
    text = preprocess_text(raw_text, chars)

    baseline_cost = path_length_cost(text, layout0)
    print(f"Baseline (QWERTY assignment) cost: {baseline_cost:.4f}")

    # Annealing - give parameter values
    params = SAParams(iters= 100 , t0= 1 , alpha= 0.99) #Values by me
    start = time.time()
    best_layout, best_cost, best_trace, current_trace = simulated_annealing(text, layout0, params, rng)
    dur = time.time() - start
    print(f"Optimized cost: {best_cost:.4f}  (improvement {(baseline_cost - best_cost):.4f})")
    print(f"Runtime: {dur:.2f}s over {iters} iterations")

    plot_costs(best_layout, best_trace, current_trace)


if __name__ == "__main__":
    main("long_text.txt")