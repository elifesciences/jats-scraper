import unittest
import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))

class BaseCase(unittest.TestCase):
    this_dir = THIS_DIR
    maxDiff = None
