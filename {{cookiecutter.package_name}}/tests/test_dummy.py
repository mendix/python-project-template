import unittest

from {{cookiecutter.package_name}}.dummy import dummy


class TestDummy(unittest.TestCase):
    def test_dummy(self) -> None:
        self.assertTrue(dummy())
