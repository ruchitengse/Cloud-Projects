import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/nearestcities')

from flaskapp import app as application