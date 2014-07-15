import collections
import types
import sys
import math
import numbers

from python_toolbox import misc_tools
from python_toolbox import binary_search
from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import caching

from layout_rabbit import shy_math_tools
from layout_rabbit import shy_sequence_tools
from layout_rabbit import shy_cute_iter_tools
from layout_rabbit import shy_nifty_collections

from . import misc
from layout_rabbit import shy_misc_tools

infinity = float('inf')


        
class ProductSpace(shy_sequence_tools.CuteSequenceMixin, collections.Sequence):
    def __init__(self, sequences):
        self.sequences = shy_sequence_tools. \
                               ensure_iterable_is_immutable_sequence(sequences)
        self.sequence_lengths = tuple(map(shy_sequence_tools.get_length,
                                          self.sequences))
        self.length = misc_tools.general_product(self.sequence_lengths)
        
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            ' * '.join(str(shy_sequence_tools.get_length(sequence))
                       for sequence in self.sequences),
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError
        
        if i < 0:
            i += self.length
            
        if not (0 <= i < self.length):
            raise IndexError
        
        wip_i = i
        reverse_indices = []
        for sequence_length in reversed(self.sequence_lengths):
            wip_i, current_index = divmod(wip_i, sequence_length)
            reverse_indices.append(current_index)
        assert wip_i == 0
        return tuple(sequence[index] for sequence, index in
                     zip(self.sequences, reversed(reverse_indices)))
    
        
    _reduced = property(lambda self: (type(self), self.sequences))
             
    __eq__ = lambda self, other: (isinstance(other, ProductSpace) and
                                  self._reduced == other._reduced)
    
    def __contains__(self, given_sequence):
        try:
            self.index(given_sequence)
        except IndexError:
            return False
        else:
            return True
        
    def index(self, given_sequence):
        if not isinstance(given_sequence, collections.Sequence) or \
                                not len(given_sequence) == len(self.sequences):
            raise IndexError
        
        reverse_indices = []
        current_radix = 1
        
        wip_index = 0
            
        for item, sequence in reversed(tuple(zip(given_sequence,
                                                 self.sequences))):
            wip_index += sequence.index(item) # Propagating `IndexError`
            current_radix *= shy_sequence_tools.get_length(sequence)
            
        return wip_index
    
    
    __bool__ = lambda self: bool(self.length)
        

