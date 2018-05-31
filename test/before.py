"""Fixture: Before testfile"""

import os
import sys
import importlib

# Add src folder to sys.path
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, path)

# Expose src/__main__.py as main
path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'src',
    '__main__.py'
)
path = os.path.abspath(path)
loader = importlib.machinery.SourceFileLoader('main', path)

main = loader.load_module()
