# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the HistoryStepIterator class.

See its documentation for more information.
'''


import copy

import garlicsim
from garlicsim.misc import BaseStepIterator, SimpackError, AutoClockGenerator


class HistoryStepIterator(BaseStepIterator):
    '''
    An iterator that uses a simpack's step to produce states.
    
    The StepIterator uses under the hood the simpack's step function, be it a
    simple step function or a step generator. Using a StepIterator instead of
    using the simpack's step has a few advantages:
    
    1. The StepIterator automatically adds clock readings if the states are
       missing them.
    2. It's possible to change the step profile while iterating.    
    3. Unless the step function raises `WorldEnd` to end the simulation, this
       iterator is guaranteed to be infinite, even if the simpack's iterator is
       finite.
    
    And possibly more.  
    '''
    # todo: make stuff private here?
    def __init__(self, history_browser, step_profile):

        self.history_step_function = step_profile.step_function
        
        self.raw_iterator = None
        
        self.step_profile = copy.deepcopy(step_profile)
        
        self.current_state = None
        self.history_browser = state_or_history_browser
            
        self.auto_clock_generator = AutoClockGenerator()
            
        self.step_profile_changed = False
            
    def __iter__(self): return self
    
    def next(self):
        '''Crunch the next state.'''
        self.current_state = self.__get_new_state()
        self.auto_clock(self.current_state)
        return self.current_state
        
    def __get_new_state(self): # todo: rename?
        '''Internal method to crunch the next state.'''
        if self.simple_step:
            thing = self.history_browser if self.history_dependent else \
                  self.current_state
            return self.simple_step(thing,
                                    *self.step_profile.args,
                                    **self.step_profile.kwargs)
        else: # self.step_generator is not None
            self.rebuild_raw_iterator_if_necessary()
            try:
                return self.raw_iterator.next()
            except StopIteration:
                try:
                    self.rebuild_raw_iterator()
                    return self.raw_iterator.next()
                except StopIteration:
                    raise SimpackError('''Step generator's iterator raised
StopIteration before producing a single state.''')
            
                
    def rebuild_raw_iterator_if_necessary(self):
        '''
        Rebuild the internal iterator if necessary.
        
        This is relevant only when we're using a simpack's step generator and
        not its simple step.
        '''
        if (self.raw_iterator is None) or self.step_profile_changed:
            self.rebuild_raw_iterator()
            self.step_profile_changed = False
            
            
    def rebuild_raw_iterator(self):
        '''
        Rebuild the internal iterator.
        
        This is relevant only when we're using a simpack's step generator and
        not its simple step.
        '''
        thing = self.current_state or self.history_browser
        self.raw_iterator = self.step_generator(thing,
                                                *self.step_profile.args,
                                                **self.step_profile.kwargs)
                
        
    def auto_clock(self, state):
        '''If the state has no clock reading, give it one automatically.'''
        state.clock = self.auto_clock_generator.make_clock(state)
        
        
    def set_step_profile(self, step_profile):
        '''
        Set a new step profile for the StepIterator to use.

        The StepIterator will immediately adopt the new step profile, and any
        states that will be crunched from this point on will be crunched using
        the new step profile. (At least until it is changed again.)
        '''
        self.step_profile = copy.deepcopy(step_profile)
        self.step_profile_changed = True
        

    
