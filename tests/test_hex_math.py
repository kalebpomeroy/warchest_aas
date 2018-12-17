from warchest.hexes import Hex


def test_get_neighbor():
    assert Hex((0, 0, 0)).neighbor('n') == Hex((0, -1, 1))
    assert Hex((0, -1, 1)).neighbor('nw') == Hex((-1, -1, 2))
    assert Hex((0, -3, 3)).neighbor('n') is None


def test_get_distance():
    assert Hex((0, 0, 0)).distance(Hex((0, -1, 1))) == 1
    assert Hex((0, 0, 0)).distance(Hex((-1, -1, 2))) == 2
    assert Hex((2, 0, -2)).distance(Hex((3, -3, 0))) == 3


def test_within_n():
    assert len(Hex((0, 0, 0)).hexes_within_n(2)) == 18
    assert len(Hex((0, 0, 0)).hexes_within_n(1)) == 6
    assert Hex((2, -3, 1)) not in Hex((0, -2, 2)).hexes_within_n(1)
    assert Hex((2, -3, 1)) in Hex((0, -2, 2)).hexes_within_n(2)

    assert len(Hex((0, 0, 0)).hexes_within_n(2, at_least=2)) == 12
