from meo.pollers.prolific import ProlificPoller
from meo.pollers.clickworker import ClickworkerPoller
from meo.pollers.freecash import FreecashPoller

ALL_POLLERS = [ProlificPoller(), FreecashPoller(), ClickworkerPoller()]
