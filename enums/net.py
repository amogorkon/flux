from enum import Enum

class IS(Enum):
	starting = 1
	connecting = 2
	ready = 3
	disconnected = 4
	down = 5

class BE(Enum):
	prepared = 1
	etc = 2