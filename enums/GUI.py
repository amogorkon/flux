from enum import Enum

IS = Enum("STATE", "loading login signup playing exiting")
CAN = Enum("CAN", "start navigate play configure")
BE  = Enum("BE", "closed clicked")
HAS = Enum("HAS", "clicks")