import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

from skybird import app as application
application.secret_key = '[[A SECRET KEY]]'
