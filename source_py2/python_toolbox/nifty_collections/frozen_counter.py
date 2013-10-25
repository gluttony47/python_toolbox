# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import operator
import _heapq
import itertools
import collections

from .frozen_dict import FrozenDict


class FrozenCounter(FrozenDict):
    '''
    An immutable counter.
    
    A counter that can't be changed. The advantage of this over
    `collections.Counter` is mainly that it's hashable, and thus can be used as
    a key in dicts and sets.
    
    In other words, `FrozenCounter` is to `Counter` what `frozenset` is to
    `set`.
    '''
    
    def __init__(self, iterable=None, **kwargs):
        '''Create a new, empty Counter object.  And if given, count elements
        from an input iterable.  Or, initialize the count from another mapping
        of elements to their counts.

        >>> c = Counter()                           # a new, empty counter
        >>> c = Counter('gallahad')                 # a new counter from an iterable
        >>> c = Counter({'a': 4, 'b': 2})           # a new counter from a mapping
        >>> c = Counter(a=4, b=2)                   # a new counter from keyword args

        '''
        super(FrozenCounter, self).__init__()
        
        if iterable is not None:
            if isinstance(iterable, collections.Mapping):
                if self:
                    self_get = self.get
                    for elem, count in iterable.iteritems():
                        self[elem] = self_get(elem, 0) + count
                else:
                    super(FrozenCounter, self).update(iterable) # fast path when counter is empty
            else:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1
        if kwargs:
            self.update(kwargs)


    def __missing__(self, key):
        'The count of elements not in the FrozenCounter is zero.'
        # Needed so that self[missing_item] does not raise KeyError
        return 0

    def most_common(self, n=None):
        '''List the n most common elements and their counts from the most
        common to the least.  If n is None, then list all element counts.

        >>> FrozenCounter('abcdeabcdabcaba').most_common(3)
        [('a', 5), ('b', 4), ('c', 3)]

        '''
        # Emulate Bag.sortedByCount from Smalltalk
        if n is None:
            return sorted(self.iteritems(), key=operator.itemgetter(1),
                          reverse=True)
        return _heapq.nlargest(n, self.iteritems(), key=operator.itemgetter(1))

    def elements(self):
        '''Iterator over elements repeating each as many times as its count.

        >>> c = FrozenCounter('ABCABC')
        >>> sorted(c.elements())
        ['A', 'A', 'B', 'B', 'C', 'C']

        # Knuth's example for prime factors of 1836:  2**2 * 3**3 * 17**1
        >>> prime_factors = FrozenCounter({2: 2, 3: 3, 17: 1})
        >>> product = 1
        >>> for factor in prime_factors.elements():     # loop over factors
        ...     product *= factor                       # and multiply them
        >>> product
        1836

        Note, if an element's count has been set to zero or is a negative
        number, elements() will ignore it.

        '''
        # Emulate Bag.do from Smalltalk and Multiset.begin from C++.
        return itertools.chain.from_iterable(
            itertools.starmap(itertools.repeat, self.iteritems())
        )

    # Override dict methods where necessary

    @classmethod
    def fromkeys(cls, iterable, v=None):
        # There is no equivalent method for counters because setting v=1
        # means that no element can have a count greater than one.
        raise NotImplementedError(
            'FrozenCounter.fromkeys() is undefined. Use '
            'FrozenCounter(iterable) instead.'
        )

    def __repr__(self):
        if not self:
            return '%s()' % self.__class__.__name__
        items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
        return '%s({%s})' % (self.__class__.__name__, items)

    # Multiset-style mathematical operations discussed in:
    #       Knuth TAOCP Volume II section 4.6.3 exercise 19
    #       and at http://en.wikipedia.org/wiki/Multiset
    #
    # Outputs guaranteed to only include positive counts.
    #
    # To strip negative and zero counts, add-in an empty counter:
    #       c += FrozenCounter()

    def __add__(self, other):
        '''Add counts from two counters.

        >>> FrozenCounter('abbb') + FrozenCounter('bcc')
        FrozenCounter({'b': 4, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, FrozenCounter):
            return NotImplemented
        result = collections.Counter()
        for elem, count in self.items():
            newcount = count + other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return FrozenCounter(result)

    def __sub__(self, other):
        ''' Subtract count, but keep only results with positive counts.

        >>> FrozenCounter('abbbc') - FrozenCounter('bccd')
        FrozenCounter({'b': 2, 'a': 1})

        '''
        if not isinstance(other, FrozenCounter):
            return NotImplemented
        result = collections.Counter()
        for elem, count in self.items():
            newcount = count - other[elem]
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count < 0:
                result[elem] = 0 - count
        return FrozenCounter(result)

    def __or__(self, other):
        '''Union is the maximum of value in either of the input counters.

        >>> FrozenCounter('abbb') | FrozenCounter('bcc')
        FrozenCounter({'b': 3, 'c': 2, 'a': 1})

        '''
        if not isinstance(other, FrozenCounter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = other_count if count < other_count else count
            if newcount > 0:
                result[elem] = newcount
        for elem, count in other.items():
            if elem not in self and count > 0:
                result[elem] = count
        return FrozenCounter(result)

    def __and__(self, other):
        ''' Intersection is the minimum of corresponding counts.

        >>> FrozenCounter('abbb') & FrozenCounter('bcc')
        FrozenCounter({'b': 1})

        '''
        if not isinstance(other, FrozenCounter):
            return NotImplemented
        result = Counter()
        for elem, count in self.items():
            other_count = other[elem]
            newcount = count if count < other_count else other_count
            if newcount > 0:
                result[elem] = newcount
        return FrozenCounter(result)