import sys
# Providing a place to put celeryconfig.py so we don't have to export a
# PYTHONPATH variable which might have unintended side-effects.
sys.path.append('./pypath')

from apvy.defer import DeferredResult
from apvy.http import TwistedHttpTask, URL
