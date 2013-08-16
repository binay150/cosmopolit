import sys, os
_root = os.path.dirname(os.path.abspath(__file__)).split(os.path.sep)
sys.path.extend([
    os.path.sep.join(_root + ['ThirdParty']),
    os.path.sep.join(_root + ['Configuration']),
    os.path.sep.join(_root + ['Common']),
    os.path.sep.join(_root + ['DB']),
    os.path.sep.join(_root + ['Library']),
    os.path.sep.join(_root),
])
print _root
from Configuration import InitializeConfiguration
from Configuration import Log
from NewsPaperConstants import NewsPapers
from managers import *
if __name__ == '__main__':
    print >> sys.stderr, """\
use: gunicorn -c gunicorn.conf.py Cosmopolit
"""
    sys.exit(1)

from cosmopolits import app as application
