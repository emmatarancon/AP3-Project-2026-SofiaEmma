#!/usr/bin/env python3
"""Makes a sanity check of a solution.

Usage: checker.py INPUT_FILE OUTPUT_FILE

Python port of checker.cc. Prints "OK" and exits with status 0 if the
solution is valid; otherwise prints an error message followed by "FAILED"
and exits with status 1.
"""

import sys


class Instance:
    def __init__(self, path):
        with open(path) as f:
            tokens = f.read().split()
        it = iter(tokens)

        P = int(next(it))
        self.films = [next(it) for _ in range(P)]          # I2P
        self.film_id = {name: k for k, name in enumerate(self.films)}  # P2I

        self.adj = [[] for _ in range(P)]                  # g
        L = int(next(it))
        for _ in range(L):
            sp, sq = next(it), next(it)
            assert sp in self.film_id, f"unknown film {sp} in input"
            assert sq in self.film_id, f"unknown film {sq} in input"
            p, q = self.film_id[sp], self.film_id[sq]
            self.adj[p].append(q)
            self.adj[q].append(p)

        S = int(next(it))
        self.cinemas = [next(it) for _ in range(S)]        # I2S
        self.cinema_id = {name: k for k, name in enumerate(self.cinemas)}  # S2I


def read_solution(path, inst):
    """Returns (obj, sol) where sol[p] = (day, cinema), or None on error."""
    with open(path) as f:
        tokens = f.read().split()

    # Header: time and objective value.
    try:
        float(tokens[0])
        obj = int(tokens[1])
    except (IndexError, ValueError):
        obj = 0

    sol = [None] * len(inst.films)
    cnt = 0
    i = 2
    while i + 3 <= len(tokens):
        sp, sd, ss = tokens[i], tokens[i + 1], tokens[i + 2]
        i += 3
        try:
            d = int(sd)
        except ValueError:
            break  # Like a failed stream extraction in C++: stop reading.

        p = inst.film_id.get(sp)
        if p is None:
            print(f"Error: didn't recognize {sp}")
            return None

        s = inst.cinema_id.get(ss)
        if s is None:
            print(f"Error: didn't recognize {ss}")
            return None

        if d <= 0:
            print(f"Error: wrong day identifier {d}")
            return None

        if sol[p] is not None:
            print(f"Error: repeated film {sp}")
            return None
        sol[p] = (d, s)
        cnt += 1

    if cnt < len(inst.films):
        print("Error: read too few films")
        return None

    return obj, sol


def solution_ok(inst, obj, sol):
    films = inst.films
    n = len(sol)

    # Incompatible films must not be projected on the same day.
    for p in range(n):
        for q in inst.adj[p]:
            if p < q and sol[p][0] == sol[q][0]:
                print(f"Error: films {films[p]} and {films[q]} "
                      f"are projected on the same day but should not")
                return False

    # No two films on the same day in the same cinema.
    # Report the same pair as the O(n^2) loop in checker.cc would:
    # the smallest p that has a clash, together with its first clashing q.
    clash = None
    groups = {}
    for k in range(n):
        groups.setdefault(sol[k], []).append(k)
    for idx in groups.values():
        if len(idx) >= 2 and (clash is None or idx[0] < clash[0]):
            clash = (idx[0], idx[1])
    if clash is not None:
        p, q = clash
        print(f"Error: films {films[p]} and {films[q]} "
              f"are projected on the same day in the same cinema")
        return False

    max_days = max([1] + [d for d, _ in sol])
    if max_days != obj:
        print(f"Error: length of festival is {max_days} but should be {obj}")
        return False

    return True


def main():
    if len(sys.argv) != 3:
        print("Makes a sanity check of a solution")
        print(f"Usage: {sys.argv[0]} INPUT_FILE OUTPUT_FILE")
        sys.exit(0)

    inst = Instance(sys.argv[1])
    res = read_solution(sys.argv[2], inst)
    if res is None:
        print("FAILED")
        sys.exit(1)

    obj, sol = res
    if solution_ok(inst, obj, sol):
        print("OK")
        sys.exit(0)
    else:
        print("FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
