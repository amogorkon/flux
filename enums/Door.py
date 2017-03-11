from enum import Enum

IS = Enum('IS', 'closed, open, destroyed')
BE = Enum("BE", "opened, closed, written, entered, fubared")
HAS = Enum("HAS", "been_opened, hitpoints, been_fluxed")