"""
Unit tests for ``random_strategy``.
"""
import unittest
from brownian.outils import Particle
from math import pi, cos, sin


class TestParticle(unittest.TestCase):

    def test_update_time(self):
        p = Particle(0, 0, 1, pi / 2, 10 ** -4)
        delta_time = 1
        p.update_time(delta_time)
        self.assertAlmostEqual(p.x, cos(pi / 2))
        self.assertAlmostEqual(p.y, sin(pi / 2))


if __name__ == '__main__':
    unittest.main()
