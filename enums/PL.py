from enum import Enum
from ..flux import can

IS = Enum("IS", "working, destroyed, done, ready, broken") 
BE = Enum("BE", "selected, destroyed, used, repaired, cancelled")
HAS = Enum("HAS", "amount")
OF = Enum("OF", "water, meat, paprica")

@can(BE.destroyed)
def destroy(self, thing):
    thing.flux_to(IS.destroyed)
    print("%s broke the %s!!!" % (self.__class__.__name__, thing.name))
