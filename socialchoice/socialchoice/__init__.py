"""
This file holds the complete interface for this package, as everything in here can be imported as
socialchoice.{whatever} instead of socialchoice.{filename}.{whatever}

This allows us to factor out the package into multiple files while keeping a consistent user-facing API.
"""

from socialchoice.ballot import *
from socialchoice.election import *

import socialchoice.pairwisecollapse as pairwise_collapse
