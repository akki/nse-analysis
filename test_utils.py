import unittest

from utils import get_xirr


class TestGetXIRR(unittest.TestCase):

    def test_cases(self):
        test_cases = [
            ([(1000, 730), (1000, 365)], 6000, 100.0),
            ([(1000, 365)], 2000, 100.0),
            ([(1000, 0)], 1000, 0.0),
            ([(1000, 365), (2000, 0)], 3000, 0.0),
            ([(1000, 365), (1000, 730)], 8000, 137.22),
        ]

        for investments, current_value, expected_xirr in test_cases:
            calculated_xirr = get_xirr(investments, current_value)
            self.assertAlmostEqual(
                calculated_xirr,
                expected_xirr,
                places=2,
                msg=(
                    f"Failed for investments={investments}, "
                    f"current_value={current_value}: "
                    f"expected {expected_xirr}, got {calculated_xirr}"
                )
            )

if __name__ == "__main__":
    unittest.main()
