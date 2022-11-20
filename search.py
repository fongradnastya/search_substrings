import logging

from builtins import object


class State(object):
    __slots__ = ['identifier', 'symbol', 'success', 'transitions', 'parent',
                 'matched_keyword', 'longest_strict_suffix']

    def __init__(self, identifier, symbol=None, parent=None, success=False):
        self.symbol = symbol
        self.identifier = identifier
        self.transitions = {}
        self.parent = parent
        self.success = success
        self.matched_keyword = None
        self.longest_strict_suffix = None

    def __str__(self):
        transitions_as_string = ','.join(
            ['{0} -> {1}'.format(key, value.identifier) for key, value in
             self.transitions.items()])
        return "State {0}. Transitions: {1}".format(self.identifier,
                                                    transitions_as_string)


class KeywordTree(object):

    def __init__(self):
        '''
        @param over_allocation: Determines how big initial transition arrays
                                are and how much space is allocated in addition
                                to what is essential when array needs to be
                                resized. Default value 2 seemed to be sweet
                                spot for memory as well as cpu.
        '''
        self._zero_state = State(0)
        self._counter = 1
        self._finalized = False

    def add(self, keyword):
        '''
        Add a keyword to the tree.
        Can only be used before finalize() has been called.
        Keyword should be str or unicode.
        '''
        if self._finalized:
            raise ValueError('KeywordTree has been finalized.' +
                             ' No more keyword additions allowed')
        original_keyword = keyword
        if len(keyword) <= 0:
            return
        current_state = self._zero_state
        for char in keyword:
            try:
                current_state = current_state.transitions[char]
            except KeyError:
                next_state = State(self._counter, parent=current_state,
                                   symbol=char)
                self._counter += 1
                current_state.transitions[char] = next_state
                current_state = next_state
        current_state.success = True
        current_state.matched_keyword = original_keyword

    def finalize(self):
        '''
        Needs to be called after all keywords have been added and
        before any searching is performed.
        '''
        if self._finalized:
            raise ValueError('KeywordTree has already been finalized.')
        self._zero_state.longest_strict_suffix = self._zero_state
        self.search_lss_for_children(self._zero_state)
        self._finalized = True

    def search_lss_for_children(self, zero_state):
        processed = set()
        to_process = [zero_state]
        while to_process:
            state = to_process.pop()
            processed.add(state.identifier)
            for child in state.transitions.values():
                if child.identifier not in processed:
                    self.search_lss(child)
                    to_process.append(child)

    def search_lss(self, state):
        zero_state = self._zero_state
        parent = state.parent
        traversed = parent.longest_strict_suffix
        while True:
            if state.symbol in traversed.transitions and \
                    traversed.transitions[state.symbol] is not state:
                state.longest_strict_suffix = \
                    traversed.transitions[state.symbol]
                break
            elif traversed is zero_state:
                state.longest_strict_suffix = zero_state
                break
            else:
                traversed = traversed.longest_strict_suffix
        suffix = state.longest_strict_suffix
        if suffix is zero_state:
            return
        if suffix.longest_strict_suffix is None:
            self.search_lss(suffix)
        for symbol, next_state in suffix.transitions.items():
            if symbol not in state.transitions:
                state.transitions[symbol] = next_state

    def __str__(self):
        return "ahocorapy KeywordTree"

    def __getstate__(self):
        state_list = [None] * self._counter
        todo_list = [self._zero_state]
        while todo_list:
            state = todo_list.pop()
            transitions = {key: value.identifier for key,
                                                     value in
                           state.transitions.items()}
            state_list[state.identifier] = {
                'symbol': state.symbol,
                'success': state.success,
                'parent': state.parent.identifier if state.parent is not None else None,
                'matched_keyword': state.matched_keyword,
                'longest_strict_suffix': state.longest_strict_suffix.identifier if state.longest_strict_suffix is not None else None,
                'transitions': transitions
            }
            for child in state.transitions.values():
                if len(state_list) <= child.identifier or not \
                        state_list[child.identifier]:
                    todo_list.append(child)

        return {
            'finalized': self._finalized,
            'counter': self._counter,
            'states': state_list
        }

    def __setstate__(self, state):
        self._counter = state['counter']
        self._finalized = state['finalized']
        states = [None] * len(state['states'])
        for idx, serialized_state in enumerate(state['states']):
            deserialized_state = State(idx, serialized_state['symbol'])
            deserialized_state.success = serialized_state['success']
            deserialized_state.matched_keyword = serialized_state[
                'matched_keyword']
            states[idx] = deserialized_state
        for idx, serialized_state in enumerate(state['states']):
            deserialized_state = states[idx]
            if serialized_state['longest_strict_suffix'] is not None:
                deserialized_state.longest_strict_suffix = states[
                    serialized_state['longest_strict_suffix']]
            else:
                deserialized_state.longest_strict_suffix = None
            if serialized_state['parent'] is not None:
                deserialized_state.parent = states[serialized_state['parent']]
            else:
                deserialized_state.parent = None
            deserialized_state.transitions = {
                key: states[value] for key, value in
                serialized_state['transitions'].items()}
        self._zero_state = states[0]


def search(string, sub_string, case_sensitivity=False, method='first',
           count=None):
    tree = KeywordTree()
    if not case_sensitivity:
        string = string.lower()
        if isinstance(sub_string, tuple):
            sub_string = list(sub_string)
            for i in range(len(sub_string)):
                sub_string[i] = sub_string[i].lower()
            sub_string = tuple(sub_string)
        else:
            sub_string = sub_string.lower()
    if isinstance(sub_string, tuple):
        for item in sub_string:
            tree.add(item)
    else:
        tree.add(sub_string)
    tree.finalize()
    zero_state = tree._zero_state
    current_state = zero_state
    found = dict()
    if isinstance(sub_string, tuple):
        for item in sub_string:
            found[item] = []
    else:
        found[sub_string] = []
    items = []
    for idx, symbol in enumerate(string):
        current_state = current_state.transitions.get(
            symbol, zero_state.transitions.get(symbol, zero_state))
        state = current_state
        while state is not zero_state:
            if state.success:
                keyword = state.matched_keyword
                idn = idx + 1 - len(keyword)
                items.append((keyword, idn))
            state = state.longest_strict_suffix
    if items:
        if method == 'last':
            items = items[::-1]
        if count and len(items) > count:
            items = items[:count]
    else:
        return None
    if not isinstance(sub_string, tuple):
        t = []
        for i in items:
            t.append(i[1])
        return tuple(t)
    else:
        found = dict()
        for str in sub_string:
            found[str] = []
        for i in items:
            found[i[0]].append(i[1])
        for key, value in found.items():
            if not value:
                found[key] = None
            else:
                found[key] = tuple(value)
        return found
