
from warnings import warn
from collections import Counter
from enum import Enum
from copy import copy
from weakref import WeakSet, proxy
from uuid import uuid1
from functools import wraps


class TraitBag:
    __slots__ = ["__weakref__", "traits", "bag", "name"]
    
    def __init__(self, name=None, *, 
                 in_traits=(), stereotypes=(), ex_traits=(), bag=()):
        """First set up stereotypes of traits (sets of Enum) outside and add
        all the traits that should be included in a "class" of TraitBags. 
        Pass in those stereotypes and polish the rough edges by taking 
        away the traits that should be excluded.
        
        You really DO NOT want to subclass this. 
        The point of TraitBag is that they only represent state, so use stereotypes instead.
        Even more so, __slots__ don't play nice with subclassing 
        (a subclass creates its own dict, killing the whole point of __slots__), so, if you NEED
        a TraitBag with its own Methods, just copy the code and make your own.
        
        The bag is used with tokens (another Enum) for most simple use cases.
        If there's a need to extend a "class" of TraitBags, don't do it here.
        Instead, use some "global" WeakKeyDictionary or WeakValueDictionary to manage things.
        Keep in mind that in this case you will probably need one to 
        map from name to thing and then from thing to property.. and be VERY CAREFUL when you
        use more than one strong ref to the thing - otherwise the weakrefs WILL bite your butt!        
        
        One more thing: the point of TraitBag.clone() is to be able to prototype.
        You can build one complex prototype of a TraitBag, then replicate 
        the bugger without all the boilerplate. 
        Careful bout those global dicts though - the clone needs extra love.
        """
        self.name = uuid1() if name is None else name
        self.bag = Counter(bag)
        # unpack the list of stereotypes and sets of traits, yielding all traits
        # but since it's a SET-comprehension, return a set of traits
        self.traits = {t for S in stereotypes for t in S}
        self.traits.update(set(in_traits))
        self.traits.difference_update(set(ex_traits))
        
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return "{0}: {1}, {2}".format(self.name, self.traits, self.bag)
    
    def clone(self, name=None):
        c = copy(self)
        c.name = uuid1 if name is None else name
        return c
        

def walk(node):
    """ iterate tree in pre-order depth-first search order """
    yield node
    for child in node.children:
        for n in walk(child):
            yield n

class StateMachine:
    __slots__ = ["name", "states", "state", "__weakref__",]
    
    def __init__(self, *, states:dict, first, name=None, final=None):
        self.name = uuid1() if name is None else name
        self.states = {final:{}} if final is not None else {}
        self.states.update(states)
        self.state = first
        
    def flux_to(self, to_state):
        if to_state in self.states[self.state]:
            self.state = to_state
            return True
        else:
            return False
    
    def clone(self, name=None):
        c = copy(self)
        c.name = uuid1 if name is None else name
        return c
    
    def __str__(self):
        return str(self.name)
    
    def __repr__(self):
        return "{0} in {1} {2}".format(self.name, self.state, self.states)
            
class TraitMachine:
    def __init__(self, *, states:dict,  first, name="thing",
                final=None, bag:dict={},
                 stereotypes=[], in_traits=set(), ex_traits=set(), stateful_traits=(), children=()
                ):
        self.name = name
        self.stateful_traits = {first: set(), final: set()}
        self.states = {final:{}}
        self.states.update(states)
        self.stateful_traits.update(stateful_traits)
                
        self.stateless_traits = {t for S in stereotypes for t in S}
        self.stateless_traits.update(set(in_traits))
        self.stateless_traits.difference_update(set(ex_traits))
        
        self.state = first
        self.bag = Counter(bag)
        self.traits = self.stateless_traits | self.stateful_traits[self.state]
        if self.traits == set():
            warn("Thing has no traits!")
        
        
        # TODO: have children
        self.children = WeakSet(children)
        
        self.parent = None
        
        #if any(n == self for n in walk(self)):
         #   raise UserWarning("cycle detected.")
            
        if self.children:
            print(1)
            for c in self.children:
                print(c)
                c.parent = proxy(self)
        
    def flux_to(self, to_state):
        if to_state in self.states[self.state]:
            self.state = to_state
            self.traits = self.stateless_traits | self.stateful_traits.get(self.state, set())
            return True
        else:
            return False
    
    def clone(self, name=None):
        c = copy(self)
        c.name = uuid1 if name is None else name
        return c
    
    def __str__(self):
        return self.name

d = {}

def fdispatch(s):
    def wrapper(func):
        @wraps(func)
        def call(first, *args, **kwargs):
            d[frozenset(first)](first, *args, **kwargs)
        d[frozenset(s)] = func
        return call
    return wrapper

def mdispatch(s):
    def wrapper(func):
        @wraps(func)
        def call(self, first, *args, **kwargs):
            d[(func.__qualname__, frozenset(first))](self, first, *args, **kwargs)
        d[(func.__qualname__, frozenset(s))] = func
        return call
    return wrapper
        
def can(trait):
    def wrapper(method):
        def calling(self, thing, *args, **kwargs):
            if trait in thing.traits:
                method(self, thing, *args, **kwargs)
            else:
                warn("{0} isn't available while {1} {2}".format(
                        method.__qualname__, thing.name, thing.state))                
        return calling
    return wrapper