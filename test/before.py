"""Before testfile fixture"""

import os
import sys
import importlib

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, path)

path = os.path.join(
    os.path.dirname(__file__),
    '..',
    'src',
    '__main__.py'
)
path = os.path.abspath(path)
# path = os.path.join(BASE_DIR, 'templates', maintype, FACTORY_FILENAME)

# path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(path)
print(type(path))


# import importlib.util
loader = importlib.machinery.SourceFileLoader('main', path)
print(loader)
main = loader.load_module()
print(main)
# foo.MyClass()


