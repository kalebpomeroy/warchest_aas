# Based on: http://www.redblobgames.com/grids/hexagons/

MAX = 3


class Hex(tuple):
    def __init__(self, coordinates):
        q, r, s = coordinates
        assert (q + r + s == 0), "q + r + s must be 0"
        self.q = q
        self.r = r
        self.s = s

    def __eq__(self, b):
        if b is None:
            return False
        if isinstance(b, list):
            b = Hex(b)
        return self.q == b.q and self.r == b.r and self.s == b.s

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "{}, {}, {}".format(self.q, self.r, self.s)

    def add(self, b):
        if abs(self.q + b.q) > MAX or abs(self.r + b.r) > MAX or abs(self.s + b.s) > MAX:
            return None
        return Hex((self.q + b.q, self.r + b.r, self.s + b.s))

    def subtract(self, b):
        return Hex((self.q - b.q, self.r - b.r, self.s - b.s))

    def neighbor(self, direction):
        return self.add(HEX_DIRECTIONS[direction])

    def diagonal_neighbor(self, direction):
        return self.add(HEX_DIAGONALS[direction])

    def length(self, b):
        return (abs(b.q) + abs(b.r) + abs(b.s)) // 2

    def distance(self, b):
        return self.length(self.subtract(b))

    def hexes_within_n(self, n, at_least=1):

        results = []
        rng = range(- n, n + 1)

        for q in rng:
            for r in rng:
                for s in rng:
                    if q + r + s == 0:
                        if not at_least or (abs(q) >= at_least or abs(r) >= at_least or abs(s) >= at_least):
                            results.append(self.add(Hex((q, r, s))))
        return [r for r in results if r]


HEX_DIRECTIONS = {
    "n": Hex((0, -1, 1)),
    "ne": Hex((1, -1, 0)),
    "se": Hex((1, 0, -1)),
    "s": Hex((0, 1, -1)),
    "sw": Hex((-1, 1, 0)),
    "nw": Hex((-1, 0, 1)),
}

HEX_DIAGONALS = {
    "ne": Hex((1, -2, 1)),
    "e": Hex((2, -1, -1)),
    "se": Hex((1, 1, -2)),
    "sw": Hex((-1, 2, -1)),
    "w": Hex((-2, 1, 1)),
    "nw": Hex((-1, -1, 2)),
}
