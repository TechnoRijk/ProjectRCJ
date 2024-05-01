import unittest
from projectrcj import __init__
import projectrcj

class TestProjectRCJ(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(__init__.print_hello_world(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()
