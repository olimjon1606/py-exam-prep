import unittest
import numpy as np
from identity import identity

class IdentityFunctionTest(unittest.TestCase):
    def test_identity(self):
        for x in range(-100, 101):
            result = identity(x)
            self.assertTrue(np.isclose(result, x))

if __name__ == '__main__':
    unittest.main()
