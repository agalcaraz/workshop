import geom_analysis as ga

def test_calculate_distance():
    coord1 = [0, 0, 0]
    coord2 = [1, 0, 0]
    expected = 1.0
    observed = ga.calculate_distance(coord1,coord2)
    assert observed == expected

def test_bond_check():
    bond_distance = 1.5
    expected = True
    observed = ga.bond_check(bond_distance)
    assert observed == expected

