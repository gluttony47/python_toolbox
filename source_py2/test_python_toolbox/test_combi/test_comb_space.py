# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import sequence_tools

from python_toolbox.combi import *


def test():
    comb_space = CombSpace('dumber', 2)
    assert isinstance(comb_space, CombSpace)
    assert isinstance(comb_space, PermSpace)
    assert comb_space.length == 1 + 2 + 3 + 4 + 5
    things_in_comb_space = (
        'du', 'db', 'br', ('d', 'u'), {'d', 'u'}, Comb('du', comb_space)
    )
    things_not_in_comb_space = (
        'dx', 'dub', ('d', 'x'), {'d', 'u', 'b'}, Comb('dux', comb_space),
        Comb('du', CombSpace('other', 2))
    )
    
    for thing in things_in_comb_space:
        assert thing in comb_space
    for thing in things_not_in_comb_space:
        assert thing not in comb_space
    
    assert comb_space.n_unused_elements == 4
    assert comb_space.index('du') == 0
    assert comb_space.index('er') == comb_space.length - 1
    assert comb_space.undapplied == comb_space
    assert comb_space.unrapplied == CombSpace(6, 2)
    assert comb_space.unpartialled == CombSpace('dumber', 6)
    assert comb_space.unpartialled.get_partialled(5) == CombSpace('dumber', 5)
    assert comb_space.uncombinationed == PermSpace('dumber', n_elements=2)
    assert comb_space.undegreed == comb_space
    assert comb_space.unrapplied.get_rapplied(range(10, 70, 10)) == \
                                                CombSpace(range(10, 70, 10), 2)
    with cute_testing.RaiseAssertor():
        comb_space.undapplied.get_dapplied(range(10, 70, 10))
    with cute_testing.RaiseAssertor():
        comb_space.get_degreed(3)
    assert comb_space.unfixed == comb_space
    assert not comb_space.fixed_indices
    assert comb_space.free_indices == comb_space.free_keys == \
                                                    sequence_tools.CuteRange(2)
    assert comb_space.free_values == 'dumber'
    
    comb = comb_space[7]
    assert type(comb.uncombinationed) is Perm
    assert tuple(comb) == tuple(comb.uncombinationed)
    assert comb.is_combination
    assert not comb.uncombinationed.is_combination
    assert repr(comb_space) == '''<CombSpace: 'dumber', n_elements=2>'''
    assert repr(CombSpace(tuple(range(50, 0, -1)), 3)) == \
     '''<CombSpace: (50, 49, 48, 47, 46, 45, 44, 43, 42 ... ), n_elements=3>'''
    
    
    
    
        